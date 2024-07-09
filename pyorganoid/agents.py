class AgentContainer:
    """
    Container for agents in the simulation.

    Attributes
    ----------
    agents : list
        List of agents in the simulation.

    Methods
    -------
    add_agent(agent)
        Add an agent to the container.
    get_agents()
        Get all agents in the container.
    get_agent_by_id(agent_id)
        Get an agent by its ID.
    """
    def __init__(self):
        self.agents = []

    def add_agent(self, agent):
        """
        Add an agent to the container.

        Parameters
        ----------
        agent : Agent
            The agent to add to the container.
        """
        self.agents.append(agent)

    def get_agents(self):
        """
        Get all agents in the container.

        Returns
        -------
        list
            List of agents in the container.
        """
        return self.agents

    def get_agent_by_id(self, agent_id):
        """
        Get an agent from the container by its ID.

        Parameters
        ----------
        agent_id : int
            The ID of the agent to get.

        Returns
        -------
        Agent
            The agent with the given ID, or None if not found.
        """
        return next((agent for agent in self.agents if agent.id == agent_id), None)


class AgentHandle:
    """
    Handle for an agent in the simulation.

    Attributes
    ----------
    agent_id : int
        The ID of the agent.
    container : AgentContainer
        The container that holds the agent.

    Methods
    -------
    get_agent()
        Get the agent from the container.
    """
    def __init__(self, agent_id, container):
        self.agent_id = agent_id
        self.container = container

    def get_agent(self):
        """
        Get the agent from the container.

        Returns
        -------
        Agent
            The agent with the given ID.
        """
        return self.container.get_agent_by_id(self.agent_id)
