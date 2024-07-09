try:
    import joblib
    import sklearn
    import numpy as np
    from .models import BaseMLModel
    from .modules import BaseMLModule


    class SklearnModel(BaseMLModel):
        """
        This adapter class represents a machine learning model implemented in scikit-learn.
        It is a subclass of the BaseMLModel class.
        The scikit-learn addon for pyorganoid must be installed using the pyorganoid[all] package or the command:
            pip install pyorganoid[sklearn]

        Parameters
        ----------
        model_path : str
            The path to the scikit-learn model to use for prediction.
        num_features : int, optional
            The number of features expected by the model. Default is None (infer from model if possible).

        Attributes
        ----------
        model : sklearn.base.BaseEstimator
            The scikit-learn model to use for prediction.
        input_shape : tuple
            The number of features expected by the model.

        Methods
        -------
        predict(input_data, verbose=False)
            Predict the output of the model given an input. Returns the predicted output.
        """

        def __init__(self, model_path, num_features=None):
            self.model = joblib.load(model_path)
            self.input_shape = (num_features,)
            if self.input_shape is None and hasattr(self.model, 'n_features_in_'):
                self.input_shape = (self.model.n_features_in_,)

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
            input_data = np.array(input_data).reshape((1, -1))
            return self.model.predict(input_data)


    class SklearnModule(BaseMLModule):
        pass
except ImportError:
    TFModel = None
    TFModule = None
