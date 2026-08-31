---
sys: CanMV Linux SDK
sys_ver: null
sys_var: RV64ILP32 / RV64LP64
category: other
last_update: 2026-08-31

model: BPI-CANMV-K230D-Zero
profile: OS Installation
---

# BPI-CANMV-K230D-Zero 使用说明

## 安装系统镜像

### 直接下载安装

RuyiSDK 目前提供了 LP64 和 ILP32 两种镜像文件，可以通过 RuyiSDK 下载安装，具体步骤如下：

1. 请确保您已经下载并安装了 `ruyi` ，请参考 [RuyiSDK 包管理器安装说明](https://ruyisdk.org/docs/Package-Manager/installation)安装（建议您下载最新版本），安装完成后可以执行 `ruyi --version` 查看版本信息；
2. 执行 `ruyi update` 更新 RuyiSDK 软件源；该操作将会把软件源的最新软件包等资源索引更新到本地，方便后续查询、安装能够得到最新的信息。
3. 执行 `ruyi device provision` 进入系统镜像安装引导程序，按照提示信息，选择 `Canaan Kendryte K230D` 开发板、开发板规格、镜像文件类型等信息，引导程序将会引导您完成镜像的烧录。

   当前，RuyiSDK 为 K230D 提供了 RV64ILP32（玄铁新32位内核+32位rootfs） 和 RV64LP64（常规64位系统），推荐您安装 RV64ILP32 系统体验新32位在动态内存空间消耗上的优势。

   ```bash
   The following system configurations are supported by the device variant you have chosen.
   Please pick the one you want to put on the device:

     1. Canaan Kendryte K230D CanMV Linux SDK demo, RV64ILP32 ABI
     2. Canaan Kendryte K230D CanMV Linux SDK demo, RV64LP64 ABI

   ```

## 启动

设备上电系统自动启动，开发板上红灯亮则说明开发板正常上电。root 账户默认没有密码，此时可以查看串口信息。

如果开发板连接屏幕，稍候会自动运行 LVGL DEMO 展示资源占用，并且 DEMO 含触控交互。
