#define candidate rc6

Summary:	The U-Boot bootloader
Name:		u-boot
Version:	2026.01
Release:	%{?candidate:0.%{candidate}.}1
License:	GPLv2+ BSD LGPL-2.1+ LGPL-2.0+
Group:		System
URL:		https://www.denx.de/wiki/U-Boot
Source0:	https://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2
Source1:	u-boot-board.template

# (tpg) add more paths to check for dtb files
Patch1:		https://src.fedoraproject.org/rpms/uboot-tools/raw/master/f/u-boot-2021.04-rc4-add-more-directories-to-efi_dtb_prefixes.patch
#Patch2:		https://src.fedoraproject.org/rpms/uboot-tools/raw/rawhide/f/smbios-Simplify-reporting-of-unknown-values.patch

# Board fixes and enablement
# RPi - uses RPI firmware device tree for HAT support
#Patch3:		https://src.fedoraproject.org/rpms/uboot-tools/raw/rawhid/f/rpi-Enable-using-the-DT-provided-by-the-Raspberry-Pi.patch


# Rockchips improvements
#Patch7:		https://src.fedoraproject.org/rpms/uboot-tools/raw/rawhide/f/rockchip-Add-initial-support-for-the-PinePhone-Pro.patch

# Misc patches
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=973323
Patch101:	https://raw.githubusercontent.com/armbian/build/main/patch/u-boot/u-boot-rockchip64-v2022.04/general-dwc-otg-usb-fix.patch
#Patch102:	https://raw.githubusercontent.com/armbian/build/main/patch/u-boot/u-boot-rockchip64-v2022.04/general-support-recovery-button.patch
#Patch103:	https://raw.githubusercontent.com/armbian/build/main/patch/u-boot/u-boot-rockchip64-v2022.04/rk3399-disable-hdmi.patch
Patch104:	https://raw.githubusercontent.com/armbian/build/main/patch/u-boot/u-boot-rockchip64-v2022.04/rk3399-always-init-rkclk.patch
#Patch105:	https://raw.githubusercontent.com/armbian/build/main/patch/u-boot/u-boot-rockchip64-v2022.04/u-boot-rk-rk3399-usb-start.patch
#Patch106:	https://raw.githubusercontent.com/armbian/build/main/patch/u-boot/u-boot-rockchip64-v2022.04/rk3399-populate-child-node-of-syscon.patch
#Patch107:	https://raw.githubusercontent.com/armbian/build/main/patch/u-boot/u-boot-rockchip64-v2022.04/board-rockpro64-advanced-recovery.patch
BuildRequires:	bc
BuildRequires:	dtc
BuildRequires:	make
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(libfdt)
BuildRequires:	python%{pyver}dist(pyelftools)
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	swig
BuildRequires:	arm-trusted-firmware-armv8
Requires:	dtc
# (tpg) this is needed for our logo
BuildRequires:	distro-release-desktop
BuildRequires:	imagemagick
BuildRequires:	opensbi
BuildRequires:	cross-riscv64-openmandriva-linux-gnu-binutils
BuildRequires:	cross-riscv64-openmandriva-linux-gnu-gcc
BuildRequires:	cross-aarch64-openmandriva-linux-gnu-binutils
BuildRequires:	cross-aarch64-openmandriva-linux-gnu-gcc

%define riscv64_boards qemu-riscv64 qemu-riscv64_smode qemu-riscv64_spl sifive_unmatched
%define sun50i_boards a64-olinuxino amarula_a64_relic bananapi_m2_plus_h5 bananapi_m64 libretech_all_h3_cc_h5 nanopi_a64 nanopi_neo2 nanopi_neo_plus2 orangepi_pc2 orangepi_prime orangepi_win orangepi_zero_plus orangepi_zero_plus2 pine64-lts pine64_plus pinebook pinephone pinetab sopine_baseboard teres_i
%define sun50h6_boards beelink_gs1 orangepi_3 orangepi_lite2 orangepi_one_plus orangepi_zero2 pine_h64 tanix_tx6
%define rk3328_boards evb-rk3328 nanopi-r2s-rk3328 rock64-rk3328 rock-pi-e-rk3328 roc-cc-rk3328
%define rk3399_boards evb-rk3399 ficus-rk3399 firefly-rk3399 khadas-edge-captain-rk3399 khadas-edge-rk3399 khadas-edge-v-rk3399 leez-rk3399 nanopc-t4-rk3399 nanopi-m4-2gb-rk3399 nanopi-m4b-rk3399 nanopi-m4-rk3399 nanopi-neo4-rk3399 nanopi-r4s-rk3399 orangepi-rk3399 pinebook-pro-rk3399 pinephone-pro-rk3399 puma-rk3399 rock960-rk3399 rock-pi-4c-rk3399 rock-pi-4-rk3399 rock-pi-n10-rk3399pro rockpro64-rk3399 roc-pc-mezzanine-rk3399 roc-pc-rk3399 eaidk-610-rk3399
%define rk3588_boards cm3588-nas-rk3588 coolpi-4b-rk3588s coolpi-cm5-evb-rk3588 coolpi-cm5-genbook-rk3588 evb-rk3588 generic-rk3588 jaguar-rk3588 nanopc-t6-rk3588 nanopi-r6c-rk3588s nanopi-r6s-rk3588s neu6a-io-rk3588 neu6b-io-rk3588 nova-rk3588s odroid-m2-rk3588s orangepi-5-plus-rk3588 orangepi-5-rk3588s quartzpro64-rk3588 rock-5-itx-rk3588 rock5a-rk3588s rock5b-rk3588 sige7-rk3588 tiger-rk3588 toybrick-rk3588 turing-rk1-rk3588
%define aarch64_boards qemu_arm64 rpi_3 rpi_3_b_plus rpi_4 rpi_arm64 mt8183_pumpkin apple_m1 dragonboard410c dragonboard820c geekbox hikey khadas-vim khadas-vim2 khadas-vim3 khadas-vim3l libretech-ac libretech_all_h3_it_h5 libretech_all_h5_cc_h5 libretech-cc mvebu_espressobin-88f3720 mvebu_mcbin-88f8040 nanopi-k2 nanopi_r1s_h5 odroid-c2 p212 p2371-2180 p2771-0000-500 p3450-0000 poplar turris_mox vexpress_aemv8a_juno xilinx_zynqmp_virt imx8qm_rom7720_a1_4G synquacer_developerbox %{sun50i_boards} %{sun50h6_boards} %{rk3328_boards} %{rk3399_boards} %{rk3588_boards}

%description
The U-Boot bootloader, commonly used with embedded devices

%package tools
Summary:	Tools for working with the U-Boot bootloader
%rename uboot-tools

%description tools
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.

%package -n uboot-images-armv8
Summary:	u-boot bootloader images for aarch64 boards
Requires:	u-boot-tools
BuildArch:	noarch
%(for i in %{aarch64_boards}; do echo "Requires: u-boot-$i = %{EVRD}"; done)

%description -n uboot-images-armv8
u-boot bootloader binaries for aarch64 boards.

%prep
%autosetup -p1 -n u-boot-%{version}%{?candidate:-%{candidate}}

cp %{SOURCE1} .

# (tpg) use OpenMandriva logo for boot logo
rm -rf tools/logos/u-boot_logo.{svg,bmp}
# (tpg) from here is the default logo displayed
rm -rf drivers/video/u_boot_logo.bmp
cp -f %{_iconsdir}/openmandriva.svg tools/logos/u-boot_logo.svg
convert -size 80x80x32 -type palettealpha %{_iconsdir}/openmandriva.svg tools/logos/u-boot_logo.bmp
convert -size 160x160x8 -type palette %{_iconsdir}/openmandriva.svg -intent undefined drivers/video/u_boot_logo.bmp

%build
mkdir builds

# u-boot makes assumptions about section naming etc. that are specific to ld.bfd
%make_build HOSTCC="%{__cc} %{optflags}" CROSS_COMPILE="" LDFLAGS="-fuse-ld=bfd" KBUILD_LDFLAGS="-fuse-ld=bfd" HOSTLDFLAGS="-fuse-ld=bfd" tools-only_defconfig O=builds/
%make_build HOSTCC="%{__cc} %{optflags}" CROSS_COMPILE="" LDFLAGS="-fuse-ld=bfd" KBUILD_LDFLAGS="-fuse-ld=bfd" HOSTLDFLAGS="-fuse-ld=bfd" tools-all O=builds/

for board in %{riscv64_boards} %{aarch64_boards}; do
	rv64=(%{riscv64_boards})

	if [[ " ${rv64[*]} " == *" $board "* ]]; then
		export CROSS_COMPILE=riscv64-openmandriva-linux-gnu-
	else
		export CROSS_COMPILE=aarch64-openmandriva-linux-gnu-
	fi

	mkdir builds/${board}

	# 3rd party components -- arm-trusted-firmware, opensbi, ...
	# ATF selection, needs improving, suggestions of ATF SoC to Board matrix welcome
	sun50i=(%{sun50i_boards})
	sun50h6=(%{sun50h6_boards})
	rk3328=(%{rk3328_boards})
	rk3399=(%{rk3399_boards})
	rk3588=(%{rk3588_boards})
	if [[ " ${sun50i[*]} " == *" $board "* ]]; then
		echo "Board: $board using sun50i_a64"
		cp %{_datadir}/arm-trusted-firmware/sun50i_a64/* builds/$board/
	elif [[ " ${sun50h6[*]} " == *" $board "* ]]; then
		echo "Board: $board using sun50i_h6"
		cp %{_datadir}/arm-trusted-firmware/sun50i_h6/* builds/$board/
	elif [[ " ${rk3328[*]} " == *" $board "* ]]; then
		echo "Board: $board using rk3328"
		cp %{_datadir}/arm-trusted-firmware/rk3328/bl31.elf builds/$board/atf-bl31
	elif [[ " ${rk3399[*]} " == *" $board "* ]]; then
		echo "Board: $board using rk3399"
		cp %{_datadir}/arm-trusted-firmware/rk3399/* builds/$board/
	elif [[ " ${rk3588[*]} " == *" $board "* ]]; then
		echo "Board: $board using rk3588"
		cp %{_datadir}/arm-trusted-firmware/rk3588/* builds/$board/
	fi
	# End ATF

	%make_build BINMAN_ALLOW_MISSING=1 LDFLAGS=-fuse-ld=bfd KBUILD_LDFLAGS=-fuse-ld=bfd HOSTLDFLAGS=-fuse-ld=bfd ${board}_defconfig O=builds/${board} OPENSBI=%{_datadir}/opensbi/generic/firmware/fw_dynamic.bin
	# (tpg) add our distribution mark and some safe default configs
	sed -i -e '/^CONFIG_IDENT_STRING=".*"/ s/"$/  %{distribution}"/' builds/$board/.config
	sed -i -e 's/.*CONFIG_SERIAL_PRESENT.*$/CONFIG_SERIAL_PRESENT=y/g' builds/$board/.config
	sed -i -e 's/.*CONFIG_GZIP.*$/CONFIG_GZIP=y/g' builds/$board/.config
	sed -i -e 's/.*CONFIG_CMD_UNZIP.*$/CONFIG_CMD_UNZIP=y/g' builds/$board/.config

	%make_build BINMAN_ALLOW_MISSING=1 LDFLAGS=-fuse-ld=bfd KBUILD_LDFLAGS=-fuse-ld=bfd HOSTLDFLAGS=-fuse-ld=bfd O=builds/${board} OPENSBI=%{_datadir}/opensbi/generic/firmware/fw_dynamic.bin
	%make_build BINMAN_ALLOW_MISSING=1 LDFLAGS=-fuse-ld=bfd KBUILD_LDFLAGS=-fuse-ld=bfd HOSTLDFLAGS=-fuse-ld=bfd u-boot.elf O=builds/${board} OPENSBI=%{_datadir}/opensbi/generic/firmware/fw_dynamic.bin
	if [ -n "$EXTRA_TARGETS" ]; then
		%make_build BINMAN_ALLOW_MISSING=1 LDFLAGS=-fuse-ld=bfd KBUILD_LDFLAGS=-fuse-ld=bfd HOSTLDFLAGS=-fuse-ld=bfd O=builds/${board} OPENSBI=%{_datadir}/opensbi/generic/firmware/fw_dynamic.bin $EXTRA_TARGETS
	fi
done

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/uboot/

for tool in dumpimage env/fw_printenv fit_check_sign fit_info gdb/gdbcont gdb/gdbsend gen_eth_addr gen_ethaddr_crc ifwitool img2srec kwboot mkeficapsule mkenvimage mkimage mksunxiboot ncb proftool sunxi-spl-image-builder; do
	install -p -m 0755 builds/tools/$tool %{buildroot}%{_bindir}
done
install -p -m 0644 doc/mkimage.1 %{buildroot}%{_mandir}/man1

install -p -m 0755 builds/tools/env/fw_printenv %{buildroot}%{_bindir}
( cd %{buildroot}%{_bindir}; ln -sf fw_printenv fw_setenv )

BUILDS=$(ls -1 builds |grep -vE '^(Makefile|arch|build|include|lib|scripts|source|tools|u-boot-initial-env|u-boot.cfg)$')

# Copy some useful docs over
mkdir -p builds/docs
cp -p board/rockchip/evb_rk3399/README builds/docs/README.evb_rk3399
cp -p board/sunxi/README.sunxi64 builds/docs/README.sunxi64
cp -p board/sunxi/README.nand builds/docs/README.sunxi-nand

for board in ${BUILDS}; do
	sed -e "s,@BOARD@,$board,g" %{S:1} >%{specpartsdir}/$board.specpart
	mkdir -p %{buildroot}%{_datadir}/uboot/$board/
	for file in u-boot.bin u-boot.dtb u-boot.elf u-boot.img u-boot-dtb.img u-boot.itb u-boot-sunxi-with-spl.bin u-boot-rockchip.bin u-boot-spl.bin idbloader.img idbloader.spi spl/u-boot-spl.bin spl/boot.bin spl/sunxi-spl.bin; do
		if [ -f builds/$board/$file ]; then
			install -p -m 0644 builds/$board/$file %{buildroot}%{_datadir}/uboot/$board/
		fi
	done
done

%files tools
%doc README doc/develop/distro.rst doc/README.gpt
%doc doc/README.rockchip doc/develop/uefi doc/arch/arm64.rst
%doc builds/docs/* doc/board/amlogic/ doc/board/rockchip/
%{_bindir}/*
%doc %{_mandir}/man1/mkimage.1*
%dir %{_datadir}/uboot/
