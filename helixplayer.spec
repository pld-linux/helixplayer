Summary:	The Helix Player is the Helix Community's open source media player for consumers
Name:		helixplayer
%define	snap	20040402
Version:	0.2.0.0
Release:	0.%{snap}.1
Group:		Applications/Multimedia
License:	RPSL
Vendor:		Real Networks, Inc
URL:		https://player.helixcommunity.org/
#		http://forms.helixcommunity.org/helixdnaclient/
Source0:	http://software-dl.real.com/0499d41a473d2834d302/helix/%{snap}/player_inst-helix-player-%{snap}-source.zip
Source1:	helixplayer.desktop
BuildRequires:	unzip
BuildRequires:	python
BuildRequires:	python-momdules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Helix Player is the Helix Community's open source media player for
consumers.

%prep
%setup -q -n player_inst-helix-player-%{snap}

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
