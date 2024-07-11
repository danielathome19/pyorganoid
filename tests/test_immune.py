def main():
    try:
        import numpy as np
        import matplotlib.pyplot as plt
        from skl2onnx import convert_sklearn
        from sklearn.linear_model import LogisticRegression
        from skl2onnx.common.data_types import FloatTensorType
        from pyorganoid import Organoid, ImmuneResponseOrganoid, ONNXModel, Environment, Scheduler, ImmuneCell

        # Generate synthetic data
        np.random.seed(42)
        X = np.random.rand(1000, 1).astype(np.float32)  # One feature: immune response
        y = (X > 0.5).astype(int).ravel()  # Binary target: active (1) or not active (0) based on immune response

        model = LogisticRegression()
        model.fit(X, y)

        # Convert the model to ONNX format
        initial_type = [('float_input', FloatTensorType([1, None]))]
        onnx_model = convert_sklearn(model, initial_types=initial_type)
        model_path = "logreg_model.onnx"
        with open(model_path, "wb") as f:
            f.write(onnx_model.SerializeToString())

        ml_model = ONNXModel(model_path, input_shape=(1,))
        environment = Environment(dimensions=3, size=50)

        def custom_input_data_func(cell: ImmuneCell):
            return (sum(cell.position) / 150) - np.random.rand() / 2

        organoid = ImmuneResponseOrganoid(environment, ml_model, num_cells=5, input_data_func=custom_input_data_func)
        organoid.plot_organoid("immune_response_organoid.png", show_properties=True, dpi=300)

        print("Running simulation...")
        scheduler = Scheduler(organoid)
        scheduler.simulate(steps=50)

        organoid.plot_simulation_history('Immune Cell Activity Over Time', 'Active State',
                                         filename='immune_response_simulation.png', dpi=300)
    except ImportError as e:
        print(e)


if __name__ == "__main__":
    main()


def test_main():
    assert True
