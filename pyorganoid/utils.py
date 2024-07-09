import numpy as np


def generate_random_position(dimensions, size):
    """
    Generate a random position in the given dimensions and size.

    Parameters
    ----------
    dimensions : int
        The number of dimensions.
    size : float
        The size of the space.

    Returns
    -------
    np.ndarray
        A random position in the given dimensions
    """
    return np.random.rand(dimensions) * size
