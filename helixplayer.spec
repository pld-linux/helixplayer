Summary:	The Helix Player - Helix Community's open source media player for consumers
Summary(pl):	Helix Player - otwarty odtwarzacz multimediów Helix Community dla u¿ytkowników
Name:		helixplayer
%define	snap	20040402
Version:	0.2.0.0
Release:	0.%{snap}.1
License:	RPSL
Vendor:		Real Networks, Inc
Group:		Applications/Multimedia
#		http://forms.helixcommunity.org/helixdnaclient/
Source0:	http://software-dl.real.com/0499d41a473d2834d302/helix/%{snap}/player_inst-helix-player-%{snap}-source.zip
Source1:	helixplayer.desktop
URL:		https://player.helixcommunity.org/
BuildRequires:	python
BuildRequires:	python-momdules
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Helix Player is the Helix Community's open source media player for
consumers.

%description -l pl
Helix Player to odtwarzacz multimediów Helix Community z otwartymi
¼ród³ami przeznaczony dla u¿ytkowników koñcowych.

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
