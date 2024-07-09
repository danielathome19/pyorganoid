try:
    import numpy as np
    import tensorflow as tf
    from .models import BaseMLModel
    from .modules import BaseMLModule


    class TFModel(BaseMLModel):
        """
        This adapter class represents a machine learning model implemented in Tensorflow/Keras.
        It is a subclass of the BaseMLModel class.
        The Tensorflow addon for pyorganoid must be installed using the pyorganoid[all] package or the command:
            pip install pyorganoid[tensorflow]

        Parameters
        ----------
        model_path : str
            The path to the Tensorflow/Keras model to use for prediction.
        input_shape : tuple, optional
            The input shape of the model. Default is None (infer from model if possible).

        Attributes
        ----------
        model : tf.keras.Model
            The Tensorflow/Keras model to use for prediction.
        input_shape : tuple
            The input shape of the model.

        Methods
        -------
        predict(input_data, verbose=False)
            Predict the output of the model given an input. Returns the predicted output.
        """
        def __init__(self, model_path, input_shape=None):
            self.model = tf.keras.models.load_model(model_path)
            self.input_shape = input_shape
            if self.input_shape is None and self.model.input_shape is not None and len(self.model.input_shape) > 0:
                self.input_shape = self.model.input_shape[1:]

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
            # Reshape input data to match model input shape as necessary (if possible)
            input_data = np.array(input_data)
            if self.input_shape is not None and input_data.shape != self.input_shape:
                input_data = input_data.reshape((1, *self.input_shape))  # .reshape((1, -1))
            return self.model.predict(input_data, verbose=verbose)


    class TFModule(BaseMLModule):
        pass
except ImportError:
    TFModel = None
    TFModule = None
