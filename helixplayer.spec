Summary:	The Helix Player - Helix Community's open source media player for consumers
Summary(pl):	Helix Player - otwarty odtwarzacz multimediów Helix Community dla u¿ytkowników
Name:		helixplayer
Version:	1.0.6
Release:	4
License:	RPSL or GPL v2+
Group:		Applications/Multimedia
#Source0Download: https://helixcommunity.org/project/showfiles.php?group_id=154
Source0:	https://helixcommunity.org/download.php/1585/hxplay-%{version}.tar.bz2
# Source0-md5:	824183372ea84570444fe946b43afac4
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-morearchs.patch
Patch2:		%{name}-desktop.patch
URL:		https://player.helixcommunity.org/
BuildRequires:	gtk+2-devel >= 2.0.0
BuildRequires:	libogg-devel
BuildRequires:	libpng-devel >= 2:1.2.5
BuildRequires:	libtheora-devel
BuildRequires:	libvorbis-devel
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel >= 1.1.4
Provides:	helix-core
# i386 lacks atomic add instruction
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_helixplayerdir %{_libdir}/%{name}

%description
The Helix Player is the Helix Community's open source media player for
consumers.

%description -l pl
Helix Player to odtwarzacz multimediów Helix Community z otwartymi
¼ród³ami przeznaczony dla u¿ytkowników koñcowych.

%package -n browser-plugin-%{name}
Summary:	Helix Player plugin for WWW browsers
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})
Conflicts:	helixplayer < 1.0.6-3.1

%description -n browser-plugin-%{name}
Helix Player plugin for WWW browsers.

%prep
%setup -q -n hxplay-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# expat is modified (based on mozilla?)
# libjpeg is compiled with different config (BGRx instead of RGB)
# so only these can be replaced by system ones
rm -rf common/import/{bzip2,zlib} datatype/image/png/import/libpng

sed -i -e "s/'gcc'/'%{__cc}'/;s/'g++'/'%{__cxx}'/;s/'-O2'/'%{rpmcflags}'/" build/umakecf/gcc.cf

%build
echo 'SetSDKPath("oggvorbissdk", "%{_prefix}")' > buildrc
export BUILDRC=`pwd`/buildrc
export BUILD_ROOT=`pwd`/build
# make threads - maybe parse make -j?
export RIBOSOME_THREADS=1
PATH="$PATH:`pwd`/build/bin"
python build/bin/build \
	-m hxplay_gtk_release \
	-P helix-client-all-defines-free \
	%{!?debug:-t release} \
	player_all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_helixplayerdir},%{_pixmapsdir},%{_desktopdir},%{_bindir}}

cp -a player/installer/archive/temp/* $RPM_BUILD_ROOT%{_helixplayerdir}
rm -rf $RPM_BUILD_ROOT%{_helixplayerdir}/Bin
rm -rf $RPM_BUILD_ROOT%{_helixplayerdir}/postinst
install player/installer/archive/temp/share/hxplay.desktop $RPM_BUILD_ROOT%{_desktopdir}
install player/installer/archive/temp/share/hxplay.png $RPM_BUILD_ROOT%{_pixmapsdir}

install -d $RPM_BUILD_ROOT%{_browserpluginsdir}
mv $RPM_BUILD_ROOT{%{_libdir}/%{name}/mozilla,%{_browserpluginsdir}}/nphelix.so
mv $RPM_BUILD_ROOT{%{_libdir}/%{name}/mozilla,%{_browserpluginsdir}}/nphelix.xpt

sed -i -e "s%#[ \t]*HELIX_LIBS[ \t]*=.*%HELIX_LIBS=%{_helixplayerdir} ; export HELIX_LIBS%" $RPM_BUILD_ROOT%{_helixplayerdir}/hxplay
ln -sf %{_libdir}/%{name}/hxplay $RPM_BUILD_ROOT%{_bindir}/hxplay

%clean
rm -rf $RPM_BUILD_ROOT

%post -n browser-plugin-%{name}
%update_browser_plugins

%postun -n browser-plugin-%{name}
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hxplay
%dir %{_helixplayerdir}
%attr(755,root,root) %{_helixplayerdir}/hxplay
%attr(755,root,root) %{_helixplayerdir}/hxplay.bin
%attr(755,root,root) %{_helixplayerdir}/codecs
%attr(755,root,root) %{_helixplayerdir}/common
%attr(755,root,root) %{_helixplayerdir}/lib
%dir %{_helixplayerdir}/plugins
%attr(755,root,root) %{_helixplayerdir}/plugins/*.so
%{_helixplayerdir}/share
%{_helixplayerdir}/README
%{_helixplayerdir}/LICENSE
%{_desktopdir}/hxplay.desktop
%{_pixmapsdir}/hxplay.png

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/nphelix.so
%{_browserpluginsdir}/nphelix.xpt
