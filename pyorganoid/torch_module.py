try:
    import torch
    import torch.nn as nn
    from .models import BaseMLModel
    from .modules import BaseMLModule


    class TorchModel(BaseMLModel):
        """
        This adapter class represents a machine learning model implemented in PyTorch.
        It is a subclass of the BaseMLModel class.
        The PyTorch addon for pyorganoid must be installed using the pyorganoid[all] package or the command:
            pip install pyorganoid[torch]

        Parameters
        ----------
        model_path : str
            The path to the PyTorch model to use for prediction.
        input_shape : tuple, optional
            The input shape of the model. Default is None (infer from model if possible).


        Attributes
        ----------
        model : torch.nn.Module
            The PyTorch model to use for prediction.

        Methods
        -------
        predict(input_data, verbose=False)
            Predict the output of the model given an input. Returns the predicted output.
        """
        def __init__(self, model_path, input_shape=None):
            self.model = torch.load(model_path)
            self.model.eval()
            self.input_shape = input_shape
            if self.input_shape is None:
                self.input_shape = self.__get_input_shape()

        def predict(self, input_data, verbose=False):
            """
            Predict the output of the model given an input.

            Parameters
            ----------
            input_data : array-like
                The input data for the model.
            verbose : bool, optional
                Whether to print verbose output. Default is False.

            Returns
            -------
            array-like
                The output of the model given the input data.
            """
            with torch.no_grad():
                input_tensor = torch.tensor(input_data).float().unsqueeze(0)
                output = self.model(input_tensor)
                return output.numpy()

        def __get_input_shape(self):
            """
            Attempt to determine the input shape of the model.

            Returns
            -------
            tuple
                The input shape of the model.
            """
            try:
                if hasattr(self.model, 'input_shape'):
                    return self.model.input_shape
                else:
                    # Attempt to determine the input shape from the first layer
                    for module in self.model.modules():
                        if isinstance(module, (nn.Linear, nn.Conv2d)):
                            return module.in_features if isinstance(module, nn.Linear) else module.in_channels,
                    raise ValueError("Unable to determine input shape from the model")
            except Exception:
                return None

    class TorchModule(BaseMLModule):
        pass
except ImportError:
    TFModel = None
    TFModule = None
