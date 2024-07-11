def main():
    try:
        import numpy as np
        import matplotlib.pyplot as plt
        from keras.layers import Dense
        from keras.models import Sequential
        from pyorganoid import Organoid, SpikingNeuronOrganoid, TFModel, Environment, Scheduler, SpikingNeuronCell

        model = Sequential([
            Dense(32, activation='relu', input_shape=(10,)),
            Dense(16, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        np.random.seed(42)
        X = np.random.rand(1000, 10)
        y = (np.sum(X, axis=1) > 5).astype(int)
        model_path = "mlp_model.h5"

        model.fit(X, y, epochs=10, batch_size=32)
        model.save(model_path)

        ml_model = TFModel(model_path, input_shape=(10,))

        # Input function where input data is based on the position of the neuron
        def custom_input_data_func(neuron: SpikingNeuronCell):
            pos = neuron.position  # Get the position of the neuron in the 3D environment and reduce it to 1D input data
            return [0.5 + (pos[0] % 5) * 0.1, 0.5 + (pos[1] % 5) * 0.1, 0.5 + (pos[2] % 5) * 0.1] * 3 + [0.5]

        environment = Environment(dimensions=3, size=50)

        # Initialize the organoid and add agents
        organoid = SpikingNeuronOrganoid(environment, ml_model, input_data_func=custom_input_data_func, num_cells=10)
        organoid.plot_organoid("spiking_organoid.png", show_properties=True, dpi=300)

        print("Running simulation...")
        scheduler = Scheduler(organoid)
        scheduler.simulate(steps=50)

        organoid.plot_simulation_history('Membrane Potential of Neurons Over Time', 'Membrane Potential',
                                         filename='membrane_potential_simulation.png', dpi=300)

        """ Notes:
        Oscillatory Behavior
        --------------------
            The neurons exhibit oscillatory behavior in their membrane potentials, indicating periodic spiking activity. 
            This is typical in certain types of neurons, especially those modeled in simplified spiking neuron simulations.

        Synchronization
        ----------------
            The neurons appear synchronized as the membrane potentials rise and fall together. 
            This suggests that the input from the machine learning model uniformly affects the neurons.

        Membrane Potential Range
        -------------------------
            The membrane potentials range from around 0.8 to 2.0. 
            This indicates that the neurons are spiking and resetting their potentials periodically.

        Spiking Threshold
        -----------------
            The potential reaches its peak at around 2.0, 
            which could be the spiking threshold where neurons reset their membrane potential to a lower value (around 0.8).

        Influence of ML Model
        ---------------------
            The input data generated by the custom function influences the neurons’ membrane potentials. 
            Since the custom input data function is based on the neuron’s position, 
            the neurons receive inputs that drive synchronized spiking patterns.
        """
    except ImportError as e:
        print(e)


if __name__ == "__main__":
    main()


def test_main():
    assert True