__import__("warnings").filterwarnings("ignore")


def main():
    try:
        import joblib
        import numpy as np
        import matplotlib.pyplot as plt
        from sklearn.tree import DecisionTreeClassifier
        from pyorganoid import (Organoid, GrowthShrinkageOrganoid, SklearnModel, StochasticEnvironment,
                                Scheduler, StochasticScheduler, PriorityScheduler, ParallelScheduler)

        # Synthetic data for volumetric model
        np.random.seed(42)
        volumes = np.linspace(0, 10, 1000).reshape(-1, 1)
        noise = np.random.normal(0, 0.5, volumes.shape)
        labels = ((volumes + noise) > 1).astype(int)  # Binary target: 1 if volume + noise > 1, else 0

        model = DecisionTreeClassifier()
        model.fit(volumes, labels)

        model_path = "dtree_model.pkl"
        joblib.dump(model, model_path)

        ml_model = SklearnModel(model_path)

        environment = StochasticEnvironment(noise_level=0.1)

        organoid = GrowthShrinkageOrganoid(environment, ml_model, num_cells=20, initial_cell_volume=None,
                                           growth_amount=0.01, growth_variance=0.05)
        organoid.plot_organoid("volumetric_organoid.png", show_properties=True, dpi=300)

        print("Running simulation...")
        # scheduler = StochasticScheduler(organoid)
        # scheduler.simulate(steps=25)

        priorities = {agent: np.random.randint(1, 10) for agent in organoid.agents}
        scheduler = PriorityScheduler(organoid, priorities)
        scheduler.simulate(steps=25)

        # scheduler = ParallelScheduler(organoid)
        # scheduler.simulate(steps=25)

        # scheduler = Scheduler(organoid)
        # scheduler.simulate(steps=25)

        organoid.plot_simulation_history('Volume of Cells Over Time', 'Volume',
                                         filename='volume_simulation.png', dpi=300)
    except ImportError as e:
        print(e)


if __name__ == "__main__":
    main()


def test_main():
    assert True
