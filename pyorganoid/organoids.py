import numpy as np
from .cells import *
from .modules import *
from .base import Organoid, Synapse
from .utils import generate_random_position


class SpikingNeuronOrganoid(Organoid):
    """
    This class represents an organoid composed of spiking neurons. It is a subclass of the base Organoid class.

    Parameters
    ----------
    environment : Environment
        The environment in which the organoid resides.
    ml_model : BaseMLModel
        The machine learning model used by the spiking neuron modules.
    num_cells : int, optional
        The number of spiking neurons in the organoid. Default is 10.
    input_data_func : callable, optional
        A function that generates input data for the spiking neurons. Defaults to '() => [0.5] * 10' if None.
    """
    def __init__(self, environment, ml_model, num_cells=10, input_data_func=None):
        super().__init__(environment)
        for i in range(num_cells):
            neuron = SpikingNeuronCell(position=generate_random_position(environment.dimensions, environment.size),
                                       input_data_func=input_data_func)
            neuron.add_module(SpikingNeuronModule(ml_model))
            self.add_agent(neuron)


class GrowthShrinkageOrganoid(Organoid):
    """
    This class represents an organoid composed of cells that grow and shrink based on machine learning predictions.
    It is a subclass of the base Organoid class.

    Parameters
    ----------
    environment : Environment
        The environment in which the organoid resides.
    ml_model : BaseMLModel
        The machine learning model used by the growth/shrinkage cell modules.
    num_cells : int, optional
        The number of growth/shrinkage cells in the organoid. Default is 10.
    initial_cell_volume : float, optional
        The initial volume of the cells. Default is 1.0. Use "None" for random volumes in the range [0.5, 1.5].
    growth_amount : float, optional
        The amount by which the cells grow at each time step. Default is 0.1.
    growth_variance : float, optional
        The variance of the growth amount. Default is 0.05.
    prediction_threshold : float, optional
        The threshold above which the cells grow and below which they shrink. Default is 0.5.
    """
    def __init__(self, environment, ml_model, num_cells=10, initial_cell_volume=1.0,
                 growth_amount=0.1, growth_variance=0.05, prediction_threshold=0.5):
        super().__init__(environment)
        for i in range(num_cells):
            initial_volume = initial_cell_volume if initial_cell_volume is not None else np.random.uniform(0.5, 1.5)
            cell = GrowthShrinkageCell(position=generate_random_position(environment.dimensions, environment.size),
                                       initial_volume=initial_volume)
            cell.add_module(GrowthShrinkageModule(ml_model, growth_amount, growth_variance, prediction_threshold))
            self.add_agent(cell)


class DifferentiationOrganoid(Organoid):
    """
    This class represents an organoid composed of differentiating (e.g., neural network) cells.
    It is a subclass of the base Organoid class.

    Parameters
    ----------
    environment : Environment
        The environment in which the organoid resides.
    ml_model : BaseMLModel
        The machine learning model used by the differentiating cell modules.
    num_cells : int, optional
        The number of differentiating cells in the organoid. Default is 10.
    """
    def __init__(self, environment, ml_model, num_cells=10):
        super().__init__(environment)
        for i in range(num_cells):
            cell = DifferentiatingCell(position=generate_random_position(environment.dimensions, environment.size))
            cell.add_module(DifferentiationModule(ml_model))
            self.add_agent(cell)


class ChemotaxisOrganoid(Organoid):
    """
    This class represents an organoid composed of chemotactic cells. It is a subclass of the base Organoid class.

    Parameters
    ----------
    environment : Environment
        The environment in which the organoid resides.
    ml_model : BaseMLModel
        The machine learning model used by the chemotactic cell modules.
    num_cells : int, optional
        The number of chemotactic cells in the organoid. Default is 10.
    """
    def __init__(self, environment, ml_model, num_cells=10):
        super().__init__(environment)
        for i in range(num_cells):
            cell = ChemotacticCell(position=generate_random_position(environment.dimensions, environment.size))
            cell.add_module(ChemotaxisModule(ml_model))
            self.add_agent(cell)


class ImmuneResponseOrganoid(Organoid):
    """
    This class represents an organoid composed of immune cells that respond to external stimuli.
    It is a subclass of the base Organoid class.

    Parameters
    ----------
    environment : Environment
        The environment in which the organoid resides.
    ml_model : BaseMLModel
        The machine learning model used by the immune cell modules.
    num_cells : int, optional
        The number of immune cells in the organoid. Default is 10.
    """
    def __init__(self, environment, ml_model, num_cells=10):
        super().__init__(environment)
        for i in range(num_cells):
            cell = ImmuneCell(position=generate_random_position(environment.dimensions, environment.size))
            cell.add_module(ImmuneResponseModule(ml_model))
            self.add_agent(cell)


class SynapticPlasticityOrganoid(Organoid):
    """
    This class represents an organoid composed of neurons with synaptic plasticity (STDP).
    It is a subclass of the base Organoid class.

    Parameters
    ----------
    environment : Environment
        The environment in which the organoid resides.
    ml_model : BaseMLModel
        The machine learning model used by the synaptic plasticity cell modules.
    num_cells : int, optional
        The number of synaptic plasticity cells (i.e., neurons) in the organoid. Default is 10.
    num_synapses : int, optional
        The number of synapses connecting the plasticity cells. Default is 5.
    """
    def __init__(self, environment, ml_model, num_cells=10, num_synapses=5):
        super().__init__(environment)
        for i in range(num_cells):
            cell = SynapticPlasticityCell(position=generate_random_position(environment.dimensions, environment.size))
            cell.add_module(SynapticPlasticityModule(ml_model))
            self.add_agent(cell)

        for _ in range(num_synapses):
            pre_cell, post_cell = np.random.choice(self.agents, 2, replace=False)
            synapse = Synapse(pre_neuron=pre_cell, post_neuron=post_cell)
            pre_cell.add_synapse(synapse)
            post_cell.add_module(SynapticPlasticityModule(synapse))


class MetabolicOrganoid(Organoid):
    """
    This class represents an organoid composed of cells with metabolic modules.
    It is a subclass of the base Organoid class.

    Parameters
    ----------
    environment : Environment
        The environment in which the organoid resides.
    ml_model : BaseMLModel
        The machine learning model used by the metabolic cell modules.
    num_cells : int, optional
        The number of metabolic cells in the organoid. Default is 10.
    """
    def __init__(self, environment, ml_model, num_cells=10):
        super().__init__(environment)
        for i in range(num_cells):
            cell = MetabolicCell(position=generate_random_position(environment.dimensions, environment.size))
            cell.add_module(MetabolicModule(ml_model))
            self.add_agent(cell)


class GeneRegulationOrganoid(Organoid):
    """
    This class represents an organoid composed of cells with gene regulation modules.
    It is a subclass of the base Organoid class.
    NOTE: In the future, this class could be extended to include sequence data and gene expression profiles.

    Parameters
    ----------
    environment : Environment
        The environment in which the organoid resides.
    ml_model : BaseMLModel
        The machine learning model used by the gene regulation cell modules.
    num_cells : int, optional
        The number of gene regulation cells in the organoid. Default is 10.
    """
    def __init__(self, environment, ml_model, num_cells=10):
        super().__init__(environment)
        for i in range(num_cells):
            cell = GeneRegulationCell(position=generate_random_position(environment.dimensions, environment.size))
            cell.add_module(GeneRegulationModule(ml_model))
            self.add_agent(cell)
