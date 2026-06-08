---
sys: FreeRTOS
sys_ver: 

status: basics
last_update: 2026-05-07

model: ESP32-P4-Function-EV-Board
profile: Hello World

---

# RuyiSDK 基础示例
>说明：ESP32-P4 必须使用乐鑫官方 IDF 工具链编译。本示例中，RuyiSDK 仅用于创建虚拟环境、获取源码和编辑 `hello_world_main.c`，编译烧录仍通过 `idf.py` 完成。

可直接在开发板上进行编译和运行的示例，适合初学者快速上手。

安装ruyi包管理器

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
pip install esptool

wget  https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.48.0/ruyi-0.48.0.amd64
chmod +x ruyi-0.48.0.amd64
sudo cp -v ./ruyi-0.48.0.amd64 /usr/local/bin/ruyi
```

安装GCC和LLVM工具链

```
ruyi update
ruyi install gnu-plct llvm-plct
```

安装 ESP-IDF v5.5.4 及工具链

```
# 下载并运行 ESP-IDF 离线安装包
# 安装完成后，通过"ESP-IDF PowerShell" 快捷方式打开终端
```

## Hello World (GCC版)

创建并配置项目

```
xcopy /e /i $env:IDF_PATH\examples\get-started\hello_world hello_world
cd hello_world

idf.py set-target esp32p4e
```

创建并激活ruyi虚拟环境（GCC）

```
ruyi venv -t toolchain/gnu-plct manual venv-gnu-plct
. venv-gnu-plct/bin/ruyi-activate
```

在虚拟环境中编辑源代码：

```
cd /mnt/d/platform/esp/hello_world/main
nano hello_world_main.c

#include <stdio.h>
void app_main(void)
{
    printf("Hello, World!\n");
}
```

编译并运行Hello World（GCC）

```
idf.py build
idf.py -p COM6 flash

idf.py -p COM6 monitor
```

正常情况下，终端会看到类似如下输出：

```
...
Hello world!
...
```


按 `Ctrl + ]` 退出监视器。

## Hello World (LLVM版)

安装 Clang 工具链

```
python "$env:IDF_PATH/tools/idf_tools.py" install esp-clang
```

切换到 Clang 工具链

```
cd hello_world
$env:IDF_TOOLCHAIN = "clang"
```

重新编译、烧录并运行

```
idf.py fullclean

idf.py build
idf.py -p COM6 flash

idf.py -p COM6 monitor
```

正常情况下，终端会看到类似如下输出：

```
...
Hello world!
...
```

按 `Ctrl + ]` 退出监视器。

清理环境

```
idf.py fullclean
```
