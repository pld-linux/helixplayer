# TODO:
#  - check why do the hxplay.{png,desktop} files mysteriously disappear
#  - use system libpng, libjpeg, bzip2, zlib and maybe expat
Summary:	The Helix Player - Helix Community's open source media player for consumers
Summary(pl):	Helix Player - otwarty odtwarzacz multimediów Helix Community dla u¿ytkowników
Name:		helixplayer
Version:	1.0.1
Release:	0.1
License:	GPL
Group:		Applications/Multimedia
Source0:	https://helixcommunity.org/download.php/634/hxplay-%{version}.tar.bz2
# Source0-md5:	ca07ed001aae3eca6e5589c9313774cc
Patch0:		%{name}-system-libs.patch
URL:		https://player.helixcommunity.org/
BuildRequires:	gtk+2-devel
BuildRequires:	libogg-devel
BuildRequires:	libtheora-devel
BuildRequires:	libvorbis-devel
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	python-modules
Requires:	gtk+2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_helixplayerdir %{_libdir}/%{name}

%description
The Helix Player is the Helix Community's open source media player for
consumers.

%description -l pl
Helix Player to odtwarzacz multimediów Helix Community z otwartymi
¼ród³ami przeznaczony dla u¿ytkowników koñcowych.

%prep
%setup -q -n hxplay-%{version}
%patch0 -p1

%build
echo 'SetSDKPath("oggvorbissdk", "%{_prefix}")' > buildrc
export BUILDRC=`pwd`/buildrc

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_helixplayerdir},%{_pixmapsdir},%{_desktopdir},%{_bindir}}
cp -a player/installer/archive/temp/* $RPM_BUILD_ROOT%{_helixplayerdir}
rm -rf $RPM_BUILD_ROOT%{_helixplayerdir}/Bin
rm -rf $RPM_BUILD_ROOT%{_helixplayerdir}/postinst
#install player/installer/archive/temp/share/hxplay.desktop $RPM_BUILD_ROOT%{_desktopdir}
#install player/installer/archive/temp/share/hxplay.png $RPM_BUILD_ROOT%{_pixmapsdir}
install -d $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins
ln -sf ../../%{name}/mozilla/nphelix.so $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/nphelix.so
ln -sf ../../%{name}/mozilla/nphelix.xpt $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/nphelix.xpt
sed -i -e "s%#[ \t]*HELIX_LIBS[ \t]*=.*%HELIX_LIBS=%{_helixplayerdir} ; export HELIX_LIBS%" $RPM_BUILD_ROOT%{_helixplayerdir}/hxplay
ln -sf ../lib/%{name}/hxplay $RPM_BUILD_ROOT%{_bindir}/hxplay

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_helixplayerdir}
%attr(755,root,root) %{_bindir}/hxplay
%attr(755,root,root) %{_libdir}/mozilla/plugins/nphelix.so
%attr(755,root,root) %{_libdir}/mozilla/plugins/nphelix.xpt
#%{_desktopdir}/hxplay.desktop
#%{_pixmapsdir}/hxplay.png
%attr(755,root,root) %{_helixplayerdir}/hxplay
%attr(755,root,root) %{_helixplayerdir}/hxplay.bin
%{_helixplayerdir}/codecs
%attr(755,root,root) %{_helixplayerdir}/codecs/*
%{_helixplayerdir}/common
%attr(755,root,root) %{_helixplayerdir}/common/*
%{_helixplayerdir}/lib
%attr(755,root,root) %{_helixplayerdir}/lib/*
%{_helixplayerdir}/mozilla
%attr(755,root,root) %{_helixplayerdir}/mozilla/*
%attr(755,root,root) %{_helixplayerdir}/plugins
%{_helixplayerdir}/share
%{_helixplayerdir}/README
%{_helixplayerdir}/LICENSE
