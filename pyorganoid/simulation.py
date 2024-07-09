import numpy as np


class Scheduler:
    """
    Base class for simulation schedulers. Can be used to simulate the behavior of an organoid in a given environment.

    Parameters
    ----------
    organoid : Organoid
        The organoid to simulate.

    Attributes
    ----------
    organoid : Organoid
        The organoid to simulate.

    Methods
    -------
    simulate(steps)
        Simulate the organoid's behavior over a number of steps.
    """
    def __init__(self, organoid):
        self.organoid = organoid

    def simulate(self, steps):
        """
        Simulate the organoid's behavior over a number of steps.

        Parameters
        ----------
        steps : int
            The number of steps to run the simulation.
        """
        for step in range(steps):
            print(f"Step {step+1}/{steps}")
            self.organoid.environment.update()
            for agent in self.organoid.agents:
                agent.update()


class StochasticScheduler(Scheduler):
    """
    Scheduler that simulates the organoid's behavior with a stochastic update rule.
    The update rule is applied to each agent with a 50% chance.
    It is a subclass of the base Scheduler class.

    Parameters
    ----------
    organoid : Organoid
        The organoid to simulate.

    Attributes
    ----------
    organoid : Organoid
        The organoid to simulate.

    Methods
    -------
    simulate(steps)
        Simulate the organoid's behavior over a number of steps with a stochastic update rule.
    """
    def simulate(self, steps):
        """
        Simulate the organoid's behavior over a number of steps with a stochastic update rule.
        The update rule is applied to each agent with a 50% chance.

        Parameters
        ----------
        steps : int
            The number of steps to run the simulation.
        """
        for step in range(steps):
            print(f"Step {step+1}/{steps}")
            self.organoid.environment.update()
            for agent in self.organoid.agents:
                if np.random.rand() > 0.5:  # 50% chance to update the agent
                    agent.update()


class PriorityScheduler(Scheduler):
    """
    Scheduler that simulates the organoid's behavior based on a priority system.
    Agents are updated in order of decreasing priority.
    It is a subclass of the base Scheduler class.

    Parameters
    ----------
    organoid : Organoid
        The organoid to simulate.
    priorities : dict
        A dictionary of agent priorities.

    Attributes
    ----------
    organoid : Organoid
        The organoid to simulate.
    priorities : dict
        A dictionary of agent priorities.

    Methods
    -------
    simulate(steps)
        Simulate the organoid's behavior over a number of steps based on a priority system.
    """
    def __init__(self, organoid, priorities):
        super().__init__(organoid)
        self.priorities = priorities

    def simulate(self, steps):
        """
        Simulate the organoid's behavior over a number of steps based on a priority system.
        Agents are updated in order of decreasing priority.

        Parameters
        ----------
        steps : int
            The number of steps to run the simulation.
        """
        for step in range(steps):
            print(f"Step {step+1}/{steps}")
            self.organoid.environment.update()
            sorted_agents = sorted(self.organoid.agents, key=lambda agent: self.priorities.get(agent, 0), reverse=True)
            for agent in sorted_agents:
                agent.update()


class ParallelScheduler(Scheduler):
    """
    Scheduler that runs the simulation in parallel using multiple CPU cores.
    The class has not yet been implemented.
    It is a subclass of the base Scheduler class.

    Parameters
    ----------
    organoid : Organoid
        The organoid to simulate.

    Attributes
    ----------
    organoid : Organoid
        The organoid to simulate.

    Methods
    -------
    simulate(steps)
        Simulate the organoid's behavior over a number of steps.
    """

    def simulate(self, steps):
        """
        Simulate the organoid's behavior over a number of steps.

        This method is intended to run the simulation in parallel using multiple
        CPU cores. Currently, this function is not yet implemented. Using joblib may
        be the most feasible way to implement parallel simulation over multiprocessing;
        however, the cell history is neither preserved nor updated correctly when executed in parallel.

        Parameters
        ----------
        steps : int
            The number of steps to run the simulation.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError("Parallel simulation is not yet implemented. Please use a different scheduler.")
