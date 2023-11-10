# matter-controller-server

A Viam modular resource that starts up a Matter Device Controller and uses the paired service API to communicate with the Viam SDKs

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)
- [Development](#development)

## Installation

Can be deployed to a Viam machine as a [modular resource](https://docs.viam.com/registry/) with no configuration. (Currently available to `viam-labs` members only at the moment)

## License

`matter-controller-server` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.

## Development

[Installing Hatch](https://hatch.pypa.io/latest/install/) will make it easier to get setup but not required.

### Install the project dependencies within the dev virtual environment:

```console
hatch -e dev run pip install .
```

### Build Python wheels and publish new version of Viam module

Make sure [`viam` CLI](https://docs.viam.com/manage/cli/) is installed.

```console
make publish
```
