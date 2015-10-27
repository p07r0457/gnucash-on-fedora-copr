Name: gnucash-docs
Summary: Help files and documentation for the GnuCash personal finanace manager
Version: 2.6.9
URL: http://gnucash.org/
Release: 1%{?dist}
License: GFDL
Group: Applications/Productivity
Source: gnucash-docs-maint.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArchitectures: noarch
BuildRequires: gettext, libtool, intltool
BuildRequires: libxslt
Requires: yelp

%description
GnuCash is a personal finance manager. gnucash-docs contains the
help files and documentation for GnuCash.

%prep
%setup -q
./autogen.sh

%build
touch configure.ac aclocal.m4 Makefile.in configure gnucash-docs.spec
%configure --without-scrollkeeper
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -rf	$RPM_BUILD_ROOT/var/scrollkeeper

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/gnome/help/*
%doc AUTHORS ChangeLog* HACKING NEWS README
%license COPYING*

%pretrans -p <lua>
for _,d in pairs ({"gnucash-guide", "gnucash-help"}) do
  path = "%{_datadir}/gnome/help/" .. d
  if posix.stat(path, "type") == "link" then
    os.remove(path)
    posix.mkdir(path)
  end
end
return 0

%changelog
* Wed Oct  7 2015 Bill Nottingham <notting@splat.cc> - 2.6.9-1
- update to 2.6.9

* Tue Oct  6 2015 Bill Nottingham <notting@splat.cc> - 2.6.8-1
- update to 2.6.8

* Mon Jun 29 2015 Bill Nottingham <notting@splat.cc> - 2.6.7-1
- update to 2.6.7

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr  1 2015 Bill Nottingham <notting@splat.cc> - 2.6.6-1
- update to 2.6.6

* Thu Jan  8 2015 Bill Nottingham <notting@splat.cc> - 2.6.5-1
- update to 2.6.5

* Tue Sep 30 2014 Bill Nottingham <notting@splat.cc> - 2.6.4-1
- update to 2.6.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr  3 2014 Bill Nottingham <notting@splat.cc> - 2.6.3-1
- update to 2.6.3

* Mon Mar 10 2014 Bill Nottingham <notting@splat.cc> - 2.6.2-1
- update to 2.6.2

* Mon Jan 27 2014 Bill Nottingham <notting@redhat.com> - 2.6.1-1
- update to 2.6.1

* Tue Jan 21 2014 Bill Nottingham <notting@redhat.com> - 2.6.0-2
- fix install (#1056046)

* Thu Jan 16 2014 Bill Nottingham <notting@redhat.com> - 2.6.0-1
- update to 2.6.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 24 2013 Bill Nottingham <notting@redhat.com> - 2.4.2-1
- update to 2.4.2
- drop scrollkeeper bits

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 05 2011 Bill Nottingham <notting@redhat.com> - 2.4.1-1
- update to 2.4.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 29 2007 Bill Nottingham <notting@redhat.com> - 2.2.0-2
- gnucash multilib fixes (#341331, #357161, #246382)

* Mon Jul 16 2007 Bill Nottingham <notting@redhat.com> - 2.2.0-1
- update to 2.2.0

* Tue Feb 13 2007 Bill Nottingham <notting@redhat.com> - 2.0.1-2
- move yelp requirement from gnucash to here

* Thu Feb  1 2007 Bill Nottingham <notting@redhat.com> - 2.0.1-1
- fork off from main gnucash package
