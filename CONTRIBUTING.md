# RuyiSDK Board Documentation Contribution Guide

[English](./CONTRIBUTING.md) / [中文](./CONTRIBUTING_zh.md)

## Overview

This document is intended for developers who wish to contribute to the RuyiSDK Board Documentation project. The project uses GitHub Pull Request mechanisms for collaboration.

Before contributing, you need to:
1. Have a [GitHub account](https://github.com/signup)
2. Be familiar with basic Git operations and GitHub workflow
3. Understand the project documentation structure and metadata specifications (see below)

If you are not familiar with GitHub and Git, we recommend first reviewing the [GitHub Quick Start Guide](https://docs.github.com/en/get-started/start-your-journey/hello-world).

This document contains general contribution information. Different parts of the project also have more specific instructions:
- [Board (example Milk-V Duo)](./Duo/README.md): Board documentation and hardware metadata.
- [Example (Milk-V Duo/Coremark)](./Duo/Coremark/README_zh.md): Environment setup, commands, and verification results.
- [Documentation templates](./templates/): Document structures for new boards and examples.

Project structure hierarchy:

```plaintext
board-docs
 |
 |--- Board
    |
    |--- README.md # English board documentation, containing hardware metadata
    |
    |--- README_zh.md # Chinese board documentation
    |
    |--- Examples
         |
         |--- README.md # English example documentation
         |
         |--- README_zh.md # Chinese example documentation
         |
         |--- Images and other supporting files
```

## Code of Conduct

Please be respectful and considerate of others when contributing to RuyiSDK. We aim to foster an open and welcoming environment for all contributors.

Please follow [the RuyiSDK Code of Conduct](https://ruyisdk.org/en/code_of_conduct).

## Quick Start

### Creating a PR Workflow

1. Fork and clone the repository locally
2. Create a branch and update or add board and example documentation
3. Commit your changes, ensuring commit messages are clear and understandable, and contain a `Signed-off-by` tag (see below)
    * It's better to squash your commits before pushing.
4. Push your commits to your forked repository and create a Pull Request

> [!Note]
> If the metadata cannot be parsed or the document content does not meet requirements, your pull request may require modifications.

### Developer's Certificate of Origin (DCO)

We require that all contributions to RuyiSDK are covered under the [Developer's Certificate of Origin (DCO)](https://developercertificate.org/). The DCO is a lightweight way for contributors to certify that they wrote or otherwise have the right to submit the code they are contributing.

#### What is the DCO?

The DCO is a declaration that you make when you sign-off a commit, simple
enough that the original text is fully reproduced below.

```
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

#### How to Sign-Off Commits

You need to add a `Signed-off-by` line to each commit message, which certifies that you agree with the DCO:

```
Signed-off-by: Your Name <your.email@example.com>
```

You can add this automatically by using the `-s` or `--signoff` flag when committing:

```
git commit -s -m "Your commit message"
```

Make sure that the name and email in the signature matches your Git configuration. You can set your Git name and email with:

```
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### DCO Verification

This repository does not yet have automated DCO checks enabled. Maintainers will verify the `Signed-off-by` tag in each commit during review.

## Data Structure Specifications

### Metadata Definitions

The YAML metadata for board documentation can refer to Milk-V Duo:

```yaml
# /Duo/README.md
---
product: Milk-V Duo (64M) # Full product name
cpu: CV1800B              # Processor model
cpu_core: XuanTie C906     # CPU core architecture
ram: 64MB                  # Memory and flash information
vendor: Milk-V             # Board manufacturer
silicon_vendor: Sophgo     # Chip manufacturer
---
```

The YAML metadata for example documentation can refer to the Blink example for Milk-V Duo S:

```yaml
# /Duo_S/Blink/README_zh.md
---
sys: debian              # System identifier
sys_ver: v1.6.35         # System version
sys_var: null            # Variant identifier
provider: milkv          # Image provider
status: peripheral       # Example category
last_update: 2026-04-09  # Document last update date
model: Milk-V Duo S      # Board name
profile: Blink           # Example name
---
```

#### Example Categories

The `status` field in an example document must use one of the following values:

| `status` value | Category |
| --- | --- |
| `basics` | Basics |
| `peripheral` | Peripheral control |
| `communication` | Communication interfaces |
| `network` | Networking |
| `system` | System programming |
| `multimedia` | Multimedia applications |
| `computer-vision` | Computer vision |
| `ai` | Artificial intelligence |
| `crypto` | Cryptography and security |
| `compression` | Data compression |
| `gui` | Graphical user interfaces |
| `benchmark` | Benchmarking |
| `application` | Applications and integration |

If there are any parts that are still unclear, please create an issue.

## Documentation Writing Standards

### Board and Example Documentation

Please refer to the following templates:

- [English board template](./templates/[board-name]/README.md)
- [Chinese board template](./templates/[board-name]/README_zh.md)
- [Chinese example template](./templates/[board-name]/[example-name]/README_zh.md)

### Internationalization (i18n)

- Main documentation should be written in English (README.md)
- Translation documents use the {FileName}_{lang}.md format (e.g. Chinese translation can use README_zh.md)
- Keep metadata, commands, versions, links, and expected results consistent between language versions
- Maintain correct hyperlinks between documents
- Use consistent terminology with other documents in the same language
