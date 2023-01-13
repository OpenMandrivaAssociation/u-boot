%undefine candidate

Summary:	U-Boot utilities
Name:		uboot-tools
Version:	2023.01
Release:	%{?candidate:0.%{candidate}.}1
License:	GPLv2+ BSD LGPL-2.1+ LGPL-2.0+
URL:		http://www.denx.de/wiki/U-Boot
Source0:	https://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2
Source1:	https://src.fedoraproject.org/rpms/uboot-tools/raw/master/f/aarch64-boards

# (tpg) add more paths to check for dtb files
Patch1:		https://src.fedoraproject.org/rpms/uboot-tools/raw/master/f/u-boot-2021.04-rc4-add-more-directories-to-efi_dtb_prefixes.patch
Patch2:		https://src.fedoraproject.org/rpms/uboot-tools/raw/rawhide/f/smbios-Simplify-reporting-of-unknown-values.patch

# Board fixes and enablement
# RPi - uses RPI firmware device tree for HAT support
Patch3:		https://src.fedoraproject.org/rpms/uboot-tools/raw/rawhid/f/rpi-Enable-using-the-DT-provided-by-the-Raspberry-Pi.patch
Patch4:		https://src.fedoraproject.org/rpms/uboot-tools/raw/rawhide/f/rpi-fallback-to-max-clock-for-mmc.patch
Patch5:		https://src.fedoraproject.org/rpms/uboot-tools/raw/rawhide/f/rpi-bcm2835_sdhost-firmware-managed-clock.patch
Patch6:		https://src.fedoraproject.org/rpms/uboot-tools/raw/rawhide/f/rpi-Copy-properties-from-firmware-DT-to-loaded-DT.patch

# Rockchips improvements
Patch7:		https://src.fedoraproject.org/rpms/uboot-tools/raw/rawhide/f/rockchip-Add-initial-support-for-the-PinePhone-Pro.patch

# Misc patches
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=973323
Patch101:	https://raw.githubusercontent.com/armbian/build/master/patch/u-boot/u-boot-rockchip64/general-dwc-otg-usb-fix.patch
Patch102:	https://raw.githubusercontent.com/armbian/build/master/patch/u-boot/u-boot-rockchip64/rk3399-disable-hdmi.patch
Patch103:	https://raw.githubusercontent.com/armbian/build/master/patch/u-boot/u-boot-rockchip64/rk3399-always-init-rkclk.patch
Patch104:	https://raw.githubusercontent.com/armbian/build/master/patch/u-boot/u-boot-rockchip64/rk3399-rp64-rng.patch
Patch105:	https://raw.githubusercontent.com/armbian/build/master/patch/u-boot/u-boot-rockchip64/u-boot-rk-rk3399-usb-start.patch
Patch106:	https://raw.githubusercontent.com/armbian/build/master/patch/u-boot/u-boot-rockchip64/rk3399-ehci-probe-usb2.patch
Patch107:	https://raw.githubusercontent.com/armbian/build/master/patch/u-boot/u-boot-rockchip64/rk3399-populate-child-node-of-syscon.patch
Patch108:	https://raw.githubusercontent.com/armbian/build/master/patch/u-boot/u-boot-rockchip64/board-rockpro64-advanced-recovery.patch
BuildRequires:	bc
BuildRequires:	dtc
BuildRequires:	make
BuildRequires:	pkgconfig(python)
BuildRequires:	python3dist(setuptools)
BuildRequires:	python3dist(libfdt)
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	swig
%ifarch aarch64
BuildRequires:	arm-trusted-firmware-armv8
%endif
Requires:	dtc
%ifarch %{armx}
# (tpg) this is needed for out logo
BuildRequires:	distro-release-desktop
BuildRequires:	imagemagick

Obsoletes:	uboot-images-elf < 2019.07
Provides:	uboot-images-elf = 2019.07
%endif

%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.

%ifarch aarch64
%package -n uboot-images-armv8
Summary:	u-boot bootloader images for aarch64 boards
Requires:	uboot-tools
BuildArch:	noarch

%description -n uboot-images-armv8
u-boot bootloader binaries for aarch64 boards.
%endif

%ifarch %{arm}
%package -n uboot-images-armv7
Summary:	u-boot bootloader images for armv7 boards
Requires:	uboot-tools
BuildArch:	noarch

%description -n uboot-images-armv7
u-boot bootloader binaries for armv7 boards.
%endif

%prep
%autosetup -p1 -n u-boot-%{version}%{?candidate:-%{candidate}}

cp %{SOURCE1} .

# (tpg) use OpenMandriva logo for boot logo
%ifarch %{armx}
rm -rf tools/logos/u-boot_logo.{svg,bmp}
# (tpg) from here is the default logo displayed
rm -rf drivers/video/u_boot_logo.bmp
cp -f %{_iconsdir}/openmandriva.svg tools/logos/u-boot_logo.svg
convert -size 80x80x32 -type palettealpha %{_iconsdir}/openmandriva.svg tools/logos/u-boot_logo.bmp
convert -size 160x160x8 -type palette %{_iconsdir}/openmandriva.svg -intent undefined drivers/video/u_boot_logo.bmp
%endif

%build
mkdir builds

# u-boot makes assumptions about section naming etc. that are specific to ld.bfd
%make_build HOSTCC="%{__cc} %{optflags}" CROSS_COMPILE="" LDFLAGS="-fuse-ld=bfd" KBUILD_LDFLAGS="-fuse-ld=bfd" HOSTLDFLAGS="-fuse-ld=bfd" tools-only_defconfig O=builds/
%make_build HOSTCC="%{__cc} %{optflags}" CROSS_COMPILE="" LDFLAGS="-fuse-ld=bfd" KBUILD_LDFLAGS="-fuse-ld=bfd" HOSTLDFLAGS="-fuse-ld=bfd" tools-all O=builds/

%ifarch aarch64
for board in $(cat %{_arch}-boards)
do
  echo "Building board: $board"
  mkdir builds/$(echo $board)/
# ATF selection, needs improving, suggestions of ATF SoC to Board matrix welcome
  sun50i=(a64-olinuxino amarula_a64_relic bananapi_m2_plus_h5 bananapi_m64 libretech_all_h3_cc_h5 nanopi_a64 nanopi_neo2 nanopi_neo_plus2 orangepi_pc2 orangepi_prime orangepi_win orangepi_zero_plus orangepi_zero_plus2 pine64-lts pine64_plus pinebook pinephone pinetab sopine_baseboard teres_i)
  if [[ " ${sun50i[*]} " == *" $board "* ]]; then
    echo "Board: $board using sun50i_a64"
    cp /usr/share/arm-trusted-firmware/sun50i_a64/* builds/$(echo $board)/
  fi
  sun50h6=(beelink_gs1 orangepi_3 orangepi_lite2 orangepi_one_plus orangepi_zero2 pine_h64 tanix_tx6)
  if [[ " ${sun50h6[*]} " == *" $board "* ]]; then
    echo "Board: $board using sun50i_h6"
    cp /usr/share/arm-trusted-firmware/sun50i_h6/* builds/$(echo $board)/
  fi
  rk3328=(evb-rk3328 nanopi-r2s-rk3328 rock64-rk3328 rock-pi-e-rk3328 roc-cc-rk3328)
  if [[ " ${rk3328[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3328"
    cp /usr/share/arm-trusted-firmware/rk3328/* builds/$(echo $board)/
  fi
  rk3399=(evb-rk3399 ficus-rk3399 firefly-rk3399 khadas-edge-captain-rk3399 khadas-edge-rk3399 khadas-edge-v-rk3399 leez-rk3399 nanopc-t4-rk3399 nanopi-m4-2gb-rk3399 nanopi-m4b-rk3399 nanopi-m4-rk3399 nanopi-neo4-rk3399 nanopi-r4s-rk3399 orangepi-rk3399 pinebook-pro-rk3399 puma-rk3399 rock960-rk3399 rock-pi-4c-rk3399 rock-pi-4-rk3399 rock-pi-n10-rk3399pro rockpro64-rk3399 roc-pc-mezzanine-rk3399 roc-pc-rk3399)
  if [[ " ${rk3399[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3399"
    cp /usr/share/arm-trusted-firmware/rk3399/* builds/$(echo $board)/
  fi
# End ATF

  BINMAN_ALLOW_MISSING=1 %make_build $(echo $board)_defconfig O=builds/$(echo $board)/

# (tpg) add our distribution mark and some safe default configs
  sed -i -e '/^CONFIG_IDENT_STRING=".*"/ s/"$/  %{distribution}"/' builds/$(echo $board)/.config
  sed -i -e 's/.*CONFIG_SERIAL_PRESENT.*$/CONFIG_SERIAL_PRESENT=y/g' builds/$(echo $board)/.config
  sed -i -e 's/.*CONFIG_GZIP.*$/CONFIG_GZIP=y/g' builds/$(echo $board)/.config
  sed -i -e 's/.*CONFIG_CMD_UNZIP.*$/CONFIG_CMD_UNZIP=y/g' builds/$(echo $board)/.config

  BINMAN_ALLOW_MISSING=1 %make_build HOSTCC="%{__cc} %{optflags}" CROSS_COMPILE="" LDFLAGS="-fuse-ld=bfd" KBUILD_LDFLAGS="-fuse-ld=bfd" HOSTLDFLAGS="-fuse-ld=bfd" V=1 O=builds/$(echo $board)/
done

# build spi images for rockchip boards with SPI flash
  rkspi=(evb-rk3399 khadas-edge-captain-rk3399 khadas-edge-rk3399 khadas-edge-v-rk3399 nanopc-t4-rk3399 pinebook-pro-rk3399 rockpro64-rk3399 roc-pc-mezzanine-rk3399 roc-pc-rk3399)
  if [[ " ${rkspi[*]} " == *" $board "* ]]; then
    echo "Board: $board with SPI flash"
    builds/$(echo $board)/tools/mkimage -n rk3399 -T rkspi -d builds/$(echo $board)/tpl/u-boot-tpl.bin:builds/$(echo $board)/spl/u-boot-spl.bin builds/$(echo $board)/idbloader.spi
  fi
%endif

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/uboot/

%ifarch aarch64
for board in $(ls builds)
do
 mkdir -p %{buildroot}%{_datadir}/uboot/$(echo $board)/
 for file in u-boot.bin u-boot.dtb u-boot.img u-boot-dtb.img u-boot.itb u-boot-sunxi-with-spl.bin u-boot-rockchip.bin idbloader.img idbloader.spi spl/boot.bin spl/sunxi-spl.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) %{buildroot}%{_datadir}/uboot/$(echo $board)/
  fi
 done
done
%endif

# Bit of a hack to remove binaries we don't use as they're large
%ifarch aarch64
for board in $(ls builds)
do
  rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.dtb
  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot-sunxi-with-spl.bin ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot{,-dtb}.*
  fi
  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/MLO ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/SPL ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.imx ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot-spl.kwb ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.*
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot-spl.bin
  fi
  if [ -f %{buildroot}%{_datadir}/uboot/$(echo $board)/idbloader.img ]; then
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot.bin
    rm -f %{buildroot}%{_datadir}/uboot/$(echo $board)/u-boot{,-dtb}.img
  fi
done
%endif

for tool in bmp_logo dumpimage env/fw_printenv fit_check_sign fit_info gdb/gdbcont gdb/gdbsend gen_eth_addr gen_ethaddr_crc img2srec mkenvimage mkimage mksunxiboot ncb proftool sunxi-spl-image-builder ubsha1 xway-swap-bytes kwboot
do
    install -p -m 0755 builds/tools/$tool %{buildroot}%{_bindir}
done
install -p -m 0644 doc/mkimage.1 %{buildroot}%{_mandir}/man1

install -p -m 0755 builds/tools/env/fw_printenv %{buildroot}%{_bindir}
( cd %{buildroot}%{_bindir}; ln -sf fw_printenv fw_setenv )

# Copy some useful docs over
mkdir -p builds/docs
cp -p board/hisilicon/hikey/README builds/docs/README.hikey
cp -p board/rockchip/evb_rk3399/README builds/docs/README.evb_rk3399
cp -p board/sunxi/README.sunxi64 builds/docs/README.sunxi64
cp -p board/sunxi/README.nand builds/docs/README.sunxi-nand

%files
%doc README doc/develop/distro.rst doc/README.gpt
%doc doc/README.rockchip doc/develop/uefi doc/uImage.FIT doc/arch/arm64.rst
%doc builds/docs/* doc/board/amlogic/ doc/board/rockchip/
%{_bindir}/*
%doc %{_mandir}/man1/mkimage.1*
%dir %{_datadir}/uboot/

%ifarch aarch64
%files -n uboot-images-armv8
%{_datadir}/uboot/*
%endif
