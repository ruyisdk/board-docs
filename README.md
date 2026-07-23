# board-docs

[中文](./README_zh.md) / [English](./README.md)

Welcome to the RuyiSDK development board tutorial and example documentation center. This repository mainly contains environment initialization guides, basic examples, peripheral examples, multimedia, AI, and other tutorial documents for various RISC-V development boards.

## 📚 Directory Structure

- `/<board-name>`: Stores tutorial documents and examples categorized by development board model (in Markdown format).
- `/templates`: Stores documentation templates for adding new boards and examples.

## 🚀 Supported Development Board Matrix

This repository currently includes, but is not limited to, documentation resources for the following hardware:

| Supported Device            | Board Documentation                              | Chip Vendor |
| --------------------------- | ------------------------------------------------ | ----------- |
| Banana Pi BPI-F3            | [BPI-F3](./BPI-F3/README.md)                     | [SpacemiT](https://www.spacemit.com/en/)         |
| Milk-V Duo (64M)            | [Duo](./Duo/README.md)                           | [SOPHGO](https://en.sophgo.com/)                 |
| Milk-V Duo (256M)           | [Duo_256m](./Duo_256m/README.md)                 | [SOPHGO](https://en.sophgo.com/)                 |
| Milk-V Duo S                | [Duo_S](./Duo_S/README.md)                       | [SOPHGO](https://en.sophgo.com/)                 |
| EBC7700                     | [EBC7700](./EBC7700/README.md)                   | [ESWIN](https://www.eswincomputing.com/en/)      |
| ESP32-P4-Function-EV-Board  | [ESP32-P4](./ESP32-P4/README.md)                 | [Espressif](https://www.espressif.com/en/)       |
| Milk-V Jupiter2             | [Jupiter2](./Jupiter2/README.md)                 | [SpacemiT](https://www.spacemit.com/en/)         |
| Canaan K510-CRB-V1.2 KIT    | [K510](./K510/README.md)                         | [Canaan](https://www.canaan.io/)                 |
| Lichee Pi 3A                | [LicheePi3A](./LicheePi3A/README.md)             | [SpacemiT](https://www.spacemit.com/en/)         |
| Lichee Pi 4A                | [LicheePi4A](./LicheePi4A/README.md)             | [XuanTie](https://www.xrvm.com/)                 |
| Milk-V Meles                | [Meles](./Meles/README.md)                       | [XuanTie](https://www.xrvm.com/)                 |
| Milk-V Pioneer              | [Pioneer](./Pioneer/README.md)                   | [SOPHGO](https://en.sophgo.com/)                 |
| Nuclei RV-STAR              | [RV-STAR](./RV-STAR/README.md)                   | [GigaDevice](https://www.gigadevice.com/)        |
| VisionFive 2 Lite           | [VisionFive2Lite](./VisionFive2Lite/README.md)   | [StarFive](https://starfivetech.com/en/)         |

*(Note: For the complete support status, please visit the [board documentation frontend](https://board-docs-frontend.pages.dev/).)*

## 🛠️ How to Contribute

We warmly welcome developers or interns to submit new development board evaluations or improve existing documentation. Please follow the steps below:

1. **Fork this repository** and clone it locally.
2. **Use templates**: Use the standard documentation templates in [`templates/`](./templates/) and fill in the initialization process and test results as required.
3. **Format check**: Ensure correct Markdown syntax, and pay special attention to checking for broken links.
4. **Submit a PR**: Clearly describe the development board model you tested and the toolchain version used in the PR description.

## 📄 License

- All **documentation and tutorial content** in this repository is licensed under the [CC BY 4.0 License](https://creativecommons.org/licenses/by/4.0/). Please provide proper attribution when redistributing or modifying.
- All **example code and scripts** in this repository are licensed under the [Apache 2.0 License](./LICENSE).
