# Yet another Stock Performance Analysis

[![License](https://img.shields.io/badge/license-bsd-3.svg)](https://choosealicense.com/licenses/bsd-3-clause/) [![Repo Status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [SW Documentation](#sw-documentation)
- [Issues, Ideas And Bugs](#issues-ideas-and-bugs)
- [License](#license)
- [Contribution](#contribution)

## Overview

The idea of this tool is to support hobby investors in finding promising stocks. A list of securities (ISINs or ticker symbols) is used as input. This can be based on Dax, Nasdaq or S&P500, for example. Using the API of [financialmodelingprep.com](https://site.financialmodelingprep.com/), various fundamental data is retrieved and filtered / highlighted according to configurable criteria.

Disclaimer: No responsibility is taken for the accuracy of the information displayed. Anyone using the tool is responsible for verifying the data with an independent source.

More information on the deployment and architecture can be found in the [documentation](./docs/README.md)

For Detailed Software Design run `$ /docs/detailed-design/make html` to generate the detailed design documentation that then can be found
in the folder `/docs/detailed-design/_build/html/index.html`

## Installation

```bash
git clone https://github.com/achim0x/yasp.git
cd yasp
pip install .
```

- Install dependencies according to requirements.txt
- Register at [financialmodelingprep.com](https://site.financialmodelingprep.com/) to get an API key
- Store the API key in the environment variable FMP_API: `export FMP_API=your-api-key`
- In VSCode this also can be done in settings.json:

  ```json
  "terminal.integrated.env.osx": {
    "FMP_API":"your-api-key"
    },
   "terminal.integrated.env.windows": {
    "FMP_API":"your-api-key"
    },
    ```

## Usage

>TODO

```bash
example [-h] [-v] {command} {command_options}
```

## SW Documentation

More information on the deployment and architecture can be found in the [documentation](./doc/README.md)

For Detailed Software Design run `$ /doc/detailed-design/make html` to generate the detailed design documentation that then can be found
in the folder `/doc/detailed-design/_build/html/index.html`

## Dependencies

see [requirements.txt](requirements.txt)

## Issues, Ideas And Bugs

If you have further ideas or you found some bugs, great! Create an [issue](https://github.com/achim0x/yasp/issues) or if you are able and willing to fix it by yourself, clone the repository and create a pull request.

## License

The whole source code is published under [BSD-3-Clause](https://github.com/achim0x/yasp/blob/main/LICENSE).
Consider the different licenses of the used third party libraries too!

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, shall be licensed as above, without any additional terms or conditions.
