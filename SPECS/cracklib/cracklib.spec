# Got this spec from http://downloads.sourceforge.net/cracklib/cracklib-2.9.6.tar.gz

Summary:          A password strength-checking library.
Name:             cracklib
Version:          2.9.7
Release:          2%{?dist}
Group:            System Environment/Libraries
Source:           cracklib-%{version}.tar.gz
%define sha1      cracklib-%{version}=ffe455aba4da8d49fcdbe6964aa35367a7438581
Source1:          cracklib-words-%{version}.gz
%define sha1      cracklib-words-%{version}=6491f1cc63233c678e9e5983f32ff98208d0b05a
URL:              http://sourceforge.net/projects/cracklib/
License:          GPL
Vendor:           VMware, Inc.
Distribution:     Photon
BuildRequires:    python3
BuildRequires:    python3-libs
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-xml
# cross compilation requires native dicts generating tools
%define BuildRequiresNative cracklib-dicts
Requires:         /bin/ln
Requires(post):   /bin/ln
Requires(postun): /bin/rm

%description
CrackLib tests passwords to determine whether they match certain
security-oriented characteristics. You can use CrackLib to stop
users from choosing passwords which would be easy to guess. CrackLib
performs certain tests:

* It tries to generate words from a username and gecos entry and
  checks those words against the password;
* It checks for simplistic patterns in passwords;
* It checks for the password in a dictionary.

CrackLib is actually a library containing a particular
C function which is used to check the password, as well as
other C functions. CrackLib is not a replacement for a passwd
program; it must be used in conjunction with an existing passwd
program.

Install the cracklib package if you need a program to check users'
passwords to see if they are at least minimally secure. If you
install CrackLib, you'll also want to install the cracklib-dicts
package.

%package    dicts
Summary:    The standard CrackLib dictionaries.
Group:      System Environment/Utilities
Requires:   cracklib

%description    dicts
The cracklib-dicts package includes the CrackLib dictionaries.
CrackLib will need to use the dictionary appropriate to your system,
which is normally put in /usr/share/dict/words.  Cracklib-dicts also contains
the utilities necessary for the creation of new dictionaries.

If you are installing CrackLib, you should also install cracklib-dicts.

%package devel
Summary:    Cracklib link library & header file
Group:      Development/Libraries
Requires:   cracklib

%description devel
The cracklib devel package include the needed library link and
header files for development.

%package -n python3-cracklib
Summary:    The cracklib python module
Group:      Development/Languages/Python
Requires:   cracklib
Requires:   python3
Requires:   python3-libs

%description -n python3-cracklib
The cracklib python3 module

%package lang
Summary:    The CrackLib language pack.
Group:      System Environment/Libraries

%description lang
The CrackLib language pack.

%prep
%autosetup -n cracklib-%{version}
chmod -R og+rX .
mkdir -p dicts
install %{SOURCE1} dicts/

%build
if [ %{_host} != %{_build} ]; then
export PYTHONXCPREFIX=/target-%{_arch}/usr
export CC=%{_host}-gcc
export LDSHARED='%{_host}-gcc -shared'
export LDFLAGS='-L/target-%{_arch}/usr/lib'
fi
export CFLAGS="$RPM_OPT_FLAGS"
%configure \
  --disable-static \
  --without-python
make %{_smp_mflags}
pushd python
python3 setup.py build
popd

%install
rm -rf %{buildroot}
make %{?_smp_mflags} install DESTDIR=%{buildroot}/
chmod 755 ./util/cracklib-format
chmod 755 ./util/cracklib-packer
if [ %{_host} = %{_build} ]; then
export PATH=./util:$PATH
fi
cracklib-format dicts/cracklib* | cracklib-packer %{buildroot}/%{_datadir}/cracklib/words
echo password | cracklib-packer %{buildroot}/%{_datadir}/cracklib/empty
rm -f %{buildroot}/%{_datadir}/cracklib/cracklib-small
ln -s cracklib-format %{buildroot}/%{_sbindir}/mkdict
ln -s cracklib-packer %{buildroot}/%{_sbindir}/packer

pushd python
python3 setup.py install --skip-build --root %{buildroot}
popd

%check
mkdir -p /usr/share/cracklib
cp %{buildroot}%{_datadir}/cracklib/* /usr/share/cracklib/
make %{?_smp_mflags} test

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
[ $1 = 1 ] || exit 0
echo "using empty dict to provide pw_dict" >&2
ln -sf empty.hwm %{_datadir}/cracklib/pw_dict.hwm
ln -sf empty.pwd %{_datadir}/cracklib/pw_dict.pwd
ln -sf empty.pwi %{_datadir}/cracklib/pw_dict.pwi

%triggerin -- cracklib-dicts
[ $2 = 1 ] || exit 0
echo "switching pw_dict to cracklib-dicts" >&2
ln -sf words.hwm %{_datadir}/cracklib/pw_dict.hwm
ln -sf words.pwd %{_datadir}/cracklib/pw_dict.pwd
ln -sf words.pwi %{_datadir}/cracklib/pw_dict.pwi

%triggerun -- cracklib-dicts
[ $2 = 0 ] || exit 0
echo "switching pw_dict to empty dict" >&2
ln -sf empty.hwm %{_datadir}/cracklib/pw_dict.hwm
ln -sf empty.pwd %{_datadir}/cracklib/pw_dict.pwd
ln -sf empty.pwi %{_datadir}/cracklib/pw_dict.pwi

%postun
/sbin/ldconfig
[ $1 = 0 ] || exit 0
rm -f %{_datadir}/cracklib/pw_dict.hwm
rm -f %{_datadir}/cracklib/pw_dict.pwd
rm -f %{_datadir}/cracklib/pw_dict.pwi

%files
%defattr(-,root,root)
%{_datadir}/cracklib/cracklib.magic
%{_datadir}/cracklib/empty*
%{_libdir}/libcrack.so.*

%files devel
%defattr(-,root,root)
%doc README README-DAWG doc
%{_includedir}/*
%{_libdir}/libcrack.so
%{_libdir}/libcrack.la

%files -n python3-cracklib
%defattr(-,root,root)
%{python3_sitelib}/*

%files dicts
%defattr(-,root,root)
%{_sbindir}/*
%{_datadir}/cracklib/words*

%files lang
%defattr(-,root,root)
%{_datadir}/locale/*

%changelog
*   Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.9.7-2
-   Update release to compile with python 3.10
*   Tue Jul 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.9.7-1
-   Automatic Version Bump
*   Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 2.9.6-10
-   Mass removal python2
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 2.9.6-9
-   Cross compilation support
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.6-8
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Sun Jun 04 2017 Bo Gan <ganb@vmware.com> 2.9.6-7
-   Fix script dependency
*   Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.6-6
-   Move python2 requires to python subpackage and added python3.
*   Thu Apr 13 2017 Bo Gan <ganb@vmware.com> 2.9.6-5
-   Fix CVE-2016-6318, trigger for cracklib-dicts
-   Trigger for dynamic symlink for dict
*   Sun Nov 20 2016 Alexey Makhalov <amakhalov@vmware.com> 2.9.6-4
-   Revert compressing pw_dict.pwd back. Python code
    cracklib.VeryFascistCheck does not handle it.
*   Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> 2.9.6-3
-   Remove any dicts from cracklib main package
-   Compress pw_dict.pwd file
-   Move doc folder to devel package
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.6-2
-   GA - Bump release of all rpms
*   Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 2.9.6-1
-   Updated to version 2.9.6
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.9.2-2
-   Updated group.
