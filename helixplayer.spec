# NOTE
# - worth reading proably: https://player.helixcommunity.org/2004/developer/gtk/quickstart
#
Summary:	The Helix Player - Helix Community's open source media player for consumers
Summary(pl.UTF-8):	Helix Player - otwarty odtwarzacz multimediów Helix Community dla użytkowników
Name:		helixplayer
Version:	1.0.9
Release:	2
License:	RPSL or GPL v2+
Group:		Applications/Multimedia
# Source0Download: https://helixcommunity.org/frs/?group_id=154
Source0:	https://helixcommunity.org/frs/download.php/2490/hxplay-%{version}-source.tar.bz2
# Source0-md5:	346eb87dea413562875aca69a05370ec
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-cflags.patch
Patch3:		%{name}-sem_t.patch
Patch4:		%{name}-bzip2.patch
Patch5:		%{name}-morearchs.patch
Patch6:		%{name}-gcc.patch
URL:		https://player.helixcommunity.org/
BuildRequires:	gtk+2-devel >= 1:2.0.0
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

%description
The Helix Player is the Helix Community's open source media player for
consumers.

%description -l pl.UTF-8
Helix Player to odtwarzacz multimediów Helix Community z otwartymi
źródłami przeznaczony dla użytkowników końcowych.

%package -n browser-plugin-%{name}
Summary:	Helix Player plugin for WWW browsers
Summary(pl.UTF-8):	Helix Player jako wtyczka dla przeglądarek WWW
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})
Conflicts:	helixplayer < 1.0.6-3.1

%description -n browser-plugin-%{name}
Helix Player plugin for WWW browsers.

%description -n browser-plugin-%{name} -l pl.UTF-8
Helix Player jako wtyczka dla przeglądarek WWW.

%prep
%setup -q -n hxplay-%{version}
%{__sed} -i -e 's,\r$,,' build/build/BIF/build.bif
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# expat is modified (based on mozilla?)
# libjpeg is compiled with different config (BGRx instead of RGB)
# so only these can be replaced by system ones
#rm -rf common/import/{bzip2,zlib} datatype/image/png/import/libpng

#mkdir -p common/import/bzip2/rel/bzip2
#ln -s common/import/bzip2/rel/bzip2

# duplicate. just avoid confusion and remove it
rm build/BIF/build.bif

echo 'SetSDKPath("oggvorbissdk", "/usr")' > buildrc

%build
%ifarch %{ix86}
export SYSTEM_ID=linux-2.6-glibc23-i386
%endif
%ifarch %{x8664}
export SYSTEM_ID=linux-2.6-glibc23-amd64
%endif
%ifarch sparc sparc64
export SYSTEM_ID=linux-2.2-libc6-sparc
%endif
%ifarch ppc
export SYSTEM_ID=linux-2.2-libc6-gcc32-powerpc
%endif
%ifarch ppc64
export SYSTEM_ID=linux-powerpc64
%endif
%ifarch alpha
export SYSTEM_ID=linux-2.2-libc6-gcc32-alpha
%endif

export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export CXX="%{__cxx}"
export CXXFLAGS="%{rpmcxxflags}"
export LD="%{__cxx}"
export LDFLAGS="%{rpmldflags}"

pwd=$(pwd)
export BUILDRC=$pwd/buildrc
export BUILD_ROOT=$pwd/build
# make threads - maybe parse make -j?
export RIBOSOME_THREADS=1
PATH="$PATH:$pwd/build/bin"
python build/bin/build.py \
	-m hxplay_gtk_release \
	-P helix-client-all-defines-free \
	-p green -v -n \
	%{!?debug:-t release} \
	player_installer_archive

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/%{name}/share,%{_pixmapsdir},%{_desktopdir},%{_bindir}}

cp -a player/installer/archive/temp/{codecs,common,lib,plugins} $RPM_BUILD_ROOT%{_libdir}/%{name}
install player/installer/archive/temp/hxplay.bin $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -a player/installer/archive/temp/share/{default,icons,hxplay*,*.css} $RPM_BUILD_ROOT%{_libdir}/%{name}/share
install player/installer/common/hxplay.desktop $RPM_BUILD_ROOT%{_desktopdir}
install player/app/gtk/res/hxplay.png $RPM_BUILD_ROOT%{_pixmapsdir}

# messed
for d in player/installer/archive/temp/share/locale/* ; do
	install -d $RPM_BUILD_ROOT%{_datadir}/locale/$(basename $d)/LC_MESSAGES
	cp $d/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/$(basename $d)/LC_MESSAGES
done

install -d $RPM_BUILD_ROOT%{_browserpluginsdir}
cp -a release/nphelix.* $RPM_BUILD_ROOT%{_browserpluginsdir}

sed -e "s,#[ \t]*HELIX_LIBS[ \t]*=.*,HELIX_LIBS=%{_libdir}/%{name}; export HELIX_LIBS," \
	player/installer/archive/temp/hxplay > $RPM_BUILD_ROOT%{_libdir}/%{name}/hxplay
chmod a+rx $RPM_BUILD_ROOT%{_libdir}/%{name}/hxplay
ln -sf %{_libdir}/%{name}/hxplay $RPM_BUILD_ROOT%{_bindir}/hxplay

%find_lang player
%find_lang widget
cat player.lang widget.lang > %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post -n browser-plugin-%{name}
%update_browser_plugins

%postun -n browser-plugin-%{name}
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hxplay
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/hxplay
%attr(755,root,root) %{_libdir}/%{name}/hxplay.bin
%attr(755,root,root) %{_libdir}/%{name}/codecs
%attr(755,root,root) %{_libdir}/%{name}/common
%attr(755,root,root) %{_libdir}/%{name}/lib
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so
%{_libdir}/%{name}/share
%{_desktopdir}/hxplay.desktop
%{_pixmapsdir}/hxplay.png

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/nphelix.so
%{_browserpluginsdir}/nphelix.xpt
