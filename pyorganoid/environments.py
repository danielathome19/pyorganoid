import numpy as np


class Environment:
    """
    Base class for environments. Environments can have conditions that change over time.
    Conditions are objects that have an update method.

    Parameters
    ----------
    dimensions : int, optional
        The number of dimensions of the environment. Default is 3.
    size : float, optional
        The size of the environment. Default is 100.0.

    Attributes
    ----------
    conditions : list
        List of conditions in the environment.
    dimensions : int
        The number of dimensions of the environment.
    size : float
        The size of the environment.

    Methods
    -------
    update()
        Update the environment.
    add_condition(condition)
        Add a condition to the environment
    """
    def __init__(self, dimensions=3, size=100.0):
        self.conditions = []
        self.dimensions = dimensions
        self.size = size

    def update(self):
        """
        Update the environment.
        This method calls the update method of all conditions in the environment.
        """
        for condition in self.conditions:
            condition.update()

    def add_condition(self, condition):
        """
        Add a condition to the environment.

        Parameters
        ----------
        condition : object
            The condition to add to the environment.
        """
        self.conditions.append(condition)


class GradientEnvironment(Environment):
    """
    Environment with a gradient that can be used by agents to navigate.
    It is a subclass of the base Environment class.

    Parameters
    ----------
    gradient_func : function
        The function that calculates the gradient at a given position.
    dimensions : int, optional
        The number of dimensions of the environment. Default is 3.
    size : float, optional
        The size of the environment. Default is 100.0.

    Attributes
    ----------
    conditions : list
        List of conditions in the environment.
    dimensions : int, optional
        The number of dimensions of the environment.
    size : float, optional
        The size of the environment.
    gradient_func : function
        The function that calculates the gradient at a given position.

    Methods
    -------
    update()
        Update the environment.
    add_condition(condition)
        Add a condition to the environment
    get_gradient(position)
        Get the gradient at a given position.
    """
    def __init__(self, gradient_func, dimensions=3, size=100.0):
        super().__init__(dimensions, size)
        self.gradient_func = gradient_func

    def get_gradient(self, position):
        """
        Get the gradient at a given position.

        Parameters
        ----------
        position : array-like
            The position at which to calculate the gradient.

        Returns
        -------
        array-like
            The gradient at the given position.
        """
        return self.gradient_func(position)


class TemperatureEnvironment(Environment):
    """
    Environment with a temperature that can change over time.
    It is a subclass of the base Environment class.

    Parameters
    ----------
    initial_temperature : float
        The initial temperature of the environment.
    temperature_range : tuple, optional
        The range of temperatures that the environment can have. Default is None.
    dimensions : int, optional
        The number of dimensions of the environment. Default is 3.
    size : float, optional
        The size of the environment. Default is 100.0.

    Attributes
    ----------
    conditions : list
        List of conditions in the environment.
    dimensions : int, optional
        The number of dimensions of the environment. Default is 3.
    size : float, optional
        The size of the environment. Default is 100.0.
    temperature : float
        The temperature of the environment.
    temperature_range : tuple
        The range of temperatures that the environment can have (optional).

    Methods
    -------
    update()
        Update the environment.
    add_condition(condition)
        Add a condition to the environment
    get_temperature()
        Get the temperature of the environment.
    set_temperature(temperature)
        Set the temperature of the environment.
    """
    def __init__(self, initial_temperature, temperature_range=None, dimensions=3, size=100.0):
        super().__init__(dimensions, size)
        self.temperature = initial_temperature
        self.temperature_range = temperature_range

    def update(self):
        """
        Update the environment.
        This method updates the temperature of the environment if a temperature range is specified.
        """
        if self.temperature_range is not None:
            self.temperature = np.random.uniform(*self.temperature_range)
        super().update()

    def get_temperature(self):
        """
        Get the temperature of the environment.

        Returns
        -------
        float
            The temperature of the environment.
        """
        return self.temperature

    def set_temperature(self, temperature):
        """
        Set the temperature of the environment.

        Parameters
        ----------
        temperature : float
            The temperature to set
        """
        self.temperature = temperature


class StochasticEnvironment(Environment):
    """
    Environment with a stochastic noise level that can change over time.
    It is a subclass of the base Environment class.

    Parameters
    ----------
    noise_level : float
        The noise level of the environment
    dimensions : int, optional
        The number of dimensions of the environment. Default is 3.
    size : float, optional
        The size of the environment. Default is 100.0.

    Attributes
    ----------
    conditions : list
        List of conditions in the environment.
    dimensions : int, optional
        The number of dimensions of the environment.
    size : float, optional
        The size of the environment.
    noise_level : float
        The noise level of the environment.

    Methods
    -------
    update()
        Update the environment.
    add_condition(condition)
        Add a condition to the environment
    get_noise()
        Get the noise level of the environment.
    """
    def __init__(self, noise_level, dimensions=3, size=100.0):
        super().__init__(dimensions, size)
        self.noise_level = noise_level

    def get_noise(self):
        """
        Get the noise level of the environment.

        Returns
        -------
        float
            The noise level of the environment.
        """
        return np.random.normal(0, self.noise_level)


class ChemicalGradientEnvironment(Environment):
    """
    Environment with a chemical gradient that can be used by agents to navigate.
    It is a subclass of the base Environment class.

    Parameters
    ----------
    gradient_func : function
        The function that calculates the gradient at a given position. Default is np.linalg.norm.
    dimensions : int, optional
        The number of dimensions of the environment. Default is 3.
    size : float, optional
        The size of the environment. Default is 100.0.

    Attributes
    ----------
    conditions : list
        List of conditions in the environment.
    dimensions : int, optional
        The number of dimensions of the environment.
    size : float, optional
        The size of the environment.
    gradient_func : function
        The function that calculates the gradient at a given position.

    Methods
    -------
    update()
        Update the environment.
    add_condition(condition)
        Add a condition to the environment
    get_concentration(position)
        Get the concentration of the chemical at a given position.
    """
    def __init__(self, gradient_func=np.linalg.norm, dimensions=3, size=100.0):
        super().__init__(dimensions, size)
        self.gradient_func = gradient_func

    def get_concentration(self, position):
        """
        Get the concentration of the chemical at a given position.

        Parameters
        ----------
        position : array-like
            The position at which to calculate the concentration.
        """
        return self.gradient_func(position)


class ElectricFieldEnvironment(Environment):
    """
    Environment with an electric field that can be used by agents to navigate.
    It is a subclass of the base Environment class.

    Parameters
    ----------
    field_strength : float
        The strength of the electric field.
    dimensions : int, optional
        The number of dimensions of the environment. Default is 3.
    size : float, optional
        The size of the environment. Default is 100.0.

    Attributes
    ----------
    conditions : list
        List of conditions in the environment.
    dimensions : int, optional
        The number of dimensions of the environment.
    size : float, optional
        The size of the environment.
    field_strength : float
        The strength of the electric field.

    Methods
    -------
    update()
        Update the environment.
    add_condition(condition)
        Add a condition to the environment
    get_field_effect(position)
        Get the effect of the electric field at a given position.
    """
    def __init__(self, field_strength, dimensions=3, size=100.0):
        super().__init__(dimensions, size)
        self.field_strength = field_strength

    def get_field_effect(self, position):
        """
        Get the effect of the electric field at a given position.

        Parameters
        ----------
        position : array-like
            The position at which to calculate the field effect.
        """
        return self.field_strength * position  # May be overridden in subclasses for more complex behavior
