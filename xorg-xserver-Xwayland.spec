#
# Conditional build:
%bcond_without	eglstream	# XWayland eglstream support
%bcond_without	glamor		# glamor dix module
%bcond_with	xcsecurity	# XC-SECURITY extension (deprecated)
%bcond_with	xf86bigfont	# XF86BigFont extension
%bcond_without	xselinux	# XSELINUX extension
%bcond_without	libunwind	# libunwind for backtracing
%bcond_with	systemtap	# systemtap/dtrace probes

Summary:	Xwayland - X server integrated into a Wayland window system
Summary(pl.UTF-8):	Xwayland - serwer X integrowalny w Wayland
Name:		xorg-xserver-Xwayland
Version:	21.1.1
Release:	0.1
License:	MIT
Group:		X11/Servers
Source0:	https://xorg.freedesktop.org/releases/individual/xserver/xwayland-%{version}.tar.xz
# Source0-md5:	693c0ef588a0f8d73a959b41230ddbda
URL:		https://xorg.freedesktop.org/
%{?with_glamor:BuildRequires:	Mesa-libgbm-devel >= 10.2}
%{?with_eglstream:BuildRequires:	egl-wayland-devel}
BuildRequires:	libbsd-devel
BuildRequires:	libdrm-devel >= 2.4.89
%{?with_glamor:BuildRequires:	libepoxy-devel}
# also possible: libsha, nettle, openssl
BuildRequires:	libgcrypt-devel
%{?with_xselinux:BuildRequires:	libselinux-devel >= 2.0.86}
%{?with_libunwind:BuildRequires:	libunwind-devel}
BuildRequires:	meson >= 0.46.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pixman-devel
BuildRequires:	rpmbuild(macros) >= 1.736
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
BuildRequires:	tar >= 1:1.22
# wayland-client
BuildRequires:	wayland-devel >= 1.3.0
BuildRequires:	wayland-protocols >= 1.18
BuildRequires:	xorg-lib-libXdmcp-devel
BuildRequires:	xorg-lib-libXext-devel >= 1.0.99.4
BuildRequires:	xorg-lib-libXfont2-devel >= 2.0
BuildRequires:	xorg-lib-libxkbfile-devel
BuildRequires:	xorg-lib-libxshmfence-devel >= 1.1
BuildRequires:	xorg-lib-xtrans-devel >= 1.3.5
BuildRequires:	xorg-proto-bigreqsproto-devel >= 1.1.0
BuildRequires:	xorg-proto-compositeproto-devel >= 0.4
BuildRequires:	xorg-proto-damageproto-devel >= 1.1
BuildRequires:	xorg-proto-dri3proto-devel >= 1.2
BuildRequires:	xorg-proto-fixesproto-devel >= 5.0
BuildRequires:	xorg-proto-fontsproto-devel >= 2.1.3
BuildRequires:	xorg-proto-inputproto-devel >= 2.3
BuildRequires:	xorg-proto-kbproto-devel >= 1.0.3
BuildRequires:	xorg-proto-recordproto-devel >= 1.13.99.1
BuildRequires:	xorg-proto-randrproto-devel >= 1.6.0
BuildRequires:	xorg-proto-renderproto-devel >= 0.11
BuildRequires:	xorg-proto-resourceproto-devel >= 1.2.0
BuildRequires:	xorg-proto-scrnsaverproto-devel >= 1.1
BuildRequires:	xorg-proto-videoproto-devel
BuildRequires:	xorg-proto-xcmiscproto-devel >= 1.2.0
BuildRequires:	xorg-proto-xextproto-devel >= 7.2.99.901
%{?with_xf86bigfont:BuildRequires:	xorg-proto-xf86bigfontproto-devel >= 1.2.0}
BuildRequires:	xorg-proto-xf86vidmodeproto-devel >= 2.2.99.1
BuildRequires:	xorg-proto-xineramaproto-devel
BuildRequires:	xorg-proto-xproto-devel >= 7.0.31
BuildRequires:	xz
%{?with_glamor:Requires:	Mesa-libgbm >= 10.2}
Requires:	libdrm >= 2.4.89
%{?with_xselinux:Requires:	libselinux >= 2.0.86}
Requires:	wayland >= 1.3.0
Requires:	xorg-app-xkbcomp
Requires:	xorg-lib-libXext >= 1.0.99.4
Requires:	xorg-lib-libXfont2 >= 2.0
Requires:	xorg-lib-libxshmfence >= 1.1
# for protocol.txt
Requires:	xorg-xserver-common >= 1.20
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Xwayland - server integrated into a Wayland window system.

%description -l pl.UTF-8
Xwayland - serwer X integrowalny w Wayland.

%prep
%setup -q -n xwayland-%{version}

%build
%meson build \
	-Dbuilder_addr="feedback@pld-linux.org" \
	-Dbuilder_string="%{name}-%{version}-%{release}" \
	-Ddefault_font_path="%{_fontsdir}/misc,%{_fontsdir}/TTF,%{_fontsdir}/OTF,%{_fontsdir}/Type1,%{_fontsdir}/100dpi,%{_fontsdir}/75dpi" \
	%{?with_systemtap:-Ddtrace=true} \
	%{!?with_glamor:-Dglamor=false} \
	%{?with_libunwind:-Dlibunwind=true} \
	-Dsha1=libgcrypt \
	-Dvendor_name="PLD Linux" \
	%{?with_xcsecurity:-Dxcsecurity=true} \
	%{?with_xf86bigfont:-Dxf86bigfont=true} \
	-Dxkb_bin_dir=%{_bindir} \
	-Dxkb_dir=%{_datadir}/X11/xkb \
	-Dxkb_output_dir=/var/lib/xkb \
	%{!?with_xselinux:-Dxselinux=false} \
	%{!?with_eglstream:-Dxwayland_eglstream=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# xorg-xserver-common package (common dependency for Xwayland and Xorg)
%{__rm} $RPM_BUILD_ROOT%{_libdir}/xorg/protocol.txt
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/Xserver.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_bindir}/Xwayland
%{_pkgconfigdir}/xwayland.pc
%{_mandir}/man1/Xwayland.1*
