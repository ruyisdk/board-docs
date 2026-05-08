---
sys: revyos
sys_ver: "20251226"
sys_var: null

status: AI
last_update: 2026-05-08

model: Lichee Pi 4A
profile: GStreamer 
---

# **RuyiSDK示例**
### **安装依赖库**
更新源并安装 rsync
```bash
sudo apt update
sudo apt install rsync
```
安装GStreamer需要的相关依赖库    
```bash
sudo apt install git build-essential libgstreamer* gstreamer1.0-tools
```
### **安装 RuyiSDK**
```bash
# 下载并安装 ruyi
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.47.0/ruyi-0.47.0.amd64
chmod +x ruyi-0.47.0.amd64
sudo cp ruyi-0.47.0.amd64 /usr/local/bin/ruyi
```
### **安装工具链**
```bash
ruyi update
ruyi install gnu-plct-xthead
```

会在终端看到如下输出：  
```text

info: skipping already installed package gnu-plct-xthead-3.1.0-ruyi.20250526

```
## **GStreamer测试示例**
### **示例描述和硬件环境准备**
GStreamer 是一个基于管道的多媒体框架，基于 GObject，以 C 语言写成。凭借 GStreamer，可以很容易地创建各种多媒体功能组件，包括简单的音频回放、音频和视频播放、录音、流媒体和音频编辑。基于流水线设计，可以创建诸如视频编辑器、流媒体广播和媒体播放器等等的很多多媒体应用。   
硬件环境：Lichee Pi 4A (16GB)     
### **创建并激活 ruyi 虚拟环境**
如已经创建可跳过  
创建虚拟环境 venv-sipeed  
```bash
ruyi venv -t gnu-plct-xthead sipeed-lpi4a venv-sipeed 
```
激活虚拟环境  
```bash
. venv-sipeed/bin/ruyi-activate 
```
拉取源码：  
```bash
git clone https://gitlab.freedesktop.org/gstreamer/gst-docs.git
cd gst-docs/examples/tutorials
```

### **使用 ruyi 工具链编译示例代码**
确认交叉编译器可用
```bash
riscv64-plctxthead-linux-gnu-g++ --version
```
需要把开发板的sysroot文件传输：  
```bash
mkdir -p ~/sysroot
rsync -avz --safe-links debian@172.16.60.209:/lib ~/sysroot/
rsync -avz --safe-links debian@172.16.60.209:/usr ~/sysroot/
```
编译器默认会在 $SYSROOT/usr/lib 找，但 Debian 把它放在了子目录下：  

```bash
ln -sf $SYSROOT/usr/lib/riscv64-linux-gnu/* $SYSROOT/usr/lib/
ln -sf $SYSROOT/lib/riscv64-linux-gnu/* $SYSROOT/lib/
```

进行交叉编译：  
```bash
export SYSROOT=$HOME/sysroot

riscv64-plctxthead-linux-gnu-gcc basic-tutorial-1.c -o basic-tutorial-1 \
--sysroot=$SYSROOT \
-I$SYSROOT/usr/include/riscv64-linux-gnu \
$(PKG_CONFIG_SYSROOT_DIR=$SYSROOT \
  PKG_CONFIG_LIBDIR=$SYSROOT/usr/lib/riscv64-linux-gnu/pkgconfig:$SYSROOT/usr/share/pkgconfig \
  pkg-config --cflags --libs gstreamer-1.0)
```
进行验证：  
```bash
file basic-tutorial-1
```
在终端显示如下：  
```text
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~/gst-docs/examples/tutorials$ export SYSROOT=$HOME/sysroot
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~/gst-docs/examples/tutorials$ riscv64-plctxthead-linux-gnu-gcc basic-tutorial-1.c -o basic-tutorial-1 \
--sysroot=$SYSROOT \
-I$SYSROOT/usr/include/riscv64-linux-gnu \
$(PKG_CONFIG_SYSROOT_DIR=$SYSROOT \
  PKG_CONFIG_LIBDIR=$SYSROOT/usr/lib/riscv64-linux-gnu/pkgconfig:$SYSROOT/usr/share/pkgconfig \
  pkg-config --cflags --libs gstreamer-1.0)
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~/gst-docs/examples/tutorials$ file basic-tutorial-1
basic-tutorial-1: ELF 64-bit LSB executable, UCB RISC-V, RVC, double-float ABI, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-riscv64-lp64d.so.1, BuildID[sha1]=cdfa865ffbb56b0040283dba3a1b5af82db6885a, for GNU/Linux 4.15.0, not stripped

```
### **运行示例并验证结果**
把 basic-tutorial-1传到开发板：  
```bash
scp basic-tutorial-1 debian@172.16.60.209:~/
```
在终端显示如下：  
```bash
«Ruyi venv-sipeed» licheepi@licheepi-virtual-machine:~/gst-docs/examples/tutorials$ scp basic-tutorial-1 debian@172.16.60.209:~/
debian@172.16.60.209's password: 
basic-tutorial-1                 100% 9128   244.8KB/s   00:00 
```
在开发板上进行验证：  
```text
chmod +x basic-tutorial-1
./basic-tutorial-1
```
在终端显示如下：  

```text
debian@revyos-lpi4a:~$ chmod +x basic-tutorial-1

debian@revyos-lpi4a:~$ ./basic-tutorial-1

[DBGT][debug_vc8kdec_trace] disabled

OMX  ! decoder_get_parameter OMX_ErrorNoMore (2)

[16455.408937] PM: hibernation: Not find  nosave memory: [mem 0x10000000-0x1fffffff]

OMX  ! decoder_useegl_image API: Use egl image not implemented

debian@revyos-lpi4a:~$
```
程序调用了系统的 OpenMAX 多媒体组件，该组件部分接口未实现或返回提示信息，但不影响程序正常运行。  
音频测试：  
```bash
gst-launch-1.0 audiotestsrc ! audioconvert ! autoaudiosink
```
在终端显示如下：  
```text
debian@revyos-lpi4a:~$ gst-launch-1.0 audiotestsrc ! audioconvert ! autoaudiosink
Setting pipeline to PAUSED ...
Pipeline is PREROLLING ...
Redistribute latency...
Pipeline is PREROLLED ...
Setting pipeline to PLAYING ...
Redistribute latency...
New clock: GstAudioSinkClock
handling interrupt.9.
Interrupt: Stopping pipeline ...
Execution ended after 0:01:07.677997819
Setting pipeline to NULL ...
Freeing pipeline ...

```

