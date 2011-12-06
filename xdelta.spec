Summary: A binary file delta generator and an RCS replacement library
Name: xdelta
Version: 1.1.4
Release: 8%{?dist}
License: GPLv2
Group: Development/Tools
Source0: http://xdelta.googlecode.com/files/xdelta-%{version}.tar.gz
Patch1: xdelta-1.1.3-aclocal.patch
Patch3: xdelta-1.1.3-edsio.patch
Patch4: xdelta-1.1.4-glib2.patch
Patch6: xdelta-1.1.3-pkgconfig.patch
Url: http://xdelta.org/
BuildRequires: glib2-devel, zlib-devel, libtool >= 1.5.22, autoconf, automake, pkgconfig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Xdelta (X for XCF: the eXperimental Computing Facility at Berkeley) is
a binary delta generator (like a diff program for binaries) and an RCS
version control replacement library. The Xdelta library performs its
work independently of the actual format used to encode the file and is
intended to be used by various higher-level programs such as XCF's
Project Revision Control System (PRCS).  PRCS is a front end for a
version control toolset.  Xdelta uses a binary file delta algorithm to
replace the standard diff program used by RCS

%package devel
Summary: Shared library and header files for Xdelta development
Group: Development/Libraries
Requires:  %{name} = %{version}
%description devel
The Xdelta-devel package contains the shared library and header files
needed for developing Xdelta-based applications

%prep
%setup -q
%patch1 -p1 -b .aclocal
%patch3 -p1 -b .edsio
%patch4 -p1 -b .glib2
%patch6 -p1 -b .pkgconfig

for all in `find . -type f -perm -001 | grep '.*[ch]$'`; do
    chmod -x "$all"
done

chmod -x NEWS README COPYING

%build
autoreconf -fiv
%configure --disable-static

# IDIOT author overrides our cflags with -O3
make %{?_smp_mflags} CFLAGS="-D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE $RPM_OPT_FLAGS `pkg-config --cflags glib-2.0`" LDFLAGS="`pkg-config --libs glib-2.0`"

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc NEWS README xdelta.magic COPYING
%{_bindir}/xdelta
%{_libdir}/lib*.so.*
%{_mandir}/*/*

%files devel
%defattr(-,root,root,-)
%{_bindir}/xdelta-config
%{_includedir}/*
%{_libdir}/lib*.so
%{_datadir}/aclocal/xdelta.m4
%{_libdir}/pkgconfig/*

%changelog
* Mon Dec 03 2009 Adam Tkac <atkac redhat com> 1.1.4-8
- merge review related fixes (#226552)

* Tue Aug 11 2009 Adam Tkac <atkac redhat com> 1.1.4-7
- update source + project URLs

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct 03 2008 Adam Tkac <atkac redhat com> 1.1.4-4
- updated patches due rpm 4.6 (#465102)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.4-3
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Adam Tkac <atkac redhat com> 1.1.4-2
- rebuild (BuildID feature)
- changed license to GPLv2

* Tue Jan 30 2007 Adam Tkac <atkac redhat com> 1.1.4-1
- version 1.1.4 has been marked as final 1.1.4 version

* Mon Jan 29 2007 Adam Tkac <atkac redhat com> 1.1.4pre1-1
- started using dist macro
- updated to 1.1.4pre1

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> 1.1.3-20
- rebuild

* Tue May 30 2006 Ludek Smid <lsmid@redhat.com> 1.1.3-19
- libtoolize and autotools are now run during build phase
- resolved multilib conflict using pkgconfig tool

* Fri May 05 2006 Ludek Smid <lsmid@redhat.com> 1.1.3-18
- patches created on i386 fail to apply on x86_64 (#190406)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.1.3-17.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1.3-17.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Sep 09 2005 Jindrich Novy <jnovy@redhat.com>1.1.3-17
- link libxdelta against libedsio (#165978)
- add support for large files (#155524)
- port to use glib2 instead of obsolete glib1.2 (#136221)

* Wed Mar 23 2005 Jindrich Novy <jnovy@redhat.com> 1.1.3-16
- fix conflicting storage classes that causes build failure with gcc4
- gcc4 warnfixes
- create backups for patches
- drop libtool BuildRequires
- rebuild with gcc4

* Wed Oct 20 2004 Miloslav Trmac <mitr@redhat.com> - 1.1.3-15
- Add BuildRequires: glib-devel (#123759)
- Properly quote aclocal macro definition

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 19 2003 Elliot Lee <sopwith@redhat.com> 1.1.3-11
- xdelta-config belongs in the -devel subpackage - fix it

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 18 2002 Elliot Lee <sopwith@redhat.com> 1.1.3-9
- Rebuild

* Mon Oct 21 2002 Elliot Lee <sopwith@redhat.com> 1.1.3-8
- Rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Feb 15 2002 Elliot Lee <sopwith@redhat.com> 1.1.3-5
- Undo fixscribble patch, jmacd explained why my code+edsio API was at 
  fault and not xdelta.

* Fri Jan 25 2002 Elliot Lee <sopwith@redhat.com> 1.1.3-4
- Fix the bad estimation of checksum array size that caused libxdelta to
  scribble over unallocated memory when generating a delta.

* Thu Jan 24 2002 Elliot Lee <sopwith@redhat.com> 1.1.3-3
- Fix the lack of xdp_generator_free function
- Use _smp_mflags
- Prevent configure.in from chucking -O3 into CFLAGS

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Sep 24 2001 Than Ngo <than@redhat.com> 1.1.3-1
- update to 1.1.3
- Copyright -> License

* Mon Jul 23 2001 Jeff Johnson <jbj@redhat.com>
- add build dependency on zlib-devel (#49739).

* Tue Jun 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- do not use attr, as it also modifies symlinks in binary rpms :-)

* Tue Jun 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- man-pages owned by root
- include link from lib major version number

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Dec 11 2000 Erik Troan <ewt@redhat.com>
- rebuilt

* Thu Jun 09 2000 Than Ngo <than@redhat.de>
- FHS fixes
- use rpm macros

* Tue May 23 2000 Karsten Hopp <Karsten.Hopp@redhat.de>
- rebuild for 7.0
- changed mandir to /usr/share/man

* Mon Jul 26 1999 Tim Powers <timp@redhat.com>
- rebuilt for 6.1

* Tue May 11 1999 Cristian Gafton <gafton@redhat.com>
- don't ship /usr/info/dir

* Mon Apr 13 1999 Michael Maher <mike@redhat.com>
- built package fpr 6.0
- updated package

* Thu Jul 23 1998 Jeff Johnson <jbj@redhat.com>
- package for powertools.

* Tue Jul 07 1998 Arne Coucheron <arneco@online.no>
  [0.22-1]
- removed running of automake, problem fixed in sources

* Sat Jul 04 1998 Arne Coucheron <arneco@online.no>
  [0.21-1]
- added xdelta.magic to %%doc
- added running of automake before configure to make this version build
- changed %%defattr

* Sat Jun 27 1998 Arne Coucheron <arneco@online.no>
  [0.20-1]

* Sun Jun  7 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [0.19-3]
- fixed configuring sources by add --x-includes=/usr/lib/glib/include
  configure parameter (for glibconfig.h),
- changed Source url to ftp://www.xcf.berkeley.edu/pub/xdelta/
- fixed %%defattr macros (thanks to René Wuttke <Rene.Wuttke@gmx.net>).

* Wed May  6 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [0.19-2]
- %%{version} macro instead %%{PACKAGE_VERSION},
- added -q %%setup parameter,
- added using %%{name} macro in Buildroot, Source and Rquires in devel
  fields.

* Sun May 03 1998 Arne Coucheron <arneco@online.no>
  [0.19-1]
- removed some older changelogs

* Wed Apr 28 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [0.18-2]
- removed COPYING from %%doc (copyright statment is in Copyright field),
- /sbin/ldconfig is now -p parameter in %%post, %%postun,
- replaced "mkdir -p" with "install -d" in %%install,
- added "Requires: xdelta = %%{PACKAGE_VERSION}" for devel,
- added using %%defattr macro in %%files (requires rpm >= 2.4.99),
- added using predefined macro %%{PACKAGE_VERSION} instead %{version},
- changed permission on /usr/lib/lib*.so links to 644,
- removed /usr/lib/libxdelta.la from devel,
- added striping /usr/lib/lib*.so.*.* libs,
- Buildroot changed to /tmp/xdelta-%%{PACKAGE_VERSION}-root.

* Fri Apr 24 1998 Arne Coucheron <arneco@online.no>
  [0.18-1]
- removed the fakeglib patch

* Wed Apr 08 1998 Arne Coucheron <arneco@online.no>
  [0.15-2]
- splitted the package into a main and devel package

* Sat Apr 04 1998 Arne Coucheron <arneco@online.no>
  [0.15-1]
