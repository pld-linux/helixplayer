Summary:	The Helix Player - Helix Community's open source media player for consumers
Summary(pl):	Helix Player - otwarty odtwarzacz multimedi�w Helix Community dla u�ytkownik�w
Name:		helixplayer
%define	snap	20040615
Version:	1.0
Release:	0.%{snap}.1
License:	RPSL
Vendor:		Real Networks, Inc
Group:		Applications/Multimedia
#		http://forms.helixcommunity.org/helixdnaclient/
Source0:	https://helixcommunity.org/download.php/487/helixplayer1.0-beta-source.tar.bz2
# Source0-md5:	e8148f6dd290752cf628d522dc6c0211
#Source1:	helixplayer.desktop
URL:		https://player.helixcommunity.org/
BuildRequires:	python
BuildRequires:	python-modules
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Helix Player is the Helix Community's open source media player for
consumers.

%description -l pl
Helix Player to odtwarzacz multimedi�w Helix Community z otwartymi
�r�d�ami przeznaczony dla u�ytkownik�w ko�cowych.

%prep
%setup -q -n player_all-bingo-beta-%{snap}

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
