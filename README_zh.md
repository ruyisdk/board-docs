# Ruyi 开发板教程与示例文档库

[中文](./README_zh.md) / [English](./README.md)

欢迎来到 RuyiSDK 的开发板教程与示例文档中心。本仓库主要存放各款 RISC-V 开发板的环境初始化指南、基础示例、外设示例、多媒体、AI等示例教程文档。

## 📚 目录结构说明

- `/<board-name>`: 存放按开发板型号分类的教程文档与示例（Markdown 格式）。
- `/templates`: 存放新增开发板和示例时使用的文档模板。

## 🚀 支持的开发板矩阵

目前本仓库已包含但不限于以下硬件的文档资源：

| 支持设备                    | 开发板文档                                          | 芯片厂商    |
| --------------------------- | --------------------------------------------------- | ----------- |
| Banana Pi BPI-F3            | [BPI-F3](./BPI-F3/README_zh.md)                     | [SpacemiT](https://www.spacemit.com/)              |
| Milk-V Duo (64M)            | [Duo](./Duo/README_zh.md)                           | [SOPHGO](https://www.sophgo.com/)                  |
| Milk-V Duo (256M)           | [Duo_256m](./Duo_256m/README_zh.md)                 | [SOPHGO](https://www.sophgo.com/)                  |
| Milk-V Duo S                | [Duo_S](./Duo_S/README_zh.md)                       | [SOPHGO](https://www.sophgo.com/)                  |
| EBC7700                     | [EBC7700](./EBC7700/README_zh.md)                   | [ESWIN](https://www.eswincomputing.com/)           |
| ESP32-P4-Function-EV-Board  | [ESP32-P4](./ESP32-P4/README_zh.md)                 | [Espressif](https://www.espressif.com/zh-hans/)    |
| Milk-V Jupiter2             | [Jupiter2](./Jupiter2/README_zh.md)                 | [SpacemiT](https://www.spacemit.com/)              |
| Canaan K510-CRB-V1.2 KIT    | [K510](./K510/README_zh.md)                         | [Canaan](https://www.canaan.io/)                   |
| Lichee Pi 3A                | [LicheePi3A](./LicheePi3A/README_zh.md)             | [SpacemiT](https://www.spacemit.com/)              |
| Lichee Pi 4A                | [LicheePi4A](./LicheePi4A/README_zh.md)             | [XuanTie](https://www.xrvm.cn/)                    |
| Milk-V Meles                | [Meles](./Meles/README_zh.md)                       | [XuanTie](https://www.xrvm.cn/)                    |
| Milk-V Pioneer              | [Pioneer](./Pioneer/README_zh.md)                   | [SOPHGO](https://www.sophgo.com/)                  |
| Nuclei RV-STAR              | [RV-STAR](./RV-STAR/README_zh.md)                   | [GigaDevice](https://www.gigadevice.com.cn/)       |
| VisionFive 2 Lite           | [VisionFive2Lite](./VisionFive2Lite/README_zh.md)   | [StarFive](https://starfivetech.com/)              |

*(注：完整的支持状态请访问[开发板文档前端](https://board-docs-frontend.pages.dev/)查阅。)*

## 🛠️ 如何参与贡献

我们非常欢迎开发者或实习生提交新的开发板评测或修正现有文档。请遵循以下步骤：

1. **Fork 本仓库** 并拉取到本地。
2. **使用模板**：使用 [`templates/`](./templates/) 中的标准文档模板，按照要求填写初始化过程和测试结果。
3. **格式检查**：请确保 Markdown 语法正确，特别注意检查是否包含失效的死链（Broken Links）。
4. **提交 PR**：请在 PR 描述中清晰说明你所测试的开发板型号和使用的工具链版本。

## 📄 版权与许可协议

- 本仓库中的**所有文档与教程内容**均采用 [CC BY 4.0 协议](https://creativecommons.org/licenses/by/4.0/)。转载或二次创作请注明出处。
- 本仓库中的**示例代码与脚本**采用 [Apache 2.0 协议](./LICENSE)。
