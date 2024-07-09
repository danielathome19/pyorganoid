from .base import Cell


class SpikingNeuronCell(Cell):
    """
    A simple spiking neuron cell model (e.g., a Leaky Integrate-and-Fire neuron).
    The membrane potential is reset to zero after spiking.
    It is a subclass of the base Cell class.

    Parameters
    ----------
    position : {tuple, int}
        The position of the cell.
    threshold : float, optional
        The threshold for spiking. Default is 1.0.
    input_data_func : function, optional
        A function to generate input data for the neuron. Default is None.

    Attributes
    ----------
    position : {tuple, int}
        The position of the cell in the environment.
    modules : list
        List of modules that define the behavior of the cell.
    history : list
        List of historical values for the cell.
    membrane_potential : float
        The membrane potential of the neuron.
    threshold : float
        The threshold for spiking.
    input_data_func : function
        The function to generate input data for the neuron.

    Methods
    -------
    update()
        Update the cell's state.
    get_history()
        Get the historical values of the cell.
    spike(verbose=False)
        Spike the neuron.
    default_input_data_func()
        Default input data function based on position.
    get_input_data()
        Get the input data for the neuron.
    """
    def __init__(self, position, threshold=1.0, input_data_func=None):
        super().__init__(position)
        self.membrane_potential = 0.0
        self.threshold = threshold
        self.input_data_func = input_data_func or self.default_input_data_func

    def spike(self, verbose=False):
        """
        Spike the neuron. The membrane potential is reset to zero after spiking.

        Parameters
        ----------
        verbose : bool, optional
            Whether to print verbose output. Default is False
        """
        self.membrane_potential = 0.0  # Reset potential after spiking
        if verbose:
            print(f"Neuron at {self.position} spiked!")

    @staticmethod
    def default_input_data_func():
        """
        Default input data function based on position.
        Simply returns a list of 10 input values (this should be overridden by providing an input data function).

        Returns
        -------
        list
            List of input data values.
        """
        return [0.5] * 10  # 10 input values

    def get_input_data(self):
        """
        Get the input data for the neuron.

        Returns
        -------
        list
            List of input data values.
        """
        return self.input_data_func(self)

    def update(self):
        """
        Update the cell's state. Record the membrane potential and spike if it exceeds the threshold.
        """
        super().update(self.membrane_potential)  # Record the membrane potential
        if self.membrane_potential >= self.threshold:
            self.spike()


class GrowthShrinkageCell(Cell):
    """
    A simple cell model that grows and shrinks based on a volume parameter (e.g., in response to nutrient availability).
    It is a subclass of the base Cell class.

    Parameters
    ----------
    position : {tuple, int}
        The position of the cell.
    initial_volume : float, optional
        The initial volume of the cell. Default is 1.0.

    Attributes
    ----------
    position : {tuple, int}
        The position of the cell in the environment.
    modules : list
        List of modules that define the behavior of the cell.
    history : list
        List of historical values for the cell.
    volume : float
        The volume of the cell.

    Methods
    -------
    update()
        Update the cell's state.
    get_history()
        Get the historical values of the cell.
    grow(amount)
        Grow the cell by a specified amount.
    shrink(amount)
        Shrink the cell by a specified amount.
    get_volume()
        Get the volume of the cell.
    """
    def __init__(self, position, initial_volume=1.0):
        super().__init__(position)
        self.volume = initial_volume

    def update(self):
        """
        Update the cell's state based on its volume.
        """
        super().update(self.volume)

    def grow(self, amount):
        """
        Grow the cell by a specified amount.

        Parameters
        ----------
        amount : float
            The amount to grow the cell by.
        """
        self.volume += amount

    def shrink(self, amount):
        """
        Shrink the cell by a specified amount.

        Parameters
        ----------
        amount : float
            The amount to shrink the cell by.
        """
        self.volume -= amount

    def get_volume(self):
        """
        Get the current volume of the cell.

        Returns
        -------
        float
            The volume of the cell.
        """
        return self.volume


class DifferentiatingCell(Cell):
    """
    A simple cell model that can differentiate into different states (e.g., an undifferentiated stem cell).
    It is a subclass of the base Cell class.

    Parameters
    ----------
    position : {tuple, int}
        The position of the cell.
    state : str, optional
        The initial state of the cell. Default is 'undifferentiated'.

    Attributes
    ----------
    position : {tuple, int}
        The position of the cell in the environment.
    modules : list
        List of modules that define the behavior of the cell.
    history : list
        List of historical values for the cell.
    state : str
        The state of the cell.

    Methods
    -------
    update()
        Update the cell's state.
    get_history()
        Get the historical values of the cell.
    differentiate(new_state)
        Differentiate the cell into a new state.
    get_state()
        Get the state of the cell.
    """
    def __init__(self, position, state='undifferentiated'):
        super().__init__(position)
        self.state = state

    def update(self):
        """
        Update the cell's state based on its current state.
        """
        super().update(self.state)

    def differentiate(self, new_state):
        """
        Differentiate the cell into a new state.

        Parameters
        ----------
        new_state : str
            The new state of the cell.
        """
        self.state = new_state

    def get_state(self):
        """
        Get the current state of the cell.

        Returns
        -------
        str
            The state of the cell.
        """
        return self.state


class ChemotacticCell(Cell):
    """
    A simple cell model that can move towards a chemotactic gradient (e.g., in response to a chemical signal).
    It is a subclass of the base Cell class.

    Parameters
    ----------
    position : {tuple, int}
        The position of the cell.

    Attributes
    ----------
    position : {tuple, int}
        The position of the cell in the environment.
    modules : list
        List of modules that define the behavior of the cell.
    history : list
        List of historical values for the cell.
    chemotactic_gradient : float
        The chemotactic gradient for the cell.
        Positive values indicate movement towards the gradient.
        Negative values indicate movement away from the gradient.

    Methods
    -------
    update()
        Update the cell's state.
    get_history()
        Get the historical values of the cell.
    move_towards_gradient(gradient)
        Move the cell towards the specified gradient.
    get_chemotactic_gradient()
        Get the chemotactic gradient of the cell.
    """
    def __init__(self, position):
        super().__init__(position)
        self.chemotactic_gradient = 0.0

    def update(self):
        """
        Update the cell's state based on the chemotactic gradient.
        """
        super().update(self.chemotactic_gradient)

    def move_towards_gradient(self, gradient):
        """
        Move the cell towards the specified gradient.

        Parameters
        ----------
        gradient : float
            The gradient to move towards.
        """
        self.position += gradient

    def get_chemotactic_gradient(self):
        """
        Get the chemotactic gradient of the cell.

        Returns
        -------
        float
            The chemotactic gradient of the cell.
        """
        return self.chemotactic_gradient


class ImmuneCell(Cell):
    """
    A simple immune cell model that can be activated or deactivated (e.g., in response to an infection).
    It is a subclass of the base Cell class.

    Parameters
    ----------
    position : {tuple, int}
        The position of the cell.
    active : bool, optional
        Whether the cell is initially active. Default is False.

    Attributes
    ----------
    position : {tuple, int}
        The position of the cell in the environment.
    modules : list
        List of modules that define the behavior of the cell.
    history : list
        List of historical values for the cell.
    active : bool
        Whether the cell is currently active.

    Methods
    -------
    update()
        Update the cell's state.
    get_history()
        Get the historical values of the cell.
    activate()
        Activate the cell.
    deactivate()
        Deactivate the cell.
    is_active()
        Check if the cell is currently active or not.
    """
    def __init__(self, position, active=False):
        super().__init__(position)
        self.active = active

    def update(self):
        """
        Update the cell's state based on its activation status.
        """
        super().update(self.active)

    def activate(self):
        """
        Activate the cell.
        """
        self.active = True

    def deactivate(self):
        """
        Deactivate the cell.
        """
        self.active = False

    def is_active(self):
        """
        Check if the cell is currently active or not.

        Returns
        -------
        bool
            True if the cell is active, False otherwise.
        """
        return self.active


class SynapticPlasticityCell(Cell):
    """
    A simple cell model that can form synapses with other cells and transmit signals between them.
    The cells are connected by synapses that can change their strength based on the timing of spikes (e.g., STDP).
    It is a subclass of the base Cell class.

    Parameters
    ----------
    position : {tuple, int}
        The position of the cell.
    initial_synapses : list, optional
        List of initial synapses for the cell. Default is None.

    Attributes
    ----------
    position : {tuple, int}
        The position of the cell in the environment.
    modules : list
        List of modules that define the behavior of the cell.
    history : list
        List of historical values for the cell.
    synapses : list
        List of synapses connected to the cell.

    Methods
    -------
    update()
        Update the cell's state.
    add_synapse(synapse)
        Add a synapse to the cell.
    """
    def __init__(self, position, initial_synapses=None):
        super().__init__(position)
        self.synapses = initial_synapses if initial_synapses else []

    def update(self, historical_value=None):
        """
        Update the cell's state based on its synapses and historical value.
        Transmit signals between connected cells.

        Parameters
        ----------
        historical_value : any, optional
            The historical value to append to the cell's history. Default is None.
        """
        super().update(historical_value)
        for synapse in self.synapses:
            synapse.transmit()

    def add_synapse(self, synapse):
        """
        Add a synapse to the cell.
        """
        self.synapses.append(synapse)


class MetabolicCell(Cell):
    """
    A simple cell model that metabolizes energy based on a specified rate (e.g., in response to nutrient availability).
    It is a subclass of the base Cell class.

    Parameters
    ----------
    position : {tuple, int}
        The position of the cell.
    metabolism_rate : float, optional
        The rate at which the cell metabolizes energy. Default is 1.0.

    Attributes
    ----------
    position : {tuple, int}
        The position of the cell in the environment.
    modules : list
        List of modules that define the behavior of the cell.
    history : list
        List of historical values for the cell.
    metabolism_rate : float
        The rate at which the cell metabolizes energy.
    energy : float
        The energy level of the cell.

    Methods
    -------
    update()
        Update the cell's state.
    metabolize(factor)
        Metabolize energy based on a specified factor.
    """
    def __init__(self, position, metabolism_rate=1.0):
        super().__init__(position)
        self.metabolism_rate = metabolism_rate
        self.energy = 100.0

    def update(self, historical_value=None):
        """
        Update the cell's state based on its energy level.
        """
        super().update(self.energy)

    def metabolize(self, factor):
        """
        Metabolize energy based on a specified factor.
        """
        self.energy *= factor


class GeneRegulationCell(Cell):
    """
    A simple cell model that regulates gene expression levels based on external factors (e.g., signaling molecules).
    It is a subclass of the base Cell class.

    Parameters
    ----------
    position : {tuple, int}
        The position of the cell.
    gene_expression_level : float, optional
        The initial gene expression level. Default is 1.0.

    Attributes
    ----------
    position : {tuple, int}
        The position of the cell in the environment.
    modules : list
        List of modules that define the behavior of the cell.
    history : list
        List of historical values for the cell.
    gene_expression_level : float
        The gene expression level of the cell.

    Methods
    -------
    update()
        Update the cell's state.
    regulate_genes(regulation_factor)
        Regulate the cell's gene expression level by a specified factor.
    """
    def __init__(self, position, gene_expression_level=1.0):
        super().__init__(position)
        self.gene_expression_level = gene_expression_level

    def update(self, historical_value=None):
        """
        Update the cell's state based on its gene expression level.

        Parameters
        ----------
        historical_value : any, optional
            The historical value to append to the cell's history. Default is None.
        """
        super().update(self.gene_expression_level)

    def regulate_genes(self, regulation_factor):
        """
        Regulate the cell's gene expression level by a specified factor.

        Parameters
        ----------
        regulation_factor : float
            The factor by which to regulate the gene expression level.
        """
        self.gene_expression_level *= regulation_factor
