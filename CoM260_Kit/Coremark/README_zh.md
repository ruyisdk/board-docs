---
sys: Bianbu
sys_ver: 4.0.6
sys_var: LXQt

category: benchmark
last_update: 2026-09-17

model: CoM260 Kit
profile: Coremark
---

# RuyiSDK 性能测试示例
安装依赖包

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

安装ruyi包管理器（其他安装方式见[官方安装文档](https://ruyisdk.org/docs/Package-Manager/installation)）

```bash
wget https://mirror.iscas.ac.cn/ruyisdk/ruyi/tags/0.52.0/ruyi-0.52.0.riscv64
chmod +x ./ruyi-0.52.0.riscv64
sudo cp -v ./ruyi-0.52.0.riscv64 /usr/local/bin/ruyi
```

安装GCC和LLVM工具链

```
ruyi update

ruyi install gnu-ruyisdk llvm-ruyisdk
```

## Coremark (GCC版)

创建并激活ruyi虚拟环境（GCC）
```
ruyi venv -t gnu-ruyisdk manual venv-gnu-ruyisdk-com260-kit

. venv-gnu-ruyisdk-com260-kit/bin/ruyi-activate
```

验证GCC版本

```
riscv64-ruyisdk-linux-gnu-gcc -v
```

编译并运行coremark（GCC）

```
git clone https://github.com/eembc/coremark

cd coremark

make CC=riscv64-ruyisdk-linux-gnu-gcc XCFLAGS="-march=rv64imafdcvh_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zaamo_zalrsc_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknha_zvknhb_zvksed_zvksh_zvkt_smaia_smstateen_ssaia_sscofpmf_ssnpm_sstc_svade_svinval_svnapot_svpbmt_sdtrig" compile

mv coremark.exe coremark-gcc

./coremark-gcc
```

正常情况下，终端会看到类似如下输出：

```
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 14358
Total time (secs): 14.358000
Iterations/Sec   : 13929.516646
Iterations       : 200000
Compiler version : GCC16.1.1 20260624
Compiler flags   : -O2 -march=rv64imafdcvh_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zaamo_zalrsc_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknha_zvknhb_zvksed_zvksh_zvkt_smaia_smstateen_ssaia_sscofpmf_ssnpm_sstc_svade_svinval_svnapot_svpbmt_sdtrig  -lrt
Memory location  : Please put data memory location here
			(e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x4983
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 13929.516646 / GCC16.1.1 20260624 -O2 -march=rv64imafdcvh_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zaamo_zalrsc_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknha_zvknhb_zvksed_zvksh_zvkt_smaia_smstateen_ssaia_sscofpmf_ssnpm_sstc_svade_svinval_svnapot_svpbmt_sdtrig  -lrt / Heap
«Ruyi venv-gnu-ruyisdk-com260-kit» com260@ifx:~/coremark$

```

返回上级目录并退出ruyi GCC虚拟环境

```
cd ..; ruyi-deactivate
```

## Coremark (LLVM版)

创建并激活ruyi虚拟环境（LLVM）

```
ruyi venv -t llvm-ruyisdk manual --sysroot-from gnu-ruyisdk venv-llvm-ruyisdk-com260-kit

. venv-llvm-ruyisdk-com260-kit/bin/ruyi-activate
```

验证LLVM版本

```
clang -v
```

编译并运行 coremark（LLVM）

```
cd coremark; make clean

make CC=clang XCFLAGS="-march=rv64imafdcvh_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zaamo_zalrsc_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknha_zvknhb_zvksed_zvksh_zvkt_smaia_smstateen_ssaia_sscofpmf_ssnpm_sstc_svade_svinval_svnapot_svpbmt_sdtrig" compile

mv coremark.exe coremark-llvm

./coremark-llvm
```

正常情况下，终端会看到类似如下输出：

```
./coremark-llvm
rm -f ./coremark.exe ./core_list_join.o ./core_main.o ./core_matrix.o ./core_state.o ./core_util.o ./*.log *.info ./index.html
clang -O2 -Ilinux -Iposix -I. -DFLAGS_STR=\""-O2 -march=rv64imafdcvh_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zaamo_zalrsc_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknha_zvknhb_zvksed_zvksh_zvkt_smaia_smstateen_ssaia_sscofpmf_ssnpm_sstc_svade_svinval_svnapot_svpbmt_sdtrig  -lrt"\" -DITERATIONS=0 -march=rv64imafdcvh_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zaamo_zalrsc_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknha_zvknhb_zvksed_zvksh_zvkt_smaia_smstateen_ssaia_sscofpmf_ssnpm_sstc_svade_svinval_svnapot_svpbmt_sdtrig core_list_join.c core_main.c core_matrix.c core_state.c core_util.c posix/core_portme.c -o ./coremark.exe -lrt
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 12817
Total time (secs): 12.817000
Iterations/Sec   : 8582.351564
Iterations       : 110000
Compiler version : RuyiSDK Clang 22.1.8 (https://github.com/ruyisdk/llvm-project 15a6990a121f883ac215df2fc2677c5ace23ec41 RuyiSDK 20260625)
Compiler flags   : -O2 -march=rv64imafdcvh_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zaamo_zalrsc_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknha_zvknhb_zvksed_zvksh_zvkt_smaia_smstateen_ssaia_sscofpmf_ssnpm_sstc_svade_svinval_svnapot_svpbmt_sdtrig  -lrt
Memory location  : Please put data memory location here
			(e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x33ff
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 8582.351564 / RuyiSDK Clang 22.1.8 (https://github.com/ruyisdk/llvm-project 15a6990a121f883ac215df2fc2677c5ace23ec41 RuyiSDK 20260625) -O2 -march=rv64imafdcvh_zicbom_zicbop_zicboz_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zaamo_zalrsc_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknha_zvknhb_zvksed_zvksh_zvkt_smaia_smstateen_ssaia_sscofpmf_ssnpm_sstc_svade_svinval_svnapot_svpbmt_sdtrig  -lrt / Heap
«Ruyi venv-llvm-ruyisdk-com260-kit» com260@ifx:~/coremark$

```

返回上级目录并退出ruyi LLVM虚拟环境

```
cd ..; ruyi-deactivate
```
