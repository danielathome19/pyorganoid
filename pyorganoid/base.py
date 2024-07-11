class Agent:
    """
    Base class for all agents in the simulation (not to be instantiated directly). It represents a single entity in the
    environment and is used as an interface for different types of agents (e.g., cells, molecules).
    The agent can have multiple modules that define its behavior.

    Parameters
    ----------
    position : tuple
        The position of the agent in the environment.

    Attributes
    ----------
    position : {tuple, int}
        The position of the agent in the environment.
    modules : list
        List of modules that define the behavior of the agent.

    Methods
    -------
    add_module(module)
        Add a module to the agent.
    update()
        Update the agent's state based on its modules.
    """

    def __init__(self, position):
        self.position = position
        self.modules = []

    def add_module(self, module):
        """
        Add a module to the agent.

        Parameters
        ----------
        module : BaseModule
            The module to add to the agent.
        """
        self.modules.append(module)

    def update(self):
        """
        Update the agent's state based on its modules.
        This method should be called at each time step to update the agent's state based on its modules.
        """
        for module in self.modules:
            module.run(self)


class Cell(Agent):
    """
    Base class for all cell agents in the simulation (typically not instantiated directly). It represents a single cell
    in the environment and extends the Agent class with additional functionality specific to cells.
    It is a subclass of the Agent class.

    Parameters
    ----------
    position : tuple
        The position of the cell in the environment.
    input_data_func : function, optional
        The input data function for the cell. Default is None.

    Attributes
    ----------
    position : {tuple, int}
        The position of the cell in the environment.
    modules : list
        List of modules that define the behavior of the cell.
    history : list
        List of historical values for the cell.
    input_data_func : function
        The input data function for the cell.

    Methods
    -------
    add_module(module)
        Add a module to the cell.
    update(historical_value=None)
        Update the cell's state based on its modules and historical value.
    get_history()
        Get the historical values of the cell.
    default_input_data_func()
        Default input data function for the cell.
    get_input_data()
        Get the input data for the cell.
    """

    def __init__(self, position, input_data_func=None):
        super().__init__(position)
        self.history = []
        self.input_data_func = input_data_func if input_data_func is not None \
            else lambda _: (_ for _ in ()).throw(NotImplementedError("Subclasses should implement this method!"))

    def update(self, historical_value=None):
        """
        Update the cell's state based on its modules and historical value.

        Parameters
        ----------
        historical_value : any, optional
            The historical value to append to the cell's history. Default is None.
        """
        super().update()
        if historical_value is not None:
            self.history.append(historical_value)

    def get_history(self):
        """
        Get the historical values of the cell.

        Returns
        -------
        list
            List of historical values for the cell.
        """
        return self.history

    def get_input_data(self, _=None):
        """
        Get the input data for the neuron.

        Returns
        -------
        list
            List of input data values.
        """
        return self.input_data_func(_)


class Synapse:
    """
    Base class for synapses connecting neurons in the simulation. It represents a connection between two neurons and
    is used to transmit signals between them.

    Parameters
    ----------
    pre_neuron : SpikingNeuronCell
        The pre-synaptic neuron.
    post_neuron : SpikingNeuronCell
        The post-synaptic neuron.
    weight : float, optional
        The weight of the synapse. Default is 0.5.

    Attributes
    ----------
    pre_neuron : SpikingNeuronCell
        The pre-synaptic neuron.
    post_neuron : SpikingNeuronCell
        The post-synaptic neuron.
    weight : float
        The weight of the synapse.
    """

    def __init__(self, pre_neuron, post_neuron, weight=0.5):
        self.pre_neuron = pre_neuron
        self.post_neuron = post_neuron
        self.weight = weight

    def transmit(self):
        """
        Transmit a signal from the pre-synaptic neuron to the post-synaptic neuron.
        This method is called when the pre-synaptic neuron fires an action potential.
        The post-synaptic neuron's membrane potential is increased by the weight of the synapse.
        """
        if self.pre_neuron.membrane_potential >= self.pre_neuron.threshold:
            self.post_neuron.membrane_potential += self.weight


class Organoid:
    """
    Base class for all organoids in the simulation (typically not instantiated directly). It represents a collection of
    agents in the environment and is used to simulate the behavior of a group of agents.

    Parameters
    ----------
    environment : Environment
        The environment in which the organoid exists.

    Attributes
    ----------
    environment : Environment
        The environment in which the organoid exists.
    agents : list
        List of agents (e.g., cells) in the organoid.

    Methods
    -------
    add_agent(agent)
        Add an agent to the organoid.
    get_cells()
        Get the list of agents in the organoid.
    """

    def __init__(self, environment):
        self.environment = environment
        self.agents = []

    def add_agent(self, agent):
        """
        Add an agent to the organoid.

        Parameters
        ----------
        agent : Agent
            The agent to add to the organoid.
        """
        self.agents.append(agent)

    def get_cells(self):
        """
        Get the list of agents in the organoid.

        Returns
        -------
        list
            List of agents (e.g., cells) in the organoid.
        """
        return self.agents

    def plot_organoid(self, filename=None, show_properties=True, dpi=300, truncate_cells=10):
        """
        Plot the structure of the organoid using Graphviz.

        Parameters
        ----------
        filename : str, optional
            The filename to save the plot as (in PNG format). Default is None.
        show_properties : bool, optional
            Whether to show properties of the agents and modules in the plot. Default is True.
        dpi : int, optional
            The DPI (dots per inch) of the plot. Default is 300.
        truncate_cells : int, optional
            The number of cells to show in the plot. If there are more cells, the remaining cells will be truncated.
            Default is 10.

        Raises
        ------
        ImportError
            If Graphviz is not installed.
        """
        try:
            from graphviz import Digraph
            dot = Digraph()
            dot.attr(dpi=str(dpi))

            # Add environment; prepend "Base" to environment name if it is the base class
            env_name = type(self.environment).__name__
            env_label = f'Environment: {"Base" + env_name if env_name == "Environment" else ""}' + (
                        f'\nDimensions: {self.environment.dimensions}\nSize: {self.environment.size}'
                        if show_properties else '')
            dot.node('env', env_label, shape='rectangle')

            # Add organoid with superclass name
            organoid_label = f'Organoid: {type(self).__name__}' + (f'\nAgents: {len(self.agents)}'
                                                                   if show_properties else '')
            dot.node('organoid', organoid_label)
            dot.edge('env', 'organoid')

            # Add cells and their modules
            cell_ids = []
            do_truncate = (truncate_cells is not None) and (len(self.agents) > truncate_cells)
            for i, cell in enumerate(self.get_cells()):
                # If there are more than TRUNCATE_CELLS cells, show cells 1-[TRUNCATE-1], (...) node, and last cell
                if do_truncate and (i == truncate_cells-1):
                    ellipses_id = f'cell_{truncate_cells-1}'
                    dot.node(ellipses_id, '...', shape='none')
                    dot.edge('organoid', ellipses_id, style='invis')
                    cell_ids.append(ellipses_id)

                    ellipses_id = f'{truncate_cells-1}_mod_{0}'
                    dot.node(ellipses_id, '...', shape='none')
                    dot.edge(f'cell_{truncate_cells-1}', ellipses_id, style='invis')
                    dot.edge(ellipses_id, 'ml_model', style='invis')

                    cell = self.get_cells()[-1]
                    i = len(self.get_cells()) - 1

                cell_id = f'cell_{i}'
                cell_ids.append(cell_id)
                # Round each value in the position tuple to 2 decimal places
                cell_label = f'Cell {i+1}: {type(cell).__name__}' + (
                             f'\nPosition: {tuple(map(lambda x: round(x, 2), cell.position))}'
                             if show_properties else '')
                dot.node(cell_id, cell_label)
                dot.edge('organoid', cell_id)

                # Add modules to each cell
                for j, module in enumerate(cell.modules):
                    module_id = f'{cell_id}_mod_{j}'
                    module_label = f'Module {j+1}: {type(module).__name__}'
                    dot.node(module_id, module_label)
                    dot.edge(cell_id, module_id)

                    # Add ML model reference if available
                    if hasattr(module, 'ml_model'):
                        ml_model_input_shape = module.ml_model.input_shape
                        ml_model_id = 'ml_model'  # f'{module_id}_ml'
                        ml_model_label = type(module.ml_model).__name__ + (f'\nInput Shape: {ml_model_input_shape}'
                                                                           if show_properties else '')
                        dot.node(ml_model_id, ml_model_label)
                        with dot.subgraph() as s:
                            s.attr(rank='same')
                            s.node(ml_model_id, shape='rectangle')
                        dot.edge(module_id, ml_model_id, dir='back')

                if do_truncate and (i == len(self.get_cells()) - 1):
                    break

            with dot.subgraph() as s:
                s.attr(rank='same')
                for cell_id in cell_ids:
                    s.node(cell_id)

            if filename is not None:
                # If the filename has an extension, use it; otherwise, default to PNG
                ext = filename.split('.')[-1] if len(filename.split('.')) > 1 else 'png'
                filename = filename.split('.')[0]
                dot.render(filename, format=ext, cleanup=True)
                print(f'Organoid structure plot saved as "{filename}.{ext}"')
            else:
                dot.view()
        except ImportError as e:
            print("Error: Graphviz is required to plot the organoid structure.")
            raise e

    def plot_simulation_history(self, title, y_label, x_label="Time Steps", filename=None, dpi=300, figsize=(10, 6)):
        """
        Plot the simulation history of the organoid using Matplotlib.

        Parameters
        ----------
        title : str
            The title of the plot.
        y_label : str
            The label for the y-axis.
        x_label : str, optional
            The label for the x-axis. Default is "Time Steps".
        filename : str, optional
            The filename to save the plot as (in PNG format). Default is None (view the image with plt.show()).
        dpi : int, optional
            The DPI (dots per inch) of the plot. Default is 300.
        figsize : tuple, optional
            The size of the figure (width, height) in inches. Default is (10, 6).

        Raises
        ------
        ImportError
            If Matplotlib is not installed.
        """
        try:
            import numpy as np
            import matplotlib.pyplot as plt

            def contains_arrays(lst):
                """Check if the list contains any numpy arrays."""
                return any(isinstance(item, np.ndarray) for item in lst)

            def flatten_list(lst):
                """Flatten a list containing numpy arrays."""
                return [item if not isinstance(item, np.ndarray) else item.item() for item in lst]

            plt.figure(figsize=figsize)
            for i, cell in enumerate(self.get_cells()):
                history = cell.get_history()
                if contains_arrays(history):
                    history = flatten_list(history)
                plt.plot(history, label=f'Cell {i + 1}')

            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(title)
            plt.legend()
            if filename is not None:
                plt.savefig(filename, dpi=dpi)
                print(f'Simulation history plot saved as "{filename}"')
            else:
                plt.show()
        except ImportError as e:
            print("Error: Matplotlib and NumPy are required to plot the simulation history.")
            raise e
