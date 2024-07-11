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
        model_class : type[torch.nn.Module]
            The PyTorch model class to use for prediction.
        input_shape : tuple, optional
            The input shape of the model. Default is None (infer from model if possible).

        Attributes
        ----------
        model : torch.nn.Module
            The PyTorch model to use for prediction.
        input_shape : tuple
            The input shape of the model.

        Methods
        -------
        predict(input_data, verbose=False)
            Predict the output of the model given an input. Returns the predicted output.

        Raises
        ------
        ValueError
            If the model_class is not provided or is None.
        """
        def __init__(self, model_path, model_class, input_shape=None):
            if model_class is None:
                raise ValueError("You must provide a model_class to load the model.")
            self.input_shape = input_shape
            if self.input_shape is None:
                self.input_shape = self.__get_input_shape()
            self.model = model_class(input_shape[0])
            self.model.load_state_dict(torch.load(model_path))
            self.model.eval()

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
                # input_tensor = torch.tensor(input_data).float().unsqueeze(0)
                # Reshape input data to match model input shape as necessary (if possible)
                input_tensor = torch.tensor(input_data).float()
                if self.input_shape is not None:
                    input_tensor = input_tensor.view(1, *self.input_shape)
                output = self.model(input_tensor)
                return output.numpy()

        def __get_input_shape(self):
            """
            Attempt to determine the input shape of the model.

            Returns
            -------
            tuple
                The input shape of the model.

            Raises
            ------
            ValueError
                If the input shape cannot be determined from the model.
                If this occurs, you must provide the input_shape manually when creating the TorchModel instance.
            """
            if hasattr(self.model, 'input_shape'):
                return self.model.input_shape
            else:
                # Attempt to determine the input shape from the first layer
                for module in self.model.modules():
                    if isinstance(module, (nn.Linear, nn.Conv2d)):
                        return module.in_features if isinstance(module, nn.Linear) else module.in_channels,
                raise ValueError("Unable to determine input shape from the model. Please provide input_shape manually.")


    class TorchModule(BaseMLModule):
        pass
except ImportError:
    TFModel = None
    TFModule = None
