class BaseMLModel:
    """
    This is the base adapter class for machine learning models used in pyorganoid (not to be instantiated directly).
    Subclasses should implement the predict method.

    Methods
    -------
    predict(input_data, verbose=False)
        Predict the output of the model given an input.
    """
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
        NotImplementedError
            If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses should implement this method!")
