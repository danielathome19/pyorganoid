<h1 align="center">
    <img src="https://github.com/danielathome19/pyorganoid/blob/main/.github/images/logo_hero.png?raw=true" width="400" alt="Pyorganoid Logo" style="max-width:100%;">
</h1>

[![PyPI Downloads](https://img.shields.io/pypi/dm/pyorganoid.svg?label=PyPI%20downloads)](
https://pypi.org/project/pyorganoid/)
[![Conda Downloads](https://img.shields.io/conda/dn/danielathome19/pyorganoid.svg?label=Conda%20downloads)](
https://anaconda.org/danielathome19/pyorganoid)
[![CI/CT/CD](https://github.com/danielathome19/pyorganoid/actions/workflows/package_upload.yml/badge.svg)](https://github.com/danielathome19/pyorganoid/actions/workflows/package_upload.yml)
[![License](https://img.shields.io/badge/license-BSD_3_Clause-blue)](./LICENSE.md)
<!--[![Research Paper](https://img.shields.io/badge/DOI-10)](
https://DOI_LINK_HERE)-->


Pyorganoid is the world's first<sup>*</sup> Python package for the simulation of organoids for the purpose of studying 
Organoid Intelligence (OI) and Organoid Learning (OL).
It is designed to be simple to use and easy to extend with support for standard machine
learning libraries such as TensorFlow, PyTorch, and Scikit-Learn (as well as ONNX-format models).

<!-- - **Website:** https://danielathome19.github.io/pyorganoid/ -->
- **Documentation:** https://danielathome19.github.io/pyorganoid/docs/
- **Source code:** https://github.com/danielathome19/pyorganoid
- **Bug reports:** https://github.com/danielathome19/pyorganoid/issues
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

It provides:

- a simple and intuitive API
- support for standard machine learning libraries
- a growing library of organoid models
- visualization tools for organoid simulation
- numerous simulation environments and scheduling algorithms
- TODO: *support for parallel/distributed computing, bio/cheminformatics libraries, logging, and more*

Pyorganoid is currently in development and may not yet be ready for production use. We are actively seeking contributors
to help us improve the package and expand its capabilities. If you are interested in contributing, please see our
[contributing guide](CONTRIBUTING.md).

<p style="font-size: 6px"><sup>*</sup>As of July 6th, 2024, to the best of our knowledge :)</p>


<img src="https://github.com/danielathome19/pyorganoid/blob/main/.github/images/spiking_organoid.png?raw=true" style="width:100%;" align="center" alt="Organoid Example">


## Installation


### Pip

Pyorganoid can be installed (without built-in support for machine learning libraries) using `pip`:

```bash
pip install pyorganoid
```

To include support for all machine learning libraries, use:

```bash
pip install pyorganoid[all]
```

Or, to include support for a specific library (TensorFlow, PyTorch, Scikit-Learn, or ONNX), use:

```bash
pip install pyorganoid[tensorflow]
pip install pyorganoid[torch]
pip install pyorganoid[sklearn]
pip install pyorganoid[onnx]
```


### Conda

Pyorganoid can also be installed using `conda`:

```bash
conda install -c danielathome19 pyorganoid
```

To include support for all machine learning libraries, use:

```bash
conda install -c danielathome19 pyorganoid-all
```

Or, to include support for a specific library (TensorFlow, PyTorch, Scikit-Learn, or ONNX), use:

```bash
conda install -c danielathome19 pyorganoid-tensorflow
conda install -c danielathome19 pyorganoid-torch
conda install -c danielathome19 pyorganoid-sklearn
conda install -c danielathome19 pyorganoid-onnx
```


## Quickstart

For a quick introduction to Pyorganoid, see the [Spiking Neuron Test](tests/test_spiking.py) in the `test` directory.
This test demonstrates the creation of a simple spiking neuron organoid running a binary classification Multi-Layer
Perceptron (MLP) model using TensorFlow.

If you prefer Scikit-Learn, PyTorch, or ONNX models, see the [Volumetric Organoid Test (Scikit-Learn)](tests/test_growshrink.py),
the [Gene Regulation Organoid Test (PyTorch)](tests/test_generegulation.py), or
the [Immune Response Organoid Test (ONNX)](tests/test_immune.py), respectively.


<table style="width:100%;">
<tr>
    <td>
        <img src="https://github.com/danielathome19/pyorganoid/blob/main/.github/images/membrane_potential_simulation.png?raw=true" style="width:100%;" align="center" alt="Spiking Organoid Example">
    </td>
    <td>
        <img src="https://github.com/danielathome19/pyorganoid/blob/main/.github/images/volume_simulation.png?raw=true" style="width:100%;" align="center" alt="Volumetric Organoid Example">    
    </td>
</tr>
<tr>
    <td>
        <img src="https://github.com/danielathome19/pyorganoid/blob/main/.github/images/generegulation_simulation.png?raw=true" style="width:100%;" align="center" alt="Gene Regulation Organoid Example">
    </td>
    <td>
        <img src="https://github.com/danielathome19/pyorganoid/blob/main/.github/images/immune_response_simulation.png?raw=true" style="width:100%;" align="center" alt="Immune Response Organoid Example">    
    </td>
</tr>
</table>

## License

Pyorganoid is licensed under the BSD-3 License. See the [LICENSE](LICENSE.md) file for more information.

<!-- Project development began July 6th, 2024. -->
