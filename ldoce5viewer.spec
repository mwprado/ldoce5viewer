%global date 20180309
%global commit0 377ff489260ffbdfd9255363dae3e5ed021bf243
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           ldoce5viewer
Version:        0
Release:        9.%{date}git%{shortcommit0}%{?dist}
Summary:        Viewer Application for the Longman Dictionary (LDOCE 5)
License:        GPLv3+ and Public Domain
URL:            https://forward-backward.co.jp/ldoce5viewer/
Source:         https://github.com/ciscorn/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{version}-%{date}git%{shortcommit0}.tar.gz
# Remove autogenerated file
# Upstream ref: https://github.com/ciscorn/ldoce5viewer/pull/68
Patch0:         https://patch-diff.githubusercontent.com/raw/ciscorn/ldoce5viewer/pull/68.patch#/%{name}-remove-autogenerated-file.patch
# Port to QT5
# https://github.com/ciscorn/ldoce5viewer/pull/69
Patch1:         https://patch-diff.githubusercontent.com/raw/ciscorn/ldoce5viewer/pull/69.patch#/%{name}-port-to-qt5.patch

BuildArch:      noarch

BuildRequires:  /usr/bin/git
BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel
BuildRequires:  python3dist(whoosh)
BuildRequires:  python3dist(lxml)
BuildRequires:  python3-qt5-devel
BuildRequires:  libappstream-glib
# Required to regenerate icons
BuildRequires:  ImageMagick
BuildRequires:  inkscape
BuildRequires:  python3dist(pillow)

Requires:       python3-gstreamer1
Requires:       gstreamer1-plugins-good
Requires:       gstreamer1-plugins-ugly
Requires:       hicolor-icon-theme
Requires:       python3-qt5-webkit
Requires:       python3dist(whoosh)
Requires:       python3dist(lxml)


%description
The %{name} is an alternative dictionary viewer for the
Longman Dictionary of Contemporary English 5th Edition (LDOCE 5).

Features:
    - Comprehensive instant search.
    - Pleasant to use.
    - Clean and readable.
    - Full sound playback.
    - Access virtually all of the LDOCE content.
    - Powerful advanced search.
    - Search in definitions and example sentences.
    - Clipboard monitoring.

Note: Before you can use the app, you have to install
      the original LDOCE 5 software from the DVD-ROM.


%prep
%autosetup -S git -n %{name}-%{commit0}

# Update the software version.
sed -i "s#\(__version__.*\ =\ \).*#\1'%{date}'#" %{name}/__init__.py

# Shebang removal
for i in %{name}/__init__.py %{name}/utils/compat.py %{name}.desktop; do
 sed '1{\@^#!/usr/bin/env@d}' $i > $i.tmp &&
 touch -r $i $i.tmp &&
 mv $i.tmp $i
done

# Be sure all necessary files will be regenerated.
make clean
make -C %{name}/qtgui/resources/icons clean

# Correct EOL (preserve timestamps).
for i in COPYING.txt LICENSE.txt; do
    sed 's#\r##g' $i > $i.tmp && \
    touch -r $i $i.tmp && \
    mv $i.tmp $i
done

# Create simple installation instruction.
cat  > INSTALL.txt <<EOF
1. Copy the 'ldoce5.data' directory from the LDOCE5 DVD-ROM [1]
   to an arbitrary location.

2. Start the %{name}

3. The application will ask you the location where you put 'ldoce5.data'.

More information can be obtained from [2].

[1] http://www.longmandictionariesonline.com/
[2] https://forward-backward.co.jp/ldoce5viewer/
EOF


%build
%make_build -C %{name}/qtgui/resources/icons
%make_build qtui qtresource
%py3_build


%install
%py3_install

# install desktop file
desktop-file-install \
    --delete-original \
    --dir=%{buildroot}%{_datadir}/applications \
    %{name}.desktop

# install icon file
install -p -m 0644 -D %{name}/qtgui/resources/%{name}.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# install and validate appdata
install -p -m 0644 -D %{name}.appdata.xml %{buildroot}/%{_datadir}/appdata/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml


%files
%doc INSTALL.txt README.md
%license COPYING.txt LICENSE.txt
%{_bindir}/%{name}
%{python3_sitelib}/*
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/*.appdata.xml
%exclude %{python3_sitelib}/%{name}/qtgui/ui/Makefile
%exclude %{python3_sitelib}/%{name}/qtgui/resources/Makefile
%exclude %{python3_sitelib}/%{name}/qtgui/resources/icons/Makefile
%exclude %{python3_sitelib}/%{name}/qtgui/resources/icons/icongen.*


%changelog
* Sat Aug 24 2019 Leigh Scott <leigh123linux@gmail.com> - 0-9.20180309git377ff48
- Rebuild for python-3.8

* Mon Aug 12 2019 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0-8.20180309git377ff48
- Drop gstreamer-0.10 dependencies (rfbz#5354).

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0-7.20180309git377ff48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 06 2019 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0-6.20180309git377ff48
- Drop patches merged upstream,
- Switch to used python3 and qt5.

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0-5.20170216git4b52afb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0-4.20170216git4b52afb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0-3.20170216git4b52afb
- Add patch to remove 0-sized and unused files.

* Tue Feb 27 2018 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0-2.20170216git4b52afb
- Modernize spec file,
- Update to the latest version.

* Fri May 23 2014 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0-1.20140224
- Initial RPM release.
