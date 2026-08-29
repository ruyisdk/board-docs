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
         |--- README.md # English example documentation (optional)
         |
         |--- README_zh.md # Chinese example documentation
         |
         |--- Images and other supporting files
```

## Conventions

### Directory Naming

- Name new board directories after the official product name used by the chip or board vendor, with spaces removed (for example, `BPI-F3` and `Jupiter2`).
- Name new example directories using lowercase letters and hyphens (for example, `hello-world` and `pedestrian-detection`).
- Do not rename existing directories; this convention applies only to new content.

### Version References

- When a tutorial installs `ruyi`, always link to the [official RuyiSDK installation documentation](https://ruyisdk.org/en/docs/Package-Manager/installation/) instead of using a hard-coded download link for a specific version, such as `ruyi-0.47.0.amd64`.
- When a specific version must be shown, state that it is an example using version X, revalidate the tutorial, and ensure the frontmatter `last_update` field truthfully reflects the document's last update date.

### Bilingual Documentation

- New examples must provide a Chinese `README_zh.md`.
- An English `README.md` is welcome.
- Having only one language does not block merging.

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

#### DCO enforcement in CI

All pull requests go through an automated DCO check in our continuous integration (CI) pipeline. This check verifies that all commits in your pull request have a proper DCO sign-off. If any commits are missing the sign-off, the CI check will fail, and your pull request cannot be merged until the issue is fixed.

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

All six board metadata fields above are required and must not be empty.

The YAML metadata for example documentation can refer to the Blink example for Milk-V Duo S:

```yaml
# /Duo_S/Blink/README_zh.md
---
sys: debian              # System identifier
sys_ver: v1.6.35         # System version
sys_var: null            # Variant identifier
provider: milkv          # Image provider
category: peripheral     # Example category
last_update: 2026-04-09  # Document last update date
model: Milk-V Duo S      # Board name
profile: Blink           # Example name
---
```

All example metadata fields above except `provider` are required. If the system
version is unknown or no system variant exists, keep `sys_ver` and `sys_var` and
set their values to `null`. The optional `provider` field identifies the provider
or maintainer of the system image and may be omitted when unknown.

#### Example Categories

The `category` field in an example document must use one of the following values:

| `category` value | Category |
| --- | --- |
| `getting-started` | Getting started |
| `peripheral` | Peripheral control |
| `network` | Networking |
| `system` | System programming |
| `storage` | Storage |
| `power-management` | Power management |
| `multimedia` | Multimedia applications |
| `computer-vision` | Computer vision |
| `ai` | Artificial intelligence |
| `security` | Security |
| `compression` | Data compression |
| `gui` | Graphical user interfaces |
| `benchmark` | Benchmarking |
| `application` | Integrated applications |
| `other` | Other |

Choose one category based on the example's primary learning objective. UART, I2C,
and SPI examples normally belong to `peripheral`; network protocols and services
belong to `network`; system calls, kernel interfaces, and multicore coordination
belong to `system`. Use `other` only when no listed category applies, and briefly
explain the reason in the pull request description.

If there are any parts that are still unclear, please create an issue.

## Documentation Writing Standards

### Board and Example Documentation

Please refer to the following templates:

- [English board template](./templates/[board-name]/README.md)
- [Chinese board template](./templates/[board-name]/README_zh.md)
- [Chinese example template](./templates/[board-name]/[example-name]/README_zh.md)
- [English example template (optional)](./templates/[board-name]/[example-name]/README.md)

### Internationalization (i18n)

- Board documentation uses README.md for English and README_zh.md for Chinese
- Example documentation uses README_zh.md; an English README.md is optional
- Other translations use the {FileName}_{lang}.md format
- Keep metadata, commands, versions, links, and expected results consistent between language versions
- Maintain correct hyperlinks between documents
- Use consistent terminology with other documents in the same language
