import numpy as np


class BaseModule:
    """
    Base class for all modules (not to be instantiated directly).
    Modules are used to implement the logic of the agents in the simulation.
    Subclasses should implement the run method.

    Methods
    -------
    run(agent)
        Run the module on the given agent.
    """
    def __init__(self, *args, **kwargs):
        pass

    def run(self, agent):
        """
        Run the module on the given agent.

        Parameters
        ----------
        agent : Agent
            The agent to run the module on.
        """
        raise NotImplementedError("Subclasses should implement this method!")


class BaseMLModule(BaseModule):
    """
    Base class for machine learning modules (not to be instantiated directly).
    Subclasses should implement the collect_input_data (optionally) and apply_prediction methods.
    It is a subclass of the BaseModule class.

    Parameters
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.

    Attributes
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.

    Methods
    -------
    run(agent, verbose=False)
        Run the module on the given agent.
    collect_input_data(agent)
        Collect the input data for the machine learning model.
    apply_prediction(agent, prediction)
        Apply the prediction of the machine learning model to the agent.
    """
    def __init__(self, ml_model):
        super().__init__()
        self.ml_model = ml_model

    def run(self, agent, verbose=False):
        """
        Run the module on the given agent. Collects input data, makes a prediction, and applies it to the agent.

        Parameters
        ----------
        agent : Agent
            The agent to run the module on.
        verbose : bool, optional
            Whether to print verbose output. Default is False.
        """
        input_data = self.collect_input_data(agent)
        prediction = self.ml_model.predict(input_data, verbose=verbose)
        self.apply_prediction(agent, prediction)

    @staticmethod
    def collect_input_data(agent):
        """
        Collect the input data for the machine learning model.

        Parameters
        ----------
        agent : Agent
            The agent to collect input data from.

        Returns
        -------
        array-like
            The input data for the machine learning model.
        """
        return [agent.get_input_data(agent)]  # Default implementation, can be overridden

    def apply_prediction(self, agent, prediction):
        """
        Apply the prediction of the machine learning model to the agent.

        Parameters
        ----------
        agent : Agent
            The agent to apply the prediction to.
        prediction : array-like
            The prediction output of the machine learning model.

        Raises
        ------
        NotImplementedError
            If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses should implement this method!")

    def drop_prediction_dimensionality(self, prediction):
        """
        Drop the dimensionality of the prediction if necessary (e.g., from Tensorflow models).

        Parameters
        ----------
        prediction : array-like
            The prediction output of the machine learning model.

        Returns
        -------
        array-like
            The prediction output with reduced dimensionality.
        """
        try:
            from .tf_module import TFModel
            from .onnx_module import ONNXModel
            from .torch_module import TorchModel
            if isinstance(self.ml_model, TFModel):
                return prediction[0] if isinstance(prediction, list) and len(prediction) > 0 else prediction
            elif isinstance(self.ml_model, TorchModel):
                return prediction[0] if ((isinstance(prediction, list) or isinstance(prediction, np.ndarray))
                                         and len(prediction) > 0) else prediction
            elif isinstance(self.ml_model, ONNXModel):
                if isinstance(prediction, list) and len(prediction) > 0:
                    prediction = prediction[0]
                if isinstance(prediction, np.ndarray):
                    prediction = prediction.flatten().tolist()
                if isinstance(prediction, float) or isinstance(prediction, int):
                    return [prediction]
                return prediction
            else:
                return prediction
        except ImportError:
            return prediction


class SpikingNeuronModule(BaseMLModule):
    """
    Module for simulating a spiking neuron using a machine learning model.
    The module collects the membrane potential of the agent as input and
    applies the prediction to the membrane potential.
    It is a subclass of the BaseMLModule class.

    Parameters
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.

    Attributes
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.

    Methods
    -------
    run(agent, verbose=False)
        Run the module on the given agent.
    collect_input_data(agent)
        Collect the input data for the machine learning model.
    apply_prediction(agent, prediction)
        Apply the prediction of the machine learning model to the agent.
    """

    def apply_prediction(self, agent, prediction):
        """
        Apply the prediction of the machine learning model to the agent.
        Adds the prediction to the membrane potential of the agent (neuron).

        Parameters
        ----------
        agent : Agent
            The agent to apply the prediction to.
        prediction : array-like
            The prediction output of the machine learning model.
        """
        prediction = self.drop_prediction_dimensionality(prediction)
        agent.membrane_potential += prediction[0]


class GrowthShrinkageModule(BaseMLModule):
    """
    Module for simulating growth and shrinkage of cells using a machine learning model.
    The module collects the volume of the agent as input and applies the prediction to the volume.
    It is a subclass of the BaseMLModule class.

    Parameters
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.
    growth_amount : float, optional
        The amount by which the cells grow at each time step. Default is 0.1.
    growth_variance : float, optional
        The variance of the growth amount. Default is 0.05.
    prediction_threshold : float, optional
        The threshold above which the cells grow and below which they shrink. Default is 0.5.

    Attributes
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.
    growth_amount : float, optional
        The amount by which the cells grow at each time step.
    growth_variance : float, optional
        The variance of the growth amount.
    prediction_threshold : float, optional
        The threshold above which the cells grow and below which they shrink.

    Methods
    -------
    run(agent, verbose=False)
        Run the module on the given agent.
    collect_input_data(agent)
        Collect the input data for the machine learning model.
    apply_prediction(agent, prediction)
        Apply the prediction of the machine learning model to the agent.
    """
    def __init__(self, ml_model, growth_amount=0.1, growth_variance=0.05, prediction_threshold=0.5):
        super().__init__(ml_model)
        self.growth_amount = growth_amount
        self.growth_variance = growth_variance
        self.prediction_threshold = prediction_threshold

    def apply_prediction(self, agent, prediction):
        """
        Apply the prediction of the machine learning model to the agent.
        If the prediction is greater than 0.5, the agent (cell) grows; otherwise, it shrinks.

        Parameters
        ----------
        agent : Agent
            The agent to apply the prediction to.
        prediction : array-like
            The prediction output of the machine learning model.
        """
        prediction = self.drop_prediction_dimensionality(prediction)
        change = self.growth_amount + np.random.uniform(-self.growth_variance, self.growth_variance)
        if prediction[0] > 0.5:
            agent.grow(change)
        else:
            agent.shrink(change)


class DifferentiationModule(BaseMLModule):
    """
    Module for simulating differentiation of cells (such as in a Neural Network) using a machine learning model.
    The module collects the state of the agent as input and applies the prediction to the state.
    It is a subclass of the BaseMLModule class.

    Parameters
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.

    Attributes
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.

    Methods
    -------
    run(agent, verbose=False)
        Run the module on the given agent.
    collect_input_data(agent)
        Collect the input data for the machine learning model.
    apply_prediction(agent, prediction)
        Apply the prediction of the machine learning model to the agent.
    """

    def apply_prediction(self, agent, prediction):
        """
        Apply the prediction of the machine learning model to the agent.
        Differentiates the agent (cell) based on the prediction.

        Parameters
        ----------
        agent : Agent
            The agent to apply the prediction to.
        prediction : array-like
            The prediction output of the machine learning model.
        """
        prediction = self.drop_prediction_dimensionality(prediction)
        agent.differentiate(prediction[0])


class ChemotaxisModule(BaseMLModule):
    """
    Module for simulating chemotaxis of cells using a machine learning model.
    The module collects the chemotactic gradient of the agent as input and applies the prediction to the gradient.
    It is a subclass of the BaseMLModule class.

    Parameters
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.

    Attributes
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.

    Methods
    -------
    run(agent, verbose=False)
        Run the module on the given agent.
    collect_input_data(agent)
        Collect the input data for the machine learning model.
    apply_prediction(agent, prediction)
        Apply the prediction of the machine learning model to the agent.
    """

    def apply_prediction(self, agent, prediction):
        """
        Apply the prediction of the machine learning model to the agent.
        Moves the agent (cell) towards the predicted gradient.

        Parameters
        ----------
        agent : Agent
            The agent to apply the prediction to.
        prediction : array-like
            The prediction output of the machine learning model.
        """
        prediction = self.drop_prediction_dimensionality(prediction)
        agent.move_towards_gradient(prediction[0])


class ImmuneResponseModule(BaseMLModule):
    """
    Module for simulating an immune response using a machine learning model.
    The module collects whether the agent is active or not as input and applies the prediction to the agent.
    It is a subclass of the BaseMLModule class.

    Parameters
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.

    Attributes
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.

    Methods
    -------
    run(agent, verbose=False)
        Run the module on the given agent.
    collect_input_data(agent)
        Collect the input data for the machine learning model.
    apply_prediction(agent, prediction)
        Apply the prediction of the machine learning model to the agent.
    """

    def apply_prediction(self, agent, prediction):
        """
        Apply the prediction of the machine learning model to the agent.
        Activates or deactivates the agent based on the prediction.

        Parameters
        ----------
        agent : Agent
            The agent to apply the prediction to.
        prediction : array-like
            The prediction output of the machine learning model.
        """
        prediction = self.drop_prediction_dimensionality(prediction)
        if prediction[0] > 0.5:
            agent.activate()
        else:
            agent.deactivate()


class SynapticPlasticityModule(BaseMLModule):
    """
    Module for simulating spike-timing-dependent plasticity (STDP) in a synapse (e.g., in a physical neural network).
    The module updates the synaptic weight based on the pre- and post-synaptic spikes.
    It is a subclass of the BaseMLModule class.

    Parameters
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.
    synapse : Synapse
        The synapse to update.
    learning_rate : float, optional
        The learning rate for updating the synaptic weight. Default is 0.01.

    Attributes
    ----------
    synapse : Synapse
        The synapse to update.
    learning_rate : float
        The learning rate for updating the synaptic weight.

    Methods
    -------
    run(agent)
        Run the module on the given agent.

    """
    def __init__(self, ml_model, synapse, learning_rate=0.01):
        super().__init__(ml_model)
        self.synapse = synapse
        self.learning_rate = learning_rate

    def run(self, agent):
        pre_spike = self.synapse.pre_neuron.membrane_potential >= self.synapse.pre_neuron.threshold
        post_spike = self.synapse.post_neuron.membrane_potential >= self.synapse.post_neuron.threshold

        if pre_spike and post_spike:
            self.synapse.weight += self.learning_rate * (1 - self.synapse.weight)
        elif pre_spike and not post_spike:
            self.synapse.weight -= self.learning_rate * self.synapse.weight

    def apply_prediction(self, agent, prediction):
        """
        Apply the prediction of the machine learning model to the agent.
        Adds the prediction to the membrane potential of the agent (neuron).

        Parameters
        ----------
        agent : Agent
            The agent to apply the prediction to.
        prediction : array-like
            The prediction output of the machine learning model.
        """
        prediction = self.drop_prediction_dimensionality(prediction)
        agent.membrane_potential += prediction[0]


class MetabolicModule(BaseMLModule):
    """
    Module for simulating metabolism in cells using a machine learning model.
    The module collects the energy level of the agent as input and applies the prediction to the agent.
    It is a subclass of the BaseMLModule class.

    Parameters
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.

    Attributes
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.

    Methods
    -------
    run(agent, verbose=False)
        Run the module on the given agent.
    collect_input_data(agent)
        Collect the input data for the machine learning model.
    apply_prediction(agent, prediction)
        Apply the prediction of the machine learning model to the agent.
    """

    def apply_prediction(self, agent, prediction):
        """
        Apply the prediction of the machine learning model to the agent.
        Metabolizes the agent based on the prediction.

        Parameters
        ----------
        agent : Agent
            The agent to apply the prediction to.
        prediction : array-like
            The prediction output of the machine learning model.
        """
        metabolism_factor = prediction[0]
        agent.metabolize(metabolism_factor)


class GeneRegulationModule(BaseMLModule):
    """
    Module for simulating gene regulation in cells using a machine learning model.
    The module collects the gene expression level of the agent as input and applies the prediction to the agent.
    It is a subclass of the BaseMLModule class.

    Parameters
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.

    Attributes
    ----------
    ml_model : BaseMLModel
        The machine learning model to use for prediction.

    Methods
    -------
    run(agent, verbose=False)
        Run the module on the given agent.
    collect_input_data(agent)
        Collect the input data for the machine learning model.
    apply_prediction(agent, prediction)
        Apply the prediction of the machine learning model to the agent.
    """

    def apply_prediction(self, agent, prediction):
        """
        Apply the prediction of the machine learning model to the agent.
        Regulates the genes of the agent based on the prediction.

        Parameters
        ----------
        agent : Agent
            The agent to apply the prediction to.
        prediction : array-like
            The prediction output of the machine learning model.
        """
        prediction = self.drop_prediction_dimensionality(prediction)
        regulation_factor = prediction[0]
        scaled_factor = 0.5 + regulation_factor  # Scale regulation_factor from [0, 1] to [0.5, 1.5]
        print(f"Regulation factor: {scaled_factor}")
        agent.regulate_genes(scaled_factor)
