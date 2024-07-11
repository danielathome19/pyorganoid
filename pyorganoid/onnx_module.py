try:
    import numpy as np
    import onnxruntime as ort
    from .models import BaseMLModel
    from .modules import BaseMLModule


    class ONNXModel(BaseMLModel):
        """
        This adapter class represents a machine learning model implemented saved as an ONNX model.
        It is a subclass of the BaseMLModel class.
        The Tensorflow addon for pyorganoid must be installed using the pyorganoid[all] package or the command:
            pip install pyorganoid[onnx]

        Parameters
        ----------
        model_path : str
            The path to the ONNX model to use for prediction.
        input_shape : tuple, optional
            The input shape of the model. Default is None (infer from model if possible).
        data_type : str, optional
            The data type to use for input data. Default is 'float32'.

        Attributes
        ----------
        model : onnxruntime.InferenceSession
            The ONNX model to use for prediction.
        input_shape : tuple
            The input shape of the model.
        data_type : str
            The data type to use for input data.

        Methods
        -------
        predict(input_data, verbose=False)
            Predict the output of the model given an input. Returns the predicted output.
        """
        def __init__(self, model_path, input_shape=None, data_type='float32'):
            self.model = ort.InferenceSession(model_path)
            self.input_shape = input_shape
            if self.input_shape is None:
                self.input_shape = self.model.get_inputs()[0].shape
            self.data_type = data_type

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

            Raises
            ------
            ValueError
                If the input data shape does not match the model input shape (e.g., if the input_shape is 'None').
            """
            input_data = np.array(input_data, dtype=self.data_type)
            # Reshape input data to match model input shape as necessary (if possible)
            if self.input_shape is None:
                raise ValueError("Input shape must be specified for ONNX model")
            if self.input_shape is not None:
                input_data = input_data.reshape((1, *self.input_shape))
            return self.model.run(None, {self.model.get_inputs()[0].name: input_data})


    class ONNXModule(BaseMLModule):
        pass
except ImportError:
    ONNXModel = None
    ONNXModule = None
