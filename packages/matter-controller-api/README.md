# matter-controller-api

A custom Viam service with generated gPRC client for Python

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)
- [Development](#development)

## Installation

The package can be installed in a Python environment as a remote file dependency in a `requirements.txt` or `pyproject.toml` file:

```
"matter-controller-api @ git+https://github.com/viam-labs/viam-matter-server.git#egg=matter-controller-api&subdirectory=packages/matter-controller-api"
```

## License

`matter-controller-api` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.

## Development

[Installing Hatch](https://hatch.pypa.io/latest/install/) will make it easier to get setup but not required.

### Install the project dependencies within the default virtual environment:

```console
hatch run pip install .
```

### Generate gRPC code from protobuf definitions

Make sure [`buf` CLI](https://buf.build/product/cli) is installed.

```console
make
```
