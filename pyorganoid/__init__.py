from .base import Agent, Cell, Synapse, Organoid
from .models import BaseMLModel
from .cells import (
    SpikingNeuronCell, GrowthShrinkageCell, DifferentiatingCell, ChemotacticCell,
    ImmuneCell, SynapticPlasticityCell, MetabolicCell, GeneRegulationCell
)
from .modules import (
    BaseModule, BaseMLModule, SpikingNeuronModule, GrowthShrinkageModule, DifferentiationModule, ChemotaxisModule,
    ImmuneResponseModule, SynapticPlasticityModule, MetabolicModule, GeneRegulationModule
)
from .organoids import (
    SpikingNeuronOrganoid, GrowthShrinkageOrganoid, DifferentiationOrganoid, ChemotaxisOrganoid,
    ImmuneResponseOrganoid, SynapticPlasticityOrganoid, MetabolicOrganoid, GeneRegulationOrganoid
)
from .environments import (
    Environment, GradientEnvironment, TemperatureEnvironment, StochasticEnvironment,
    ChemicalGradientEnvironment, ElectricFieldEnvironment
)
from .simulation import Scheduler, StochasticScheduler, PriorityScheduler, ParallelScheduler
from .agents import AgentContainer, AgentHandle
from .utils import generate_random_position
# TODO: bioinformatics and cheminformatics modules/importing, e.g. sequence alignment, molecular docking, etc.;
#       parallel/distributed scheduling; logging; visualization; etc.


__all__ = [
    'Agent', 'Cell', 'Synapse', 'Organoid',
    'SpikingNeuronCell', 'GrowthShrinkageCell', 'DifferentiatingCell', 'ChemotacticCell', 'ImmuneCell', 'SynapticPlasticityCell', 'MetabolicCell', 'GeneRegulationCell',
    'SpikingNeuronOrganoid', 'GrowthShrinkageOrganoid', 'DifferentiationOrganoid', 'ChemotaxisOrganoid', 'ImmuneResponseOrganoid', 'SynapticPlasticityOrganoid', 'MetabolicOrganoid', 'GeneRegulationOrganoid',
    'BaseModule', 'SpikingNeuronModule', 'GrowthShrinkageModule', 'DifferentiationModule', 'ChemotaxisModule', 'ImmuneResponseModule', 'SynapticPlasticityModule', 'MetabolicModule', 'GeneRegulationModule',
    'BaseMLModel',
    'Environment', 'GradientEnvironment', 'TemperatureEnvironment', 'StochasticEnvironment', 'ChemicalGradientEnvironment', 'ElectricFieldEnvironment',
    'Scheduler', 'StochasticScheduler', 'PriorityScheduler', 'ParallelScheduler',
    'AgentContainer', 'AgentHandle',
    'generate_random_position',
    # Conditional inclusion based on availability of required packages
    'TFModel', 'TFModule',
    'TorchModel', 'TorchModule',
    'SklearnModel', 'SklearnModule',
    'ONNXModel', 'ONNXModule',
]


try:
    from .tf_module import TFModel, TFModule
except ImportError:
    TFModel = None
    TFModule = None


try:
    from .torch_module import TorchModel, TorchModule
except ImportError:
    TorchModel = None
    TorchModule = None


try:
    from .sklearn_module import SklearnModel, SklearnModule
except ImportError:
    SklearnModel = None
    SklearnModule = None


try:
    from .onnx_module import ONNXModel, ONNXModule
except ImportError:
    ONNXModel = None
    ONNXModule = None


globals().update({
    "TFModel": TFModel,
    "TFModule": TFModule,
    "ONNXModel": ONNXModel,
    "ONNXModule": ONNXModule,
    "TorchModel": TorchModel,
    "TorchModule": TorchModule,
    "SklearnModel": SklearnModel,
    "SklearnModule": SklearnModule,
})
