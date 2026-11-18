---
sys: Ubuntu
sys_ver: "26.04"
sys_var: null

category: benchmark
last_update: 2026-11-17

model: SpacemiT V100-C2201
profile: Coremark
---

# RuyiSDK Performance Test Example
Install dependencies

```
sudo apt update; sudo apt install -y wget tar zstd xz-utils git build-essential
```

Install the ruyi package manager (see the [official installation guide](https://ruyisdk.org/docs/Package-Manager/installation) for other methods)

```bash
wget https://github.com/ruyisdk/ruyi/releases/download/0.54.0/ruyi-0.54.0.riscv64
chmod +x ./ruyi-0.54.0.riscv64
sudo cp -v ./ruyi-0.54.0.riscv64 /usr/local/bin/ruyi
```

Install the GCC and LLVM toolchains

```
ruyi update

ruyi install gnu-ruyisdk llvm-ruyisdk
```

## Coremark (GCC)

Create and activate the ruyi virtual environment (GCC)
```
ruyi venv -t gnu-ruyisdk manual venv-gnu-ruyisdk-v100

. venv-gnu-ruyisdk-v100/bin/ruyi-activate
```

Verify the GCC version

```
riscv64-ruyisdk-linux-gnu-gcc -v
```

Compile and run Coremark (GCC)

```
git clone https://github.com/eembc/coremark

cd coremark &&
make CC=riscv64-ruyisdk-linux-gnu-gcc XCFLAGS="-march=rv64imafdcvh_zicbom_zicbop_zicboz_ziccrse_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zaamo_zalrsc_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknhb_zvksed_zvksh_zvkt_smaia_smstateen_ssaia_sscofpmf_ssnpm_sstc_svade_svinval_svnapot_svpbmt" compile &&
mv coremark.exe coremark-gcc &&
./coremark-gcc
```

Under normal circumstances, the terminal displays output similar to:

```
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 13702
Total time (secs): 13.702000
Iterations/Sec   : 14596.409283
Iterations       : 200000
Compiler version : GCC16.2.1 20260921
Compiler flags   : -O2 -march=rv64imafdcvh_zicbom_zicbop_zicboz_ziccrse_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zaamo_zalrsc_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknhb_zvksed_zvksh_zvkt_smaia_smstateen_ssaia_sscofpmf_ssnpm_sstc_svade_svinval_svnapot_svpbmt  -lrt
Memory location  : Please put data memory location here
			(e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x4983
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 14596.409283 / GCC16.2.1 20260921 -O2 -march=rv64imafdcvh_zicbom_zicbop_zicboz_ziccrse_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zaamo_zalrsc_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknhb_zvksed_zvksh_zvkt_smaia_smstateen_ssaia_sscofpmf_ssnpm_sstc_svade_svinval_svnapot_svpbmt  -lrt / Heap
```

Return to the parent directory and exit the ruyi GCC virtual environment

```
cd ..; ruyi-deactivate
```

## Coremark (LLVM)

Create and activate the ruyi virtual environment (LLVM)

```
ruyi venv -t llvm-ruyisdk manual --sysroot-from gnu-ruyisdk venv-llvm-ruyisdk-v100

. venv-llvm-ruyisdk-v100/bin/ruyi-activate
```

Verify the LLVM version

```
clang -v
```

Compile and run Coremark (LLVM)

```
cd coremark &&
make clean &&
make CC=clang XCFLAGS="-march=rv64imafdcvh_zicbom_zicbop_zicboz_ziccrse_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zaamo_zalrsc_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknhb_zvksed_zvksh_zvkt_smaia_smstateen_ssaia_sscofpmf_ssnpm_sstc_svade_svinval_svnapot_svpbmt" compile &&
mv coremark.exe coremark-llvm &&
./coremark-llvm
```

Under normal circumstances, the terminal displays output similar to:

```
2K performance run parameters for coremark.
CoreMark Size    : 666
Total ticks      : 12194
Total time (secs): 12.194000
Iterations/Sec   : 9020.829916
Iterations       : 110000
Compiler version : RuyiSDK Clang 22.1.8 (https://github.com/ruyisdk/llvm-project 15a6990a121f883ac215df2fc2677c5ace23ec41 RuyiSDK 20260625)
Compiler flags   : -O2 -march=rv64imafdcvh_zicbom_zicbop_zicboz_ziccrse_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zaamo_zalrsc_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknhb_zvksed_zvksh_zvkt_smaia_smstateen_ssaia_sscofpmf_ssnpm_sstc_svade_svinval_svnapot_svpbmt  -lrt
Memory location  : Please put data memory location here
			(e.g. code in flash, data on heap etc)
seedcrc          : 0xe9f5
[0]crclist       : 0xe714
[0]crcmatrix     : 0x1fd7
[0]crcstate      : 0x8e3a
[0]crcfinal      : 0x33ff
Correct operation validated. See README.md for run and reporting rules.
CoreMark 1.0 : 9020.829916 / RuyiSDK Clang 22.1.8 (https://github.com/ruyisdk/llvm-project 15a6990a121f883ac215df2fc2677c5ace23ec41 RuyiSDK 20260625) -O2 -march=rv64imafdcvh_zicbom_zicbop_zicboz_ziccrse_zicntr_zicond_zicsr_zifencei_zihintntl_zihintpause_zihpm_zimop_zaamo_zalrsc_zawrs_zfa_zfbfmin_zfh_zfhmin_zca_zcb_zcd_zcmop_zba_zbb_zbc_zbs_zkt_zvbb_zvbc_zve32f_zve32x_zve64d_zve64f_zve64x_zvfbfmin_zvfbfwma_zvfh_zvfhmin_zvkb_zvkg_zvkned_zvknhb_zvksed_zvksh_zvkt_smaia_smstateen_ssaia_sscofpmf_ssnpm_sstc_svade_svinval_svnapot_svpbmt  -lrt / Heap
```

Return to the parent directory and exit the ruyi LLVM virtual environment

```
cd ..; ruyi-deactivate
```
