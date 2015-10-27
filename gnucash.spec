Name: gnucash
Summary: Finance management application
Version: 2.6.9
URL: http://gnucash.org/
Release: 1%{?dist}
License: GPLv2+
Group: Applications/Productivity
Source: gnucash-maint.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: webkitgtk-devel, libxml2 >= 2.5.10, libxslt-devel, zlib-devel
BuildRequires: libgsf-devel >= 1.12.2, goffice-devel < 0.9, swig
BuildRequires: libglade2-devel >= 2.4, libgnomeui-devel >= 2.4
BuildRequires: libofx-devel, aqbanking-devel, guile-devel >= 5:2.0
BuildRequires: desktop-file-utils, texinfo
BuildRequires: gettext, libtool, intltool
BuildRequires: python-devel, libdbi-devel
BuildRequires: libdbi-dbd-mysql, libdbi-dbd-pgsql, libdbi-dbd-sqlite
BuildRequires: libtool-ltdl-devel
BuildRequires: ktoblzcheck-devel
BuildRequires: libsecret-devel
BuildRequires: libappstream-glib

Requires: gnucash-docs >= 2.2.0
Requires: dconf
Requires: perl(Finance::Quote)
%if 0%{?fedora} <= 14 && 0%{?rhel} <= 6
# for HBCI setup wizard
Requires: aqbanking
%endif
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Obsoletes: gnucash-backend-postgres

%description
GnuCash is a personal finance manager. A check-book like register GUI
allows you to enter and track bank accounts, stocks, income and even
currency trades. The interface is designed to be simple and easy to
use, but is backed with double-entry accounting principles to ensure
balanced books.

%prep
%setup -q
find src/quotes -name "*.in" -exec sed -i "s|use lib '@-PERLINCL-@';||g" {} \;
./autogen.sh

%build
sed -i 's|get_python_lib(0|get_python_lib(1|g' configure
%configure  --enable-error-on-warning=no \
	--enable-ofx \
	--enable-aqbanking \
	--with-html-engine=webkit \
	--enable-locale-specific-tax \
	--enable-dbi \
	--disable-static \
	--docdir=%{_datadir}/doc/gnucash-%{version} \
	--enable-python \
	BUILDING_FROM_VCS=yes

#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
#sed -i 's|^link_all_deplibs=no|link_all_deplibs=unknown|g' libtool

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Update the screenshot shown in the software center
#
# NOTE: It would be *awesome* if this file was pushed upstream.
#
# See http://people.freedesktop.org/~hughsient/appdata/#screenshots for more details.
#
if appstream-util --help | grep -q replace-screenshots ; then
  appstream-util replace-screenshots $RPM_BUILD_ROOT%{_datadir}/appdata/gnucash.appdata.xml \
    https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/gnucash/a.png
fi
%find_lang %{name}

# vfolder desktop file install stuff
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/applications/
desktop-file-install --delete-original \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	$RPM_BUILD_ROOT%{_datadir}/applications/gnucash.desktop

mv $RPM_BUILD_ROOT/%{_libdir}/lib* $RPM_BUILD_ROOT/%{_libdir}/gnucash

rm -rf $RPM_BUILD_ROOT/%{_infodir} \
	$RPM_BUILD_ROOT/%{_includedir} \
	$RPM_BUILD_ROOT/%{_datadir}/aclocal \
	$RPM_BUILD_ROOT/%{_libdir}/lib*.a \
	$RPM_BUILD_ROOT/%{_libdir}/gnucash/lib*.a \
	$RPM_BUILD_ROOT/%{_bindir}/gnc-test-env \
	$RPM_BUILD_ROOT/%{_bindir}/gnc-fq-update

find $RPM_BUILD_ROOT/%{_libdir} -name *.la -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    [ -x /usr/bin/gtk-update-icon-cache ] && /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%defattr(-,root,root)
%docdir %{_datadir}/doc/gnucash-%{version}
%license COPYING
%{_datadir}/doc/gnucash-%{version}
%dir %{_sysconfdir}/gnucash
%{_bindir}/*
%{_libexecdir}/gnucash
%{_libdir}/*
%exclude /usr/lib/debug
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/gnucash
%{_datadir}/appdata/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man*/*
%{python_sitearch}/gnucash
%config(noreplace) %{_sysconfdir}/gnucash/*

%changelog
* Wed Oct  7 2015 Bill Nottingham <notting@splat.cc> - 2.6.9-1
- update to 2.6.9

* Tue Oct  6 2015 Bill Nottingham <notting@splat.cc> - 2.6.8-1
- update to 2.6.8 (#1266794)

* Mon Jun 29 2015 Bill Nottingham <notting@splat.cc> - 2.6.7-1
- update to 2.6.7 (#1236432)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 31 2015 Bill Nottingham <notting@splat.cc> - 2.6.6-1
- update to 2.6.6 (#1207447)

* Mon Mar 30 2015 Richard Hughes <rhughes@redhat.com> - 2.6.5-2
- Use better AppData screenshots

* Thu Jan  8 2015 Bill Nottingham <notting@splat.cc> - 2.6.5-1
- update to 2.6.5 (#1176892) which fixes guile cache issues (#1151870) and charts (#1157203)

* Tue Sep 30 2014 Bill Nottingham <notting@splat.cc> - 2.6.4-1
- update to 2.6.4 (#1147844, #1123943, #1116500)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr  3 2014 Bill Nottingham <notting@splat.cc> - 2.6.3-1
- update to 2.6.3 (#1082288)

* Mon Mar 10 2014 Bill Nottingham <notting@splat.cc> - 2.6.2-1
- update to 2.6.2 (#1071911)

* Mon Jan 27 2014 Bill Nottingham <notting@redhat.com> - 2.6.1-1
- update to 2.6.1 (#1057990)
- add dconf requires (#1058218)

* Tue Jan 21 2014 Bill Nottingham <notting@redhat.com> - 2.6.0-3
- fix %%postun (#1056721)
- rebuild for libdbi

* Fri Jan 17 2014 Bill Nottingham <notting@redhat.com> - 2.6.0-2
- package upstream appdata file

* Thu Jan 16 2014 Bill Nottingham <notting@redhat.com> - 2.6.0-1
- update to 2.6.0

* Mon Sep 23 2013 Bill Nottingham <notting@redhat.com> - 2.4.13-5
- rebuild against new libofx

* Tue Sep  3 2013 Bill Nottingham <notting@redhat.com> - 2.4.13-4
- add appstream metadata from upstream git head

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.4.13-2
- Perl 5.18 rebuild

* Tue Apr 23 2013 Bill Nottingham <notting@redhat.com> - 2.4.13-1
- update to 2.4.13

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Bill Nottingham <notting@redhat.com> - 2.4.11-1
- update to 2.4.11

* Tue Jul 10 2012 Bill Nottingham <notting@redhat.com> - 2.4.10-2
- rebuild for ofx ABI bump

* Wed Feb 29 2012 Bill Nottingham <notting@redhat.com> - 2.4.10-1
- update to 2.4.10
- enable ktobzlcheck support (#783849)

* Thu Jan 19 2012 Bill Nottingham <notting@redhat.com> - 2.4.9-1
- update to 2.4.9

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 25 2011 Bill Nottingham <notting@redhat.com> - 2.4.8-1
- update to 2.4.8

* Fri Oct 14 2011 Bill Nottingham <notting@redhat.com> - 2.4.7-4
- update the last fix (#703249, #742202, #744310)

* Tue Oct 11 2011 Bill Nottingham <notting@redhat.com> - 2.4.7-3
- when scanning modules, don't unload them (#703249, #742202, #744310)

* Tue Aug  9 2011 Bill Nottingham <notting@redhat.com> - 2.4.7-2
- fix python bindings on 64bit (#729454)

* Wed Jul  6 2011 Bill Nottingham <notting@redhat.com> - 2.4.7-1
- update to 2.4.7 (#712268)

* Mon Jun 13 2011 Bill Nottingham <notting@redhat.com> - 2.4.5-4
- re-enable python bindings (#712621)

* Fri May 13 2011 Bill Nottingham <notting@redhat.com> - 2.4.5-3
- fix it to at least compile with guile-2.0 (does not work yet) (#704527)

* Thu May  5 2011 Bill Nottingham <notting@redhat.com> - 2.4.5-2
- fix tips (#702391)

* Tue Apr 19 2011 Bill Nottingham <notting@redhat.com> - 2.4.5-1
- update to 2.4.5

* Fri Mar 18 2011 Bill Nottingham <notting@redhat.com> - 2.4.4-2
- fix configure.ac to correctly use WEBKIT_LIBS from pkg-config (#670001, <q3aiml@gmail.com>)

* Wed Mar 16 2011 Bill Nottingham <notting@redhat.com> - 2.4.4-1
- update to 2.4.4

* Thu Mar  3 2011 Bill Nottingham <notting@redhat.com> - 2.4.3-1
- update to 2.4.3

* Fri Feb 11 2011 Bill Nottingham <notting@redhat.com> - 2.4.2-1
- update to 2.4.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Bill Nottingham <notting@redhat.com> - 2.4.0-3
- don't ship gnc-fq-update; updates should be handled by normal packaging

* Wed Jan 12 2011 Bill Nottingham <notting@redhat.com> - 2.4.0-2
- remove 'this is a development version' warning

* Mon Jan  3 2011 Bill Nottingham <notting@redhat.com> - 2.4.0-1
- update to 2.4.0

* Thu Oct 21 2010 Bill Nottingham <notting@redhat.com>
- don't ship gnc-test-env (#644933, CVE-2010-3999)

* Mon Aug 23 2010 Bill Nottingham <notting@redhat.com> - 2.3.15-1
- update to 2.3.15
- include upstream patch for config migration (#571621)

* Tue Jul  6 2010 Bill Nottingham <notting@redhat.com> - 2.3.13-2
- rebuild against newer webkitgtk

* Thu Jun  3 2010 Bill Nottingham <notting@redhat.com> - 2.3.13-1
- update to 2.3.13

* Tue May 18 2010 Bill Nottingham <notting@redhat.com> - 2.3.12-3
- fix finding of dbi drivers (#593090)

* Fri Apr 30 2010 Bill Nottingham <notting@redhat.com> - 2.3.12-2
- update to 2.3.12

* Fri Mar 19 2010 Bill Nottingham <notting@redhat.com> - 2.3.11-1
- update to 2.3.11

* Wed Feb 24 2010 Bill Nottingham <notting@redhat.com> - 2.3.10-2
- rebuild against new goffice

* Thu Feb 18 2010 Bill Nottingham <notting@redhat.com> - 2.3.10-1
- update to 2.3.10

* Mon Feb 15 2010 Bill Nottingham <notting@redhat.com> - 2.3.9-1
- update to 2.3.9

* Thu Jan 21 2010 Bill Nottingham <notting@redhat.com> - 2.3.8-2
- Rebuild against latest aqbanking

* Thu Dec 10 2009 Bill Nottingham <notting@redhat.com> - 2.3.8-1
- update to 2.3.8

* Tue Dec  1 2009 Bill Nottingham <notting@redhat.com> - 2.3.7-1
- Update to development version.
- Fix accelerators (#533019, #541915)

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.2.9-3
- Use lzma compressed upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar  5 2009 Bill Nottingham <notting@redhat.com> - 2.2.9-1
- update to 2.2.9

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Bill Nottingham <notting@redhat.com> - 2.2.8-2
- fix crash resulting from earlier crash fix (#474511, <jik@kamens.brookline.ma.us>)

* Tue Dec 16 2008 Bill Nottingham <notting@redhat.com> - 2.2.8-1
- update to 2.2.8

* Fri Dec  5 2008 Bill Nottingham <notting@redhat.com> - 2.2.7-2
- fix crash with glib-2.19 (#474511, <jik@kamens.brookline.ma.us>)

* Tue Sep 30 2008 Bill Nottingham <notting@redhat.com> - 2.2.7-1
- update to 2.2.7

* Tue Sep  9 2008 Bill Nottingham <notting@redhat.com> - 2.2.6-2
- rebuild against new aqbanking

* Fri Aug  1 2008 Bill Nottingham <notting@redhat.com> - 2.2.6-1
- update to 2.2.6

* Tue Apr 29 2008 Bill Nottingham <notting@redhat.com> - 2.2.5-1
- update to 2.2.5

* Mon Mar  3 2008 Bill Nottingham <notting@redhat.com> - 2.2.4-1
- update to 2.2.4

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2.3-3
- Autorebuild for GCC 4.3

* Fri Jan 25 2008 Bill Nottingham <notting@redhat.com> - 2.2.3-2
- rebuild against new goffice

* Tue Jan  8 2008 Bill Nottingham <notting@redhat.com> - 2.2.3-1
- update to 2.2.3

* Tue Dec 18 2007 Bill Nottingham <notting@redhat.com> - 2.2.2-1
- update to 2.2.2

* Thu Oct 25 2007 Bill Nottingham <notting@redhat.com> - 2.2.1-4
- multilib fixes (#341331, #357161, #246382)

* Wed Oct 10 2007 Bill Nottingham <notting@redhat.com> - 2.2.1-3
- silence binreloc warning

* Wed Aug 29 2007 Bill Nottingham <notting@redhat.com> - 2.2.1-2
- fix build

* Tue Aug 21 2007 Bill Nottingham <notting@redhat.com> - 2.2.1-1
- update to 2.2.1

* Fri Aug  3 2007 Bill Nottingham <notting@redhat.com>
- tweak license tag

* Mon Jul 23 2007 Bill Nottingham <notting@redhat.com> - 2.2.0-2
- fix icon (#248492)

* Mon Jul 16 2007 Bill Nottingham <notting@redhat.com> - 2.2.0-1
- update to 2.2.0

* Mon Jul  2 2007 Bill Nottingham <notting@redhat.com> - 2.1.5-1
- update to 2.1.5

* Mon Jun 25 2007 Bill Nottingham <notting@redhat.com> - 2.1.4-1
- update to RC version 2.1.4
  - switch to using goffice04, and stock gtkhtml3
  - no more g-wrap or libtool-ltdl - use swig

* Tue Mar 13 2007 Bill Nottingham <notting@redhat.com> - 2.0.5-3
- require gtkhtml38 include file to pull in the proper gtkhtml version
- fix build when libofx and ofx tools are separate

* Mon Feb 19 2007 Bill Nottingham <notting@redhat.com> - 2.0.5-1
- update to 2.0.5
- fixes: CVE-2007-0007 (#223233)

* Tue Feb 13 2007 Bill Nottingham <notting@redhat.com> - 2.0.4-5
- split off docs package

* Mon Jan 15 2007 Bill Nottingham <notting@redhat.com> - 2.0.4-4
- fix perl requirement noise
- fix libgsf-gnome buildreq
- fix %%post
- better rpath fixing

* Thu Jan 11 2007 Bill Nottingham <notting@redhat.com> - 2.0.4-3
- build against separate goffice
- various spec cleanups
- fix gconf scriplets

* Mon Jan  8 2007 Bill Nottingham <notting@redhat.com> - 2.0.4-1
- update to 2.0.4

* Wed Oct 11 2006 Bill Nottingham <notting@redhat.com> - 2.0.2-1
- update to 2.0.2
- update docs to 2.0.1

* Mon Aug 28 2006 Bill Nottingham <notting@redhat.com> - 2.0.1-6
- rebuild against new libofx

* Sat Aug 26 2006 Karsten Hopp <karsten@redhat.com> - 2.0.1-5
- buildrequire intltool which was previously pulled in by scrollkeeper but
  dropped this requirement because of bz #203606

* Tue Aug 22 2006 Bill Nottingham <notting@redhat.com> - 2.0.1-4
- require perl-Crypt-SSLeay (#203050)

* Fri Aug 11 2006 Bill Nottingham <notting@redhat.com> - 2.0.1-3
- require yelp (#202266)

* Tue Aug  8 2006 Bill Nottingham <notting@redhat.com> - 2.0.1-2
- fix schema list

* Tue Aug  1 2006 Bill Nottingham <notting@redhat.com> - 2.0.1-1
- update to 2.0.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.0.0-2.1
- rebuild

* Tue Jul 11 2006 Bill Nottingham <notting@redhat.com> - 2.0.0-2
- rebuild against new aqbanking

* Mon Jul 10 2006 Bill Nottingham <notting@redhat.com> - 2.0.0-1
- update to 2.0.0. Woo.

* Mon Jun 19 2006 Bill Nottingham <notting@redhat.com> - 1.9.8-1
- update to 1.9.8

* Tue Jun  6 2006 Bill Nottingham <notting@redhat.com> - 1.9.7-1
- update to 1.9.7
- use official docs tarball, not svn snapshot

* Thu May 25 2006 Bill Nottingham <notting@redhat.com> - 1.9.6-2
- update docs to latest svn (gets rid of extraneous configure check
  for db185)

* Wed May 17 2006 Bill Nottingham <notting@redhat.com> - 1.9.6-1
- update to 1.9.6

* Tue May  9 2006 Bill Nottingham <notting@redhat.com> - 1.9.5-3
- rebuild against new guile (<mlichvar@redhat.com>)
- silence warnings

* Mon Apr 17 2006 Bill Nottingham <notting@redhat.com> - 1.9.5-1
- update to 1.9.5

* Thu Apr  6 2006 Bill Nottingham <notting@redhat.com> - 1.9.4-1
- update to 1.9.4

* Tue Apr  4 2006 Bill Nottingham <notting@redhat.com> - 1.9.3-2
- fix conflict with qof (#187267)

* Mon Mar 27 2006 Bill Nottingham <notting@redhat.com> - 1.9.3-1
- update to 1.9.x

* Mon Feb 20 2006 Bill Nottingham <notting@redhat.com> - 1.8.12-3
- rebuild against g-wrap-1.9.6

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.8.12-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.8.12-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 13 2006 Bill Nottingham <notting@redhat.com> 1.8.12-2
- disable postgres backend (#177646)

* Thu Dec 22 2005 Bill Nottingham <notting@redhat.com> 1.8.12-1
- update to 1.8.12

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Sep  9 2005 Bill Nottingham <notting@redhat.com> 1.8.11-4
- with new slib, umb-scheme is no longer needed. Switch requirement.

* Tue Apr 12 2005 Bill Nottingham <notting@redhat.com> 1.8.11-3
- require umb-scheme explicitly (#151465)
- rebuild against new postgresql
- use full path to icon (#154587)

* Mon Mar  7 2005 Bill Nottingham <notting@redhat.com> 1.8.11-2
- rebuild against bonobo-less Guppi, gtkhtml

* Wed Feb  9 2005 Bill Nottingham <notting@redhat.com> 1.8.11-1
- update to 1.8.11
- update docs to 1.8.5
- remove info file (#123444)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 13 2004 Bill Nottingham <notting@redhat.com> 1.8.9-1
- update to 1.8.9

* Sat Mar 20 2004 Bill Nottingham <notting@redhat.com> 1.8.8-5
- reinstate libtool helper files (#118495)

* Fri Mar 12 2004 Bill Nottingham <notting@redhat.com> 1.8.8-4
- rebuild against separate libofx/openhbci

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Dec 23 2003 Bill Nottingham <notting@redhat.com>
- add a 64-bit patch from mandrake

* Wed Dec  3 2003 Bill Nottingham <notting@redhat.com> 1.8.8-2
- rebuild

* Tue Dec  2 2003 Bill Nottingham <notting@redhat.com> 1.8.8-1
- update to 1.8.8

* Tue Sep 23 2003 Bill Nottingham <notting@redhat.com> 1.8.7-1
- update to 1.8.7
- fix docs build

* Wed Aug 20 2003 Bill Nottingham <notting@redhat.com> 1.8.5-1
- update to 1.8.5

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 28 2003 Bill Nottingham <notting@redhat.com> 1.8.4-1
- update to 1.8.4

* Mon May 19 2003 Bill Nottingham <notting@redhat.com> 1.8.3-1
- update to 1.8.3

* Mon Mar 24 2003 Bill Nottingham <notting@redhat.com> 1.8.2-1
- update to 1.8.2

* Thu Mar 20 2003 Tim Waugh <twaugh@redhat.com> 1.8.1-4
- Build requires openjade-devel (new openjade sub-package).
- Rebuild against new OpenSP.

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Sun Feb 23 2003 Bill Nottingham <notting@redhat.com> 1.8.1-2
- fix crash on hiding accounts (#84931, patch from upstream)

* Tue Feb 11 2003 Bill Nottingham <notting@redhat.com> 1.8.1-1
- update to 1.8.1

* Wed Feb  5 2003 Bill Nottingham <notting@redhat.com> 1.8.0-3
- fix desktop entry (#82804)
- add startup-notification

* Tue Feb  4 2003 Bill Nottingham <notting@redhat.com> 1.8.0-1
- 1.8.0

* Tue Jan 28 2003 Bill Nottingham <notting@redhat.com> 1.7.8-3
- rebuild everywhere

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Bill Nottingham <notting@redhat.com> 1.7.8-1
- 1.7.8

* Tue Jan 14 2003 Bill Nottingham <notting@redhat.com> 1.7.7-1
- update to 1.7.7
- add libofx, openhbci support

* Fri Dec  6 2002 Tim Waugh <twaugh@redhat.com> 1.7.5-3
- Fix desktop file (bug #69422).

* Wed Dec  4 2002 Bill Nottingham <notting@redhat.com> 1.7.5-2
- fix omf file ref to buildroot

* Tue Dec  3 2002 Bill Nottingham <notting@redhat.com> 1.7.5-1
- update to 1.7.5-1, split off postgres backend

* Mon Nov 18 2002 Bill Nottingham <notting@redhat.com> 1.6.8-3
- guile is everywhere, build everywhere
- except hammer (postgres)

* Mon Nov 11 2002 Tim Powers <timp@redhat.com> 1.6.8-2
- rebuild against guile-1.4

* Thu Nov  7 2002 Bill Nottingham <notting@redhat.com> 1.6.8-1
- update to 1.6.8-1
- stop using db1

* Thu Oct 24 2002 Jeremy Katz <katzj@redhat.com>
- build against new gtkhtml

* Sat Aug 10 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- bzip2 source

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 16 2002 Bill Nottingham <notting@redhat.com>
- autoconf fun

* Mon Apr  8 2002 Bill Nottingham <notting@redhat.com>
- rebuild in new environment against fixed guile, g-wrap

* Thu Mar 14 2002 Bill Nottingham <notting@redhat.com>
- rebuild in new environment

* Mon Mar 11 2002 Bill Nottingham <notting@redhat.com>
- update to 1.6.6

* Fri Feb 22 2002 Bill Nottingham <notting@redhat.com>
- rebuild

* Mon Dec 17 2001 Bill Nottingham <notting@redhat.com>
- update to 1.6.5

* Mon Oct  1 2001 Bill Nottingham <notting@redhat.com>
- update to 1.6.4

* Mon Sep 24 2001 Bill Nottingham <notting@redhat.com>
- update to 1.6.3

* Mon Aug 13 2001 Bill Nottingham <notting@redhat.com>
- update to 1.6.2

* Thu Aug  9 2001 Bill Nottingham <notting@redhat.com>
- add patch to fix triple imports of prices from 1.4 files
  (<dave@krondo.com>)

* Thu Jul 19 2001 Bill Nottingham <notting@redhat.com>
- tweak buildprereqs

* Sun Jul  8 2001 Bill Nottingham <notting@redhat.com>
- update to 1.6.1
- fix info dir (#47646)
- fix library dependencies

* Fri Jun 29 2001 Bill Nottingham <notting@redhat.com>
- don't own %%{_infodir}/dir

* Wed Jun 27 2001 Bill Nottingham <notting@redhat.com>
- add info dir entry

* Mon Jun 18 2001 Bill Nottingham <notting@redhat.com>
- update to 1.6.0, merge in stuff from included spec file

* Mon Feb  5 2001 Adrian Havill <havill@redhat.com>
- added Japanese locale

* Thu Jan 11 2001 Tim Powers <timp@redhat.com>
- exclude ia64

* Wed Dec  6 2000 Tim Powers <timp@redhat.com>
- updated to 1.4.9

* Mon Oct 23 2000 Tim Powers <timp@redhat.com>
- update to 1.4.8

* Wed Sep 13 2000 Tim Powers <timp@redhat.com>
- update to 1.4.6

* Wed Aug 2 2000 Tim Powers <timp@redhat.com>
- rebuilt against libpng-1.0.8

* Mon Jul 31 2000 Tim Powers <timp@redhat.com>
- updated to 1.4.3, bugfix release

* Tue Jul 25 2000 Tim Powers <timp@redhat.com>
- ExcludeArch alpha

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 17 2000 Tim Powers <timp@redhat.com>
- fixed defattr for the stuff in /usr/bin

* Wed Jul 12 2000 Tim Powers <timp@redhat.com>
- update to 1.4.2

* Tue Jul 11 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jul 05 2000 Preston Brown <pbrown@redhat.com>
- adopted for Powertools 7.0
