# Yet another Stock Performance Analysis

The idea of this tool is to support hobby investors in finding promising stocks. A list of securities (ISINs or ticker symbols) is used as input. This can be based on Dax, Nasdaq or S&P500, for example. Using the API of [financialmodelingprep.com](https://site.financialmodelingprep.com/), various fundamental data is retrieved and filtered / highlighted according to configurable criteria.

Disclaimer: No responsibility is taken for the accuracy of the information displayed. Anyone using the tool is responsible for verifying the data with an independent source.

[![License](https://img.shields.io/badge/license-gpl-3.svg)](https://choosealicense.com/licenses/gpl-3.0/) [![Repo Status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

## Installation
* Install dependencies according to requirements.txt
* Register at [financialmodelingprep.com](https://site.financialmodelingprep.com/) to get an API key
* Store the API key in the environment variable FMP_API: `export FMP_API=your-api-key`

## Usage
TBD

## General Concept
### Main Use Cases

The following diagram show the main usecases of this project
![usecases](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/achim0x/yasp/master/docs/diagrams/src/usecases.iuml&fmt=svg)

### Class Diagram

The following show the main structure of the project

![classes](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/achim0x/yasp/master/docs/diagrams/src/classes.iuml&fmt=svg)

### Detailed Documentation
See docs folder

## Dependencies
See requirements.txt

## Issues, Ideas And Bugs

If you have further ideas or you found some bugs, great! Create an [issue](https://github.com/achim0x/yasp/issues) or if you are able and willing to fix it by yourself, clone the repository and create a pull request.

## License

The whole source code is published under [GPL3.0](https://github.com/achim0x/yasp/blob/main/LICENSE).
Consider the different licenses of the used third party libraries too!

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, shall be licensed as above, without any additional terms or conditions.