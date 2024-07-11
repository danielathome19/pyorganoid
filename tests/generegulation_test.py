try:
    import torch
    import numpy as np
    import torch.nn as nn
    import torch.optim as optim
    import matplotlib.pyplot as plt
    from pyorganoid import Organoid, GeneRegulationOrganoid, TorchModel, Environment, Scheduler, GeneRegulationCell

    class SimpleMLP(nn.Module):
        def __init__(self, input_size):
            super(SimpleMLP, self).__init__()
            self.fc1 = nn.Linear(input_size, 32)
            self.fc2 = nn.Linear(32, 16)
            self.fc3 = nn.Linear(16, 1)
            self.sigmoid = nn.Sigmoid()

        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = torch.relu(self.fc2(x))
            x = self.sigmoid(self.fc3(x))
            return x

    # Generate random data for gene expression levels
    np.random.seed(42)
    X = np.random.rand(1000, 1).astype(np.float32)  # Single feature input
    y = (X.flatten() > 0.5).astype(int).reshape(-1, 1).astype(np.float32)

    # Adjust the labels ensure class balance
    y[:500] = 0
    y[500:] = 1

    # Convert data to PyTorch tensors
    X_tensor = torch.tensor(X)
    y_tensor = torch.tensor(y)

    model = SimpleMLP(input_size=1)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(25):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_tensor)
        loss = criterion(outputs, y_tensor)
        loss.backward()
        optimizer.step()
        print(f'Epoch [{epoch+1}/25], Loss: {loss.item():.4f}, Accuracy: '
              f'{((outputs > 0.5) == y_tensor).sum().item() / len(y):.2f}')

    model_path = "generegulation_model.pth"
    torch.save(model.state_dict(), model_path)
    ml_model = TorchModel(model_path, model_class=SimpleMLP, input_shape=(1,))

    # Input function where input data is based on the gene expression level and position of the cell (for testing)
    def custom_input_data_func(cell: GeneRegulationCell):
        gene_exp_level = cell.gene_expression_level
        position = cell.position
        return gene_exp_level + (position[0] % 5) * 0.1 + (position[1] % 5) * 0.1

    environment = Environment(dimensions=2, size=50)
    organoid = GeneRegulationOrganoid(environment, ml_model, num_cells=10, regulation_variance=0.05,
                                      input_data_func=custom_input_data_func)
    organoid.plot_organoid("gene_regulation_organoid.png", show_properties=True, dpi=300)

    print("Running simulation...")
    scheduler = Scheduler(organoid)
    scheduler.simulate(steps=25)

    organoid.plot_simulation_history('Gene Expression Levels Over Time', 'Gene Expression Level',
                                     filename='generegulation_simulation', dpi=300)
except ImportError as e:
    print(e)
