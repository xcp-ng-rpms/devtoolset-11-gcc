%global package_speccommit e17dc15d8a771944131cde083343193b190006b7
%global usver 11.2.1
%global xsver 6
%global xsrel %{xsver}%{?xscount}%{?xshash}

#--- begin macros.scl.inc
# Our definitions
%global __python %{__python2}

# From devtoolset-11-build
%global scl devtoolset-11
%undefine nfsmountable
%global enable_devtoolset11 %global ___build_pre %{___build_pre}; source scl_source enable devtoolset-11 || :

# From /etc/rpm/macros.scl
# scl-utils RPM macros
#
# Copyright (C) 2012 Red Hat, Inc.
#   Written by Jindrich Novy <jnovy@redhat.com>.

%global scl_debug() %{expand:
%define old_debug %{lua:print(rpm.expand("%{debug_package}"):len())}
%global debug_package %{expand:
%if "%{?old_debug}" == "0"
       %{expand: %{nil}}
%else
%if "%{?scl}%{!?scl:0}" == "%{pkg_name}"
        %{expand: %{nil}}
%else
%ifnarch noarch
%package debuginfo
Summary: Debug information for package %{name}
Group: Development/Debug
AutoReqProv: 0
Requires: %scl_runtime
Provides: scl-package(%scl)
%{lua:
        debuginfo=tonumber(rpm.expand("%{old_debug}"))
        if debuginfo > 0 then
                rpm.define("__debug_package 1")
        end
}
%description debuginfo
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.
%files debuginfo -f debugfiles.list
%defattr(-,root,root)
%endif
%endif
%endif
%{nil}}}

%global scl_package() %{expand:%{!?_root_prefix:
%global pkg_name		%1
%global scl_name		%{scl}
%global scl_prefix		%{scl}-
%global scl_runtime		%{scl}-runtime
%{!?_scl_prefix:		%global _scl_prefix /opt/rh}
%global _scl_scripts		%{_scl_prefix}/%{scl}
%global _scl_root		%{_scl_prefix}/%{scl}/root
%global _root_prefix		%{_prefix}
%global _root_exec_prefix	%{_root_prefix}
%global _root_bindir		%{_exec_prefix}/bin
%global _root_sbindir		%{_exec_prefix}/sbin
%global _root_libexecdir	%{_exec_prefix}/libexec
%global _root_datadir		%{_prefix}/share
%global _root_sysconfdir	%{_sysconfdir}
%global _root_sharedstatedir	%{_prefix}/com
%global _root_localstatedir	%{_localstatedir}
%global _root_libdir		%{_exec_prefix}/%{_lib}
%global _root_includedir	%{_prefix}/include
%global _root_infodir		%{_datadir}/info
%global _root_mandir		%{_datadir}/man
%global _root_initddir		%{_sysconfdir}/rc.d/init.d
%global _prefix			%{_scl_root}/usr
%global _exec_prefix		%{_prefix}
%global _bindir			%{_exec_prefix}/bin
%global _sbindir		%{_exec_prefix}/sbin
%global _libexecdir		%{_exec_prefix}/libexec
%global _datadir		%{_prefix}/share
%global _sysconfdir		%{_scl_root}/etc
%{?nfsmountable:		%global _sysconfdir %{_root_sysconfdir}%{_scl_prefix}/%{scl}}
%global _sharedstatedir		%{_scl_root}/var/lib
%{?nfsmountable:		%global _sharedstatedir %{_root_localstatedir}%{_scl_prefix}/%{scl}/lib}
%global _localstatedir		%{_scl_root}/var
%{?nfsmountable:		%global _localstatedir %{_root_localstatedir}%{_scl_prefix}/%{scl}}
%global _libdir			%{_exec_prefix}/%{_lib}
%global _includedir		%{_prefix}/include
%global _infodir		%{_datadir}/info
%global _mandir			%{_datadir}/man
%global _docdir			%{_datadir}/doc
%global _defaultdocdir		%{_docdir}
}
%{?scl_dependency_generators:%scl_dependency_generators}
%global scl_pkg_name		%{scl}-%{pkg_name}
%scl_debug
%global __os_install_post %{expand:
    /usr/lib/rpm/brp-scl-compress %{_scl_root}
    %{!?__debug_package:/usr/lib/rpm/brp-strip %{__strip}
    /usr/lib/rpm/brp-strip-comment-note %{__strip} %{__objdump}
    }
    /usr/lib/rpm/brp-strip-static-archive %{__strip}
    /usr/lib/rpm/brp-scl-python-bytecompile %{__python} %{?_python_bytecompile_errors_terminate_build} %{_scl_root}
    /usr/lib/rpm/brp-python-hardlink
    %{!?__jar_repack:/usr/lib/rpm/redhat/brp-java-repack-jars}
%{nil}}
BuildRequires: scl-utils-build
%if "%{?scl}%{!?scl:0}" == "%{pkg_name}"
Requires: %{scl_runtime}
Provides: scl-package(%{scl})
%endif
%{?scl_package_override:%scl_package_override}
}

%global scl_require()	%{_scl_prefix}/%1/enable, %1
%global scl_require_package() %1-%2
%global scl_files %{expand:
%defattr(-,root,root,-)
%dir %_scl_prefix
%dir %attr(555,root,root) %{_scl_root}
%dir %attr(555,root,root) %{_scl_scripts}
%{_scl_scripts}/enable
%{_root_sysconfdir}/scl/prefixes/%scl
%{_scl_root}/bin
%attr(555,root,root) %{_scl_root}/boot
%{_scl_root}/dev
%dir %{_sysconfdir}
%{_sysconfdir}/X11
%{_sysconfdir}/xdg
%{_sysconfdir}/opt
%{_sysconfdir}/pm
%{_sysconfdir}/xinetd.d
%{_sysconfdir}/skel
%{_sysconfdir}/sysconfig
%{_sysconfdir}/pki
%{_scl_root}/home
%{_scl_root}/lib
%ifarch x86_64 ppc ppc64 ppc64le aarch64 sparc sparc64 s390 s390x
%{_scl_root}/%{_lib}
%endif
%{_scl_root}/media
%dir %{_scl_root}/mnt
%dir %{_scl_root}/opt
%attr(555,root,root) %{_scl_root}/proc
%attr(550,root,root) %{_scl_root}/root
%{_scl_root}/run
%{_scl_root}/sbin
%{_scl_root}/srv
%{_scl_root}/sys
%attr(1777,root,root) %{_scl_root}/tmp
%dir %{_scl_root}/usr
%attr(555,root,root) %{_scl_root}/usr/bin
%{_scl_root}/usr/etc
%{_scl_root}/usr/games
%{_scl_root}/usr/include
%dir %attr(555,root,root) %{_scl_root}/usr/lib
%ifarch x86_64 ppc ppc64 ppc64le aarch64 sparc sparc64 s390 s390x
%attr(555,root,root) %{_scl_root}/usr/%{_lib}
%endif
%{_scl_root}/usr/libexec
%{_scl_root}/usr/local
%attr(555,root,root) %{_scl_root}/usr/sbin
%dir %{_scl_root}/usr/share
%{_scl_root}/usr/share/aclocal
%{_scl_root}/usr/share/applications
%{_scl_root}/usr/share/augeas
%{_scl_root}/usr/share/backgrounds
%{_scl_root}/usr/share/desktop-directories
%{_scl_root}/usr/share/dict
%{_scl_root}/usr/share/doc
%attr(555,root,root) %dir %{_scl_root}/usr/share/empty
%{_scl_root}/usr/share/games
%{_scl_root}/usr/share/ghostscript
%{_scl_root}/usr/share/gnome
%{_scl_root}/usr/share/icons
%{_scl_root}/usr/share/idl
%{_scl_root}/usr/share/info
%dir %{_scl_root}/usr/share/locale
%dir %{_scl_root}/usr/share/man
%{_scl_root}/usr/share/mime-info
%{_scl_root}/usr/share/misc
%{_scl_root}/usr/share/omf
%{_scl_root}/usr/share/pixmaps
%{_scl_root}/usr/share/sounds
%{_scl_root}/usr/share/themes
%{_scl_root}/usr/share/xsessions
%{_scl_root}/usr/share/X11
%{_scl_root}/usr/src
%{_scl_root}/usr/tmp
%dir %{_localstatedir}
%{_localstatedir}/adm
%{_localstatedir}/cache
%{_localstatedir}/db
%{_localstatedir}/empty
%{_localstatedir}/games
%{_localstatedir}/gopher
%{_localstatedir}/lib
%{_localstatedir}/local
%ghost %dir %attr(755,root,root) %{_localstatedir}/lock
%ghost %{_localstatedir}/lock/subsys
%{_localstatedir}/log
%{_localstatedir}/mail
%{_localstatedir}/nis
%{_localstatedir}/opt
%{_localstatedir}/preserve
%ghost %attr(755,root,root) %{_localstatedir}/run
%dir %{_localstatedir}/spool
%attr(755,root,root) %{_localstatedir}/spool/lpd
%attr(775,root,mail) %{_localstatedir}/spool/mail
%attr(1777,root,root) %{_localstatedir}/tmp
%{_localstatedir}/yp
}

%global scl_install %{expand:
# scl specific stuff
mkdir -p %{buildroot}%{_root_sysconfdir}/{rpm,scl/prefixes}
cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config << EOF
%%%%scl %scl
%{?nfsmountable:%%%%nfsmountable %{nfsmountable}}
%{!?nfsmountable:%%%%undefine nfsmountable}
EOF
cat >> %{buildroot}%{_root_sysconfdir}/scl/prefixes/%{scl} << EOF
%_scl_prefix
EOF
# filelist
set +x
cat >> %{buildroot}/lang-exceptions << EOF
af_ZA
am_ET
ast_ES
az_IR
bg_BG
bn_IN
ca@valencia
ca_ES
ca_ES@valencian
cs_CZ
de_AT
de_CH
de_DE
default
el_GR
en_AU
en_CA
en_GB
en_US
en_NZ
es_AR
es_CL
es_CO
es_CR
es_DO
es_EC
es_ES
es_GT
es_HN
es_MX
es_NI
es_PA
es_PE
es_PR
es_SV
es_UY
es_VE
et_EE
eu_ES
fa_IR
fi_FI
fr_BE
fr_CA
fr_CH
fr_FR
gl_ES
he_IL
hr_HR
hu_HU
it_CH
it_IT
ja_JP
ko_KR
ks@devanagari
lv_LV
ms_MY
my_MM
nb_NO
nds_DE
nl_BE
nl_NL
pl_PL
pt_BR
pt_PT
ru_RU
sl_SI
sq_AL
sr_RS
sv_SE
uk_UA
ur_PK
zh_CN
zh_CN.GB2312
zh_HK
zh_TW
zh_TW.Big5
en@boldquot
en@quot
nds@NFE
sr@ije
sr@ijekavian
sr@ijekavianlatin
sr@latin
sr@Latn
uz@cyrillic
uz@Latn
be@latin
en@shaw
brx
brx_IN
EOF
cat >> %{buildroot}/iso_639.sed << EOF
1,/<iso_639_entries/b
# on each new iso-code process the current one
\\!\\(<iso_639_entry\\|</iso_639_entries>\\)!{
    x
    s/^$//
    # we are on the first iso-code--nothing to process here
    t
    # process and write to output
    s/\\s\\+/ /g
    s/<iso_639_entry//
    s!/\\s*>!!
    # use '%' as a separator of parsed and unparsed input
    s/\\(.*\\)iso_639_2T_code="\\([^"]\\+\\)"\\(.*\\)/\\2 % \\1 \\3/
    s/\\([^%]\\+\\)%\\(.*\\)iso_639_2B_code="\\([^"]\\+\\)"\\(.*\\)/\\1\\t\\3 % \\2 \\4/
    #  clear subst. memory for the next t
    t clear
    :clear
    s/\\([^%]\\+\\)%\\(.*\\)iso_639_1_code="\\([^"]\\+\\)"\\(.*\\)/\\1\\t\\3 % \\2 \\4/
    t name
    # no 639-1 code--write xx
    s/%/\\tXX %/
    :name
    s/\\([^%]\\+\\)%\\(.*\\)name="\\([^"]\\+\\)"\\(.*\\)/\\1\\t\\3/
    s/ \\t/\\t/g
    p
    b
    :noout
}
H
EOF
cat >> %{buildroot}/iso_3166.sed << EOF
1,/<iso_3166_entries/b
# on each new iso-code process the current one
\\!\\(<iso_3166_entry\\|</iso_3166_entries>\\)!{
    x
    s/^$//
    # we are on the first iso-code--nothing to process here
    t
    # process and write to output
    s/\\s\\+/ /g
    s/<iso_3166_entry//
    s!/\\s*>!!
    # use '%' as a separator of parsed and unparsed input
    s/\\(.*\\)alpha_2_code="\\([^"]\\+\\)"\\(.*\\)/\\2 % \\1 \\3/
    s/\\([^%]\\+\\)%\\(.*\\)alpha_3_code="\\([^"]\\+\\)"\\(.*\\)/\\1% \\2 \\4/
    #  clear subst. memory for the next t
    t clear
    :clear
    s/\\([^%]\\+\\)%\\(.*\\)numeric_code="\\([^"]\\+\\)"\\(.*\\)/\\1% \\2 \\4/
    t name
    # no 3166 code--write xx
    s/%/\\tXX %/
    :name
    s/\\([^%]\\+\\)%\\(.*\\)name="\\([^"]\\+\\)"\\(.*\\)/\\1\\t\\3/
    s/ \\t/\\t/g
    p
    b
    :noout
}
H
EOF
mkdir -p %{buildroot}%{_localstatedir}
pushd  %{buildroot}%{_localstatedir}
mkdir -p {adm,empty,gopher,lib/{games,misc,rpm-state},local,lock/subsys,log,nis,preserve,run,spool/{mail,lpd},tmp,db,cache,opt,games,yp}
popd
mkdir -p %{buildroot}%{_sysconfdir}
pushd %{buildroot}%{_sysconfdir}
mkdir -p {X11/{applnk,fontpath.d},xdg/autostart,opt,pm/{config.d,power.d,sleep.d},xinetd.d,skel,sysconfig,pki}
popd
mkdir -p %{buildroot}%{_scl_root}
rm -f $RPM_BUILD_DIR/%{buildsubdir}/filelist
rm -f $RPM_BUILD_DIR/%{buildsubdir}/filesystem
pushd %{buildroot}%{_scl_root}
mkdir -p boot dev \\
        home media mnt opt proc root run/lock srv sys tmp \\
        usr/{bin,etc,games,include,lib/{games,locale,modules,sse2},libexec,local/{bin,etc,games,lib,sbin,src,share/{applications,man/man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x},info},libexec,include,},sbin,share/{aclocal,applications,augeas/lenses,backgrounds,desktop-directories,dict,doc,empty,games,ghostscript/conf.d,gnome,icons,idl,info,man/man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x,0p,1p,3p},mime-info,misc,omf,pixmaps,sounds,themes,xsessions,X11},src,src/kernels,src/debug}
%ifarch x86_64 ppc ppc64 ppc64le aarch64 sparc sparc64 s390 s390x
mkdir -p usr/{%{_lib}/{games,sse2,tls,X11,pm-utils/{module.d,power.d,sleep.d}},local/%{_lib}}
%endif
ln -snf %{_localstatedir}/tmp usr/tmp
ln -snf spool/mail %{buildroot}%{_localstatedir}/mail
ln -snf usr/bin bin
ln -snf usr/sbin sbin
ln -snf usr/lib lib
%ifarch x86_64 ppc ppc64 ppc64le aarch64 sparc sparc64 s390 s390x
ln -snf usr/%{_lib} %{_lib}
%endif
sed -n -f %{buildroot}/iso_639.sed /usr/share/xml/iso-codes/iso_639.xml >%{buildroot}/iso_639.tab
sed -n -f %{buildroot}/iso_3166.sed /usr/share/xml/iso-codes/iso_3166.xml >%{buildroot}/iso_3166.tab
grep -v "^$" %{buildroot}/iso_639.tab | grep -v "^#" | while read a b c d ; do
    [[ "$d" =~ "^Reserved" ]] && continue
    [[ "$d" =~ "^No linguistic" ]] && continue
    locale=$c
    if [ "$locale" = "XX" ]; then
        locale=$b
    fi
    echo "%lang(${locale})      %{_scl_root}/usr/share/locale/${locale}" >> $RPM_BUILD_DIR/%{buildsubdir}/filelist
    echo "%lang(${locale}) %ghost %config(missingok) %{_scl_root}/usr/share/man/${locale}" >> $RPM_BUILD_DIR/%{buildsubdir}/filelist
done
cat %{buildroot}/lang-exceptions | grep -v "^#" | grep -v "^$" | while read loc ; do
    locale=$loc
    locality=
    special=
    [[ "$locale" =~ "@" ]] && locale=${locale%%%%@*}
    [[ "$locale" =~ "_" ]] && locality=${locale##*_}
    [[ "$locality" =~ "." ]] && locality=${locality%%%%.*}
    [[ "$loc" =~ "_" ]] || [[ "$loc" =~ "@" ]] || special=$loc
    # If the locality is not official, skip it
    if [ -n "$locality" ]; then
        grep -q "^$locality" %{buildroot}/iso_3166.tab || continue
    fi
    # If the locale is not official and not special, skip it
    if [ -z "$special" ]; then
        egrep -q "[[:space:]]${locale%%_*}[[:space:]]" \\
           %{buildroot}/iso_639.tab || continue
    fi
    echo "%lang(${locale})      %{_scl_root}/usr/share/locale/${loc}" >> $RPM_BUILD_DIR/%{buildsubdir}/filelist
    echo "%lang(${locale})  %ghost %config(missingok) %{_scl_root}/usr/share/man/${loc}" >> $RPM_BUILD_DIR/%{buildsubdir}/filelist
done
rm -f %{buildroot}/iso_639.tab
rm -f %{buildroot}/iso_639.sed
rm -f %{buildroot}/iso_3166.tab
rm -f %{buildroot}/iso_3166.sed
rm -f %{buildroot}/lang-exceptions
cat $RPM_BUILD_DIR/%{buildsubdir}/filelist | grep "locale" | while read a b ; do
    mkdir -p -m 755 %{buildroot}/$b/LC_MESSAGES
done
cat $RPM_BUILD_DIR/%{buildsubdir}/filelist | grep "/share/man" | while read a b c d; do
    mkdir -p -m 755 %{buildroot}/$d/man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x,0p,1p,3p}
done
for i in man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x,0p,1p,3p}; do
   echo "%{_scl_root}/usr/share/man/$i" >> $RPM_BUILD_DIR/%{buildsubdir}/filelist
done
ln -s $RPM_BUILD_DIR/%{buildsubdir}/filelist $RPM_BUILD_DIR/%{buildsubdir}/filesystem
set -x
popd
}
#--- end macros.scl.inc

%global __python /usr/bin/python3
%{?scl:%global __strip %%{_scl_root}/usr/bin/strip}
%{?scl:%global __objdump %%{_scl_root}/usr/bin/objdump}
%{?scl:%scl_package gcc}
%global DATE 20210728
%global gitrev 134ab8155c937122663513b76afa8e64ad61fe99
%global gcc_version 11.2.1
%global gcc_major 11
# Note, gcc_release must be integer, if you want to add suffixes to
# %%{release}, append them after %%{gcc_release} on Release: line.
%global gcc_release 1
%global nvptx_tools_gitrev 5f6f343a302d620b0868edab376c00b15741e39e
%global newlib_cygwin_gitrev 50e2a63b04bdd018484605fbb954fd1bd5147fa0
%global mpc_version 1.0.3
%global isl_version 0.18
%global mpfr_version 3.1.4
%global gmp_version 6.1.0
%global doxygen_version 1.8.0
%global _unpackaged_files_terminate_build 0
%global multilib_enabled 0
%if 0%{?fedora} > 27 || 0%{?rhel} > 7
%undefine _annotated_build
%endif
# Strip will fail on nvptx-none *.a archives and the brp-* scripts will
# fail randomly depending on what is stripped last.
%if 0%{?__brp_strip_static_archive:1}
%global __brp_strip_static_archive %{__brp_strip_static_archive} || :
%endif
%if 0%{?__brp_strip_lto:1}
%global __brp_strip_lto %{__brp_strip_lto} || :
%endif
%global multilib_64_archs sparc64 ppc64 ppc64p7 x86_64
%if 0%{?rhel} > 7
%global build_ada 0
%global build_objc 0
%global build_go 1
%global build_d 0
%else
%ifarch %{ix86} x86_64 ia64 ppc %{power64} alpha s390x %{arm} aarch64
%global build_ada 0
%else
%global build_ada 0
%endif
%global build_objc 0
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
%global build_go 1
%else
%global build_go 0
%endif
%ifarch %{ix86} x86_64 %{arm} %{mips} s390 s390x riscv64
%global build_d 1
%else
%global build_d 0
%endif
%endif
%if 0%{?rhel} >= 7
%ifarch %{ix86} x86_64 ia64 ppc ppc64 ppc64le
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%endif
%if 0%{?rhel} == 6
%ifarch %{ix86} x86_64 ia64 ppc64le
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64
%global build_libasan 1
%else
%global build_libasan 0
%endif
%ifarch x86_64 ppc64 ppc64le aarch64
%global build_libtsan 1
%else
%global build_libtsan 0
%endif
%ifarch x86_64 ppc64 ppc64le aarch64
%global build_liblsan 1
%else
%global build_liblsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64
%global build_libubsan 1
%else
%global build_libubsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips} riscv64
%global build_libatomic 1
%else
%global build_libatomic 0
%endif
%ifarch %{ix86} x86_64 %{arm} alpha ppc ppc64 ppc64le ppc64p7 s390 s390x aarch64
%global build_libitm 1
%else
%global build_libitm 0
%endif
%if 0%{?rhel} == 6
%global build_isl 0
%else
%global build_isl 1
%endif
%global build_libstdcxx_docs 0
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
%global attr_ifunc 1
%else
%global attr_ifunc 0
%endif
%ifarch x86_64 ppc64le
%if 0%{?rhel} >= 8
%global build_offload_nvptx 1
%else
%global build_offload_nvptx 0
%endif
%else
%global build_offload_nvptx 0
%endif
%if 0%{?fedora} < 32
%ifarch s390x
%global multilib_32_arch s390
%endif
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64 ppc64p7
%global multilib_32_arch ppc
%endif
%ifarch x86_64
%global multilib_32_arch i686
%endif

%global run_tests 1

Summary: GCC version 11
Name: devtoolset-11-gcc
Version: 11.2.1
Release: %{?xsrel}%{?dist}
# libgcc, libgfortran, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
# The source for this package was pulled from upstream's vcs.
# %%{gitrev} is some commit from the
# https://gcc.gnu.org/git/?p=gcc.git;h=refs/vendors/redhat/heads/gcc-%%{gcc_major}-branch
# branch.  Use the following commands to generate the tarball:
# git clone --depth 1 git://gcc.gnu.org/git/gcc.git gcc-dir.tmp
# git --git-dir=gcc-dir.tmp/.git fetch --depth 1 origin %%{gitrev}
# git --git-dir=gcc-dir.tmp/.git archive --prefix=%%{name}-%%{version}-%%{DATE}/ %%{gitrev} | xz -9e > %%{name}-%%{version}-%%{DATE}.tar.xz
# rm -rf gcc-dir.tmp
Source0: gcc-11.2.1-20210728.tar.xz
Source1: isl-0.18.tar.bz2
Source2: mpc-1.0.3.tar.gz
Source3: doxygen-1.8.0.src.tar.gz
Patch0: gcc11-hack.patch
Patch1: gcc11-sparc-config-detection.patch
Patch2: gcc11-libgomp-omp_h-multilib.patch
Patch3: gcc11-libtool-no-rpath.patch
Patch4: gcc11-isl-dl.patch
Patch5: gcc11-isl-dl2.patch
Patch6: gcc11-no-add-needed.patch
Patch7: gcc11-foffload-default.patch
Patch8: gcc11-Wno-format-security.patch
Patch9: gcc11-d-shared-libphobos.patch
Patch10: gcc11-add-Wbidirectional.patch
Patch11: gcc11-fortran-fdec-duplicates.patch
Patch12: gcc11-fortran-flogical-as-integer.patch
Patch13: gcc11-fortran-fdec-ichar.patch
Patch14: gcc11-fortran-fdec-non-integer-index.patch
Patch15: gcc11-fortran-fdec-old-init.patch
Patch16: gcc11-fortran-fdec-override-kind.patch
Patch17: gcc11-fortran-fdec-non-logical-if.patch
Patch18: gcc11-fortran-fdec-promotion.patch
Patch19: gcc11-fortran-fdec-sequence.patch
Patch20: gcc11-fortran-fdec-add-missing-indexes.patch
Patch21: gcc11-libstdc++-compat.patch
Patch22: gcc11-libgfortran-compat.patch
Patch23: 0001-x86-Remove-before-ret.patch
Patch24: 0002-x86-Add-mharden-sls-none-all-return-indirect-branch.patch
Patch25: 0003-x86-Add-mindirect-branch-cs-prefix.patch
Patch26: 0004-x86-Rename-harden-sls-indirect-branch-to-harden-sls-.patch
Patch27: 0005-x86-Skip-ENDBR-when-emitting-direct-call-jmp-to-loca.patch
Patch28: 0006-Add-fcf-check-attribute-yes-no.patch
Patch29: 21b30eddc59d92a07264c3b21eb032d6c303d16f.patch
# The source for nvptx-tools package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone --depth 1 git://github.com/MentorEmbedded/nvptx-tools.git nvptx-tools-dir.tmp
# git --git-dir=nvptx-tools-dir.tmp/.git fetch --depth 1 origin %%{nvptx_tools_gitrev}
# git --git-dir=nvptx-tools-dir.tmp/.git archive --prefix=nvptx-tools-%%{nvptx_tools_gitrev}/ %%{nvptx_tools_gitrev} | xz -9e > nvptx-tools-%%{nvptx_tools_gitrev}.tar.x# rm -rf nvptx-tools-dir.tmp
Source4: nvptx-tools-5f6f343a302d620b0868edab376c00b15741e39e.tar.xz
# The source for nvptx-newlib package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone git://sourceware.org/git/newlib-cygwin.git newlib-cygwin-dir.tmp
# git --git-dir=newlib-cygwin-dir.tmp/.git archive --prefix=newlib-cygwin-%%{newlib_cygwin_gitrev}/ %%{newlib_cygwin_gitrev} ":(exclude)newlib/libc/sys/linux/include/rpc/*.[hx]" | xz -9e > newlib-cygwin-%%{newlib_cygwin_gitrev}.tar.xz
# rm -rf newlib-cygwin-dir.tmp
Source5: newlib-cygwin-50e2a63b04bdd018484605fbb954fd1bd5147fa0.tar.xz
Source6: libgomp_nonshared.c
Source7: mpfr-3.1.4.tar.bz2
Source8: gmp-6.1.0.tar.bz2
URL: http://gcc.gnu.org

BuildRequires: devtoolset-11-build

# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %%gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
# Need binutils which support --no-add-needed >= 2.20.51.0.2-12
# Need binutils which support -plugin
# Need binutils which support .loc view >= 2.30
# Need binutils which support --generate-missing-build-notes=yes >= 2.31
%if 0%{?scl:1}
BuildRequires: devtoolset-11-binutils >= 2.31
# For testing
%if 0%{?run_tests:1}
BuildRequires: devtoolset-11-gdb >= 7.4.50
%endif
%endif
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, sharutils
BuildRequires: texinfo, texinfo-tex, /usr/bin/pod2man
#BuildRequires: systemtap-sdt-devel >= 1.3
#BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 3.1.0, libmpc-devel >= 0.8.1
#BuildRequires: python3-devel, /usr/bin/python
BuildRequires: gcc, gcc-c++, make
%if 0%{?rhel} <= 7
BuildRequires: python3
%endif
# For VTA guality testing
BuildRequires: gdb
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
%if 0%{?rhel} >= 8
BuildRequires: libzstd-devel
%endif
%ifarch ppc ppc64 ppc64le ppc64p7 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%if 0%{?multilib_enabled}
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
# Need binutils that support --build-id
# Need binutils that support %%gnu_unique_object
# Need binutils that support .cfi_sections
# Need binutils that support --no-add-needed
# Need binutils that support -plugin
# Need binutils that support .loc view >= 2.30
# Need binutils which support --generate-missing-build-notes=yes >= 2.31
%if 0%{?rhel} <= 8
Requires: devtoolset-11-binutils >= 2.22.52.0.1
%else
Requires: binutils >= 2.24
%endif
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
%ifarch ppc ppc64 ppc64le ppc64p7 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
%if 0%{?rhel} >= 7
BuildRequires: gmp-devel >= 4.3.2
BuildRequires: mpfr-devel >= 3.1.0
BuildRequires: libmpc-devel >= 0.8.1
%endif
%if %{build_libstdcxx_docs}
BuildRequires: libxml2
BuildRequires: graphviz
%if 0%{?rhel} < 7
# doxygen BRs
BuildRequires: perl
BuildRequires: texlive-dvips, texlive-utils, texlive-latex
BuildRequires: ghostscript
%endif
%if 0%{?rhel} >= 7
BuildRequires: doxygen >= 1.7.1
BuildRequires: texlive-collection-latex
# BuildRequires: docbook5-style-xsl
# BuildRequires: dblatex
%endif
%endif
Requires: libgcc >= 4.1.2-43
Requires: libgomp >= 4.4.4-13
# lto-wrapper invokes make
Requires: make
%{?scl:Requires:%scl_runtime}
AutoReq: true
# Various libraries are imported.  #1859893 asks us to list them all.
Provides: bundled(libiberty)
Provides: bundled(libbacktrace)
Provides: bundled(libffi)
Provides: gcc(major) = %{gcc_major}
%ifarch sparc64 ppc64 ppc64le s390x x86_64 ia64 aarch64
Provides: liblto_plugin.so.0()(64bit)
%else
Provides: liblto_plugin.so.0
%endif
%global oformat %{nil}
%global oformat2 %{nil}
%ifarch %{ix86}
%global oformat OUTPUT_FORMAT(elf32-i386)
%endif
%ifarch x86_64
%global oformat OUTPUT_FORMAT(elf64-x86-64)
%global oformat2 OUTPUT_FORMAT(elf32-i386)
%endif
%ifarch ppc
%global oformat OUTPUT_FORMAT(elf32-powerpc)
%global oformat2 OUTPUT_FORMAT(elf64-powerpc)
%endif
%ifarch ppc64
%global oformat OUTPUT_FORMAT(elf64-powerpc)
%global oformat2 OUTPUT_FORMAT(elf32-powerpc)
%endif
%ifarch s390
%global oformat OUTPUT_FORMAT(elf32-s390)
%endif
%ifarch s390x
%global oformat OUTPUT_FORMAT(elf64-s390)
%global oformat2 OUTPUT_FORMAT(elf32-s390)
%endif
%ifarch ia64
%global oformat OUTPUT_FORMAT(elf64-ia64-little)
%endif
%ifarch ppc64le
%global oformat OUTPUT_FORMAT(elf64-powerpcle)
%endif
%ifarch aarch64
%global oformat OUTPUT_FORMAT(elf64-littleaarch64)
%endif
%if 0%{?rhel} == 6
ExclusiveArch: x86_64 %{ix86}
%endif
%if 0%{?rhel} == 7
ExcludeArch: aarch64
%endif





%if 0%{?rhel} > 7
%global nonsharedver 80
%else
%if 0%{?rhel} == 7
%global nonsharedver 48
%else
%global nonsharedver 44
%endif
%endif

%if 0%{?scl:1}
%global _gnu %{nil}
%else
%global _gnu -gnueabi
%endif
%ifarch sparcv9
%global gcc_target_platform sparc64-%{_vendor}-%{_target_os}
%endif
%ifarch ppc ppc64p7
%global gcc_target_platform ppc64-%{_vendor}-%{_target_os}
%endif
%ifnarch sparcv9 ppc ppc64p7
%global gcc_target_platform %{_target_platform}
%endif

%description
The devtoolset-11-gcc%{!?scl:11} package contains the GNU Compiler Collection version 10.

%package -n libgcc
Summary: GCC version 11 shared support library
Autoreq: false

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++
Summary: C++ support for GCC  version 11
Requires: devtoolset-11-gcc%{!?scl:11} = %{version}-%{release}
%if 0%{?rhel} >= 7
Requires: libstdc++
%else
Requires: libstdc++ >= 4.4.4-13
%endif
Requires: devtoolset-11-libstdc++%{!?scl:11}-devel = %{version}-%{release}
Autoreq: true

%description c++
This package adds C++ support to the GNU Compiler Collection
version 11.  It includes support for most of the current C++ specification
and a lot of support for the upcoming C++ specification.

%package -n libstdc++
Summary: GNU Standard C++ Library
Autoreq: true
Requires: glibc >= 2.10.90-7

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n devtoolset-11-libstdc++%{!?scl:11}-devel
Summary: Header files and libraries for C++ development
%if 0%{?rhel} >= 7
Requires: libstdc++
%else
Requires: libstdc++ >= 4.4.4-13
%endif
Requires: libstdc++%{?_isa}
Autoreq: true

%description -n devtoolset-11-libstdc++%{!?scl:11}-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n devtoolset-11-libstdc++%{!?scl:11}-docs
Summary: Documentation for the GNU standard C++ library
Autoreq: true

%description -n devtoolset-11-libstdc++%{!?scl:11}-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.

%package go
Summary: Go support for GCC 11 (gccgo)
Requires: devtoolset-11-gcc%{!?scl:11} = %{version}-%{release}
Autoreq: true

%description go
The devtoolset-11-gcc%{!?scl:10}-go package provides support for compiling Go
programs with the GNU Compiler Collection.

%package gfortran
Summary: Fortran support for GCC 11
Requires: devtoolset-11-gcc%{!?scl:11} = %{version}-%{release}
%if 0%{?rhel} > 7
Requires: libgfortran >= 8.1.1
%else
Requires: libgfortran5 >= 8.1.1
%endif
# xenpkg clone gcc needs this when used in a fedora37 distrobox:
%if 0%{!?build_libquadmath:1}
%if 0%{!?scl:1}
Requires: libquadmath
%endif
Requires: devtoolset-11-libquadmath-devel = %{version}-%{release}
%endif
Autoreq: true

%description gfortran
The devtoolset-11-gcc%{!?scl:10}-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.


%package gdb-plugin
Summary: GCC 11 plugin for GDB
Requires: devtoolset-11-gcc%{!?scl:11} = %{version}-%{release}

%description gdb-plugin
This package contains GCC 11 plugin for GDB C expression evaluation.

%package -n devtoolset-11-libgccjit
Summary: Library for embedding GCC inside programs and libraries
Requires: devtoolset-11-gcc%{!?scl:11} = %{version}-%{release}

%description -n devtoolset-11-libgccjit
This package contains shared library with GCC 11 JIT front-end.

%package -n devtoolset-11-libgccjit-devel
Summary: Support for embedding GCC inside programs and libraries
Group: Development/Libraries
Requires: devtoolset-11-libgccjit = %{version}-%{release}
%if 0
Requires: devtoolset-11-libgccjit-docs = %{version}-%{release}
%endif

%description -n devtoolset-11-libgccjit-devel
This package contains header files for GCC 11 JIT front end.

%if 0
%package -n devtoolset-11-libgccjit-docs
Summary: Documentation for embedding GCC inside programs and libraries
Group: Development/Libraries
#%if 0%{?rhel} > 7
#BuildRequires: python3-sphinx
#%else
#BuildRequires: python-sphinx
#%endif
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n devtoolset-11-libgccjit-docs
This package contains documentation for GCC 11 JIT front-end.
%endif

%package -n libquadmath
Summary: GCC 11 __float128 shared support library
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libquadmath
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%package -n devtoolset-11-libquadmath-devel
Summary: GCC 11 __float128 support
Group: Development/Libraries
%if 0%{!?scl:1}
Requires: devtoolset-11-libquadmath%{_isa} = %{version}-%{release}
%else
%if 0%{?rhel} >= 7
Requires: libquadmath%{_isa}
%endif
%endif
Requires: devtoolset-11-gcc%{!?scl:11} = %{version}-%{release}

%description -n devtoolset-11-libquadmath-devel
This package contains headers for building Fortran programs using
REAL*16 and programs using __float128 math.

%package -n libitm
Summary: The GNU Transactional Memory library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n devtoolset-11-libitm-devel
Summary: The GNU Transactional Memory support
Requires: libitm%{_isa} >= 4.7.0-1
Requires: devtoolset-11-gcc%{!?scl:11} = %{version}-%{release}

%description -n devtoolset-11-libitm-devel
This package contains headers and support files for the
GNU Transactional Memory library.

%package plugin-devel
Summary: Support for compiling GCC plugins
Requires: devtoolset-11-gcc%{!?scl:11} = %{version}-%{release}
%if 0%{?rhel} >= 7
Requires: gmp-devel >= 4.3.2
Requires: mpfr-devel >= 3.1.0
Requires: libmpc-devel >= 0.8.1
%endif

%description plugin-devel
This package contains header files and other support files
for compiling GCC 11 plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.

%package -n libatomic
Summary: The GNU Atomic library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libatomic
This package contains the GNU Atomic library
which is a GCC support runtime library for atomic operations not supported
by hardware.

%package -n devtoolset-11-libatomic-devel
Summary: The GNU Atomic static library
Requires: libatomic%{_isa} >= 4.8.0

%description -n devtoolset-11-libatomic-devel
This package contains GNU Atomic static libraries.

%package -n libasan6
Summary: The Address Sanitizer runtime library from GCC 11
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libasan6
This package contains the Address Sanitizer library from GCC 11
which is used for -fsanitize=address instrumented programs.

%package -n devtoolset-11-libasan-devel
Summary: The Address Sanitizer static library
%if 0%{?rhel} > 8
Requires: libasan%{_isa} >= 8.3.1
%else
Requires: libasan6%{_isa} >= 10.2.1
%endif
Obsoletes: libasan5 <= 8.3.1

%description -n devtoolset-11-libasan-devel
This package contains Address Sanitizer static runtime library.

%package -n libtsan
Summary: The Thread Sanitizer runtime library
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libtsan
This package contains the Thread Sanitizer library
which is used for -fsanitize=thread instrumented programs.

%package -n devtoolset-11-libtsan-devel
Summary: The Thread Sanitizer static library
Requires: libtsan%{_isa} >= 5.1.1

%description -n devtoolset-11-libtsan-devel
This package contains Thread Sanitizer static runtime library.

%package -n libubsan1
Summary: The Undefined Behavior Sanitizer runtime library
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libubsan1
This package contains the Undefined Behavior Sanitizer library
which is used for -fsanitize=undefined instrumented programs.

%package -n devtoolset-11-libubsan-devel
Summary: The Undefined Behavior Sanitizer static library
%if 0%{?rhel} > 7
Requires: libubsan%{_isa} >= 8.3.1
Obsoletes: libubsan1 <= 8.3.1
%else
Requires: libubsan1%{_isa} >= 8.3.1
%endif

%description -n devtoolset-11-libubsan-devel
This package contains Undefined Behavior Sanitizer static runtime library.

%package -n liblsan
Summary: The Leak Sanitizer runtime library
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n liblsan
This package contains the Leak Sanitizer library
which is used for -fsanitize=leak instrumented programs.

%package -n devtoolset-11-liblsan-devel
Summary: The Leak Sanitizer static library
Requires: liblsan%{_isa} >= 5.1.1

%description -n devtoolset-11-liblsan-devel
This package contains Leak Sanitizer static runtime library.

%package -n devtoolset-11-offload-nvptx
Summary: Offloading compiler to NVPTX
Requires: gcc >= 8.3.1
Requires: libgomp-offload-nvptx >= 8.3.1

%description -n devtoolset-11-offload-nvptx
The gcc-offload-nvptx package provides offloading support for
NVidia PTX.  OpenMP and OpenACC programs linked with -fopenmp will
by default add PTX code into the binaries, which can be offloaded
to NVidia PTX capable devices if available.

%prep

. /opt/rh/devtoolset-11/enable

%if 0%{?rhel} >= 7
%autosetup -p1 -n gcc-%{version}-%{DATE} -a 1 -a 4 -a 5
%else
%autosetup -p1 -n gcc-%{version}-%{DATE} -a 1 -a 2 -a 3 -a 7 -a 8
%endif

find gcc/testsuite -name \*.pr96939~ | xargs rm -f

echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

%if 0%{?rhel} == 6
# Default to -gdwarf-3 rather than -gdwarf-5
sed -i '/UInteger Var(dwarf_version)/s/Init(5)/Init(3)/' gcc/common.opt
sed -i 's/\(version for most targets is \)5 /\13 /' gcc/doc/invoke.texi
%endif
%if 0%{?rhel} <= 8
# Default to -gdwarf-4 rather than -gdwarf-5
sed -i '/UInteger Var(dwarf_version)/s/Init(5)/Init(4)/' gcc/common.opt
sed -i 's/\(version for most targets is \)5 /\14 /' gcc/doc/invoke.texi
%endif

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h
cp -a libstdc++-v3/config/cpu/i{4,3}86/opt
echo 'TM_H += $(srcdir)/config/rs6000/rs6000-modes.h' >> gcc/config/rs6000/t-rs6000

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

sed -i -e 's/Common Driver Var(flag_report_bug)/& Init(1)/' gcc/common.opt

%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/post/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/sparc64-linux-gnu/32
fi
%endif

# This test causes fork failures, because it spawns way too many threads
rm -f gcc/testsuite/go.test/test/chan/goroutines.go

# These tests get stuck and don't timeout.
%ifarch ppc ppc64 ppc64le
rm -f libgomp/testsuite/libgomp.c/target-*.c
rm -rf libgomp/testsuite/libgomp.oacc*
rm -rf libgomp/testsuite/libgomp.graphite*
%endif
# This test gets stuck.
%ifarch %{ix86} ppc64 s390x
rm -f libstdc++-v3/testsuite/30_threads/future/members/poll.cc
%endif

%build

# Undo the broken autoconf change in recent Fedora versions
export CONFIG_SITE=NONE

CC=gcc
CXX=g++
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-flto=auto//g;s/-flto//g;s/-ffat-lto-objects//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-Werror=format-security/-Wformat-security/g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables /' \
      libgcc/Makefile.in
    ;;
esac

%if %{build_offload_nvptx}
mkdir obji
IROOT=`pwd`/obji
cd nvptx-tools-%{nvptx_tools_gitrev}
rm -rf obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}
CC="$CC" CXX="$CXX" CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" \
../configure --prefix=%{_prefix}
make %{?_smp_mflags}
make install prefix=${IROOT}%{_prefix}
cd ../..

ln -sf newlib-cygwin-%{newlib_cygwin_gitrev}/newlib newlib
rm -rf obj-offload-nvptx-none
mkdir obj-offload-nvptx-none

cd obj-offload-nvptx-none
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
    CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
          | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
    XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
    ../configure --disable-bootstrap --disable-sjlj-exceptions \
    --enable-newlib-io-long-long --with-build-time-tools=${IROOT}%{_prefix}/nvptx-none/bin \
    --target nvptx-none --enable-as-accelerator-for=%{gcc_target_platform} \
    --enable-languages=c,c++,fortran,lto \
    --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
    --with-bugurl=http://bugzilla.redhat.com/bugzilla \
    --enable-checking=release --with-system-zlib \
    --with-gcc-major-version-only --without-isl
make %{?_smp_mflags}
cd ..
rm -f newlib
%endif

rm -rf obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if %{build_libstdcxx_docs}

%if 0%{?rhel} < 7
mkdir doxygen-install
pushd ../doxygen-%{doxygen_version}
./configure --prefix `cd ..; pwd`/obj-%{gcc_target_platform}/doxygen-install \
  --shared --release --english-only

make %{?_smp_mflags} all
make install
popd
export PATH=`pwd`/doxygen-install/bin/${PATH:+:${PATH}}
%endif
%endif

%if 0%{?rhel} < 7
# Build GMP for RHEL 6.  Build it first because MPC and MPFR need it.
mkdir gmp gmp-install
cd gmp
../../gmp-%{gmp_version}/configure --disable-shared --disable-assembly \
  CFLAGS="${CFLAGS:-%optflags} -fPIC" CXXFLAGS="${CXXFLAGS:-%optflags} -fPIC" \
  --prefix=`cd ..; pwd`/gmp-install
make %{?_smp_mflags}
make install
cd ..

# It also needs MPFR.
mkdir mpfr mpfr-install
cd mpfr
../../mpfr-%{mpfr_version}/configure --disable-shared \
  --with-gmp=`cd ..; pwd`/gmp-install \
  CFLAGS="${CFLAGS:-%optflags} -fPIC" CXXFLAGS="${CXXFLAGS:-%optflags} -fPIC" \
  --prefix=`cd ..; pwd`/mpfr-install
make %{?_smp_mflags}
make install
cd ..

mkdir mpc mpc-install
cd mpc
../../mpc-%{mpc_version}/configure --disable-shared \
  --with-mpfr=`cd ..; pwd`/mpfr-install \
  --with-gmp=`cd ..; pwd`/gmp-install \
  CFLAGS="${CFLAGS:-%optflags} -fPIC" CXXFLAGS="${CXXFLAGS:-%optflags} -fPIC" \
  --prefix=`cd ..; pwd`/mpc-install
make %{?_smp_mflags}
make install
cd ..
%endif

%if %{build_isl}
mkdir isl-build isl-install
%ifarch s390 s390x
ISL_FLAG_PIC=-fPIC
%else
ISL_FLAG_PIC=-fpic
%endif
pwd
cd ..
tar xjf ../../SOURCES/isl-%{isl_version}.tar.bz2
find . -type d -name "isl-%{isl_version}"
cd obj-x86_64-redhat-linux/isl-build
sed -i 's|libisl|libgcc11privateisl|g' \
  ../../isl-%{isl_version}/Makefile.{am,in}
../../isl-%{isl_version}/configure \
  CC=/usr/bin/gcc CXX=/usr/bin/g++ \
  CFLAGS="${CFLAGS:-%optflags} $ISL_FLAG_PIC" --prefix=`cd ..; pwd`/isl-install
make %{?_smp_mflags}
make install
cd ../isl-install/lib
rm libgcc11privateisl.so{,.15}
mv libgcc11privateisl.so.15.3.0 libisl.so.15
ln -sf libisl.so.15 libisl.so
cd ../..
%endif

%ifnarch s390
%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}
%endif
CONFIGURE_OPTS="\
    --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
    --with-bugurl=http://bugzilla.redhat.com/bugzilla \
    --enable-shared --enable-threads=posix --enable-checking=release \
%ifarch ppc64le
    --enable-targets=powerpcle-linux \
%endif
%if 0%{?multilib_enabled}
%ifarch ppc64le %{mips} s390x
    --disable-multilib \
%else
    --enable-multilib \
%endif
%else
    --disable-multilib \
%endif
    --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
    --enable-gnu-unique-object --enable-linker-build-id --with-gcc-major-version-only \
%ifnarch %{mips}
    --with-linker-hash-style=gnu \
%endif
%if 0%{?rhel} <= 7
    --with-default-libstdcxx-abi=gcc4-compatible \
%endif
    --enable-plugin --enable-initfini-array \
%if %{build_isl}
    --with-isl=`pwd`/isl-install \
%else
    --without-isl \
%endif
%if %{build_offload_nvptx}
    --enable-offload-targets=nvptx-none \
    --without-cuda-driver \
%endif
%if 0%{?rhel} < 7
    --with-mpc=`pwd`/mpc-install \
    --with-mpfr=`pwd`/mpfr-install \
    --with-gmp=`pwd`/gmp-install \
%endif
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
%if %{attr_ifunc}
    --enable-gnu-indirect-function \
%endif
%endif
%ifarch %{arm}
    --disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
    --enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 ppc64le ppc64p7 s390 s390x alpha
    --with-long-double-128 \
%endif
%ifarch sparc
    --disable-linux-futex \
%endif
%ifarch sparc64
    --with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
    --host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%ifarch ppc ppc64 ppc64p7
%if 0%{?rhel} >= 7
    --with-cpu-32=power7 --with-tune-32=power7 --with-cpu-64=power7 --with-tune-64=power7 \
%endif
%if 0%{?rhel} == 6
    --with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc64le
%if 0%{?rhel} == 9
    --with-cpu-32=power9 --with-tune-32=power9 --with-cpu-64=power9 --with-tune-64=power9 \
%else
    --with-cpu-32=power8 --with-tune-32=power8 --with-cpu-64=power8 --with-tune-64=power8 \
%endif
%endif
%ifarch ppc
    --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
%if 0%{?rhel} >= 8
    --enable-cet \
%endif
    --with-tune=generic \
%endif
%if 0%{?rhel} >= 7
%ifarch %{ix86}
    --with-arch=x86-64 \
%endif
%ifarch x86_64
%if 0%{?rhel} > 8
    --with-arch_64=x86-64-v2 \
%endif
    --with-arch_32=x86-64 \
%endif
%else
%ifarch %{ix86}
    --with-arch=i686 \
%endif
%ifarch x86_64
    --with-arch_32=i686 \
%endif
%endif
%ifarch s390 s390x
%if 0%{?rhel} >= 7
%if 0%{?rhel} > 7
%if 0%{?rhel} > 8
%if 0%{?rhel} == 9
    --with-arch=z14 --with-tune=z15 \
%else
    --with-arch=z13 --with-tune=arch13 \
%endif
%else
    --with-arch=z13 --with-tune=z14 \
%endif
%else
    --with-arch=z196 --with-tune=zEC12 \
%endif
%else
%if 0%{?fedora} >= 26
    --with-arch=zEC12 --with-tune=z13 \
%else
    --with-arch=z9-109 --with-tune=z10 \
%endif
%endif
    --enable-decimal-float \
%endif
%ifarch armv7hl
    --with-tune=generic-armv7-a --with-arch=armv7-a \
    --with-float=hard --with-fpu=vfpv3-d16 --with-abi=aapcs-linux \
%endif
%ifarch mips mipsel
    --with-arch=mips32r2 --with-fp-32=xx \
%endif
%ifarch mips64 mips64el
    --with-arch=mips64r2 --with-abi=64 \
%endif
%ifarch riscv64
    --with-arch=rv64gc --with-abi=lp64d --with-multilib-list=lp64d \
%endif
%ifnarch sparc sparcv9 ppc
    --build=%{gcc_target_platform} \
%endif
%if 0%{?fedora} >= 35
%ifarch x86_64 %{ix86} ppc64le s390x
    --with-build-config=bootstrap-lto --enable-link-serialization=1 \
%endif
%endif
    "

%if %{build_go}
enablelgo=,go
%endif
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
    CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
          | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
    XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
    ../configure --enable-bootstrap \
    --enable-languages=c,c++,fortran${enablelgo},lto \
    $CONFIGURE_OPTS

%ifarch sparc sparcv9 sparc64
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
%else
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap
%endif

%if 0%{?rhel} <= 8
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 -lstdc++_nonshared%{nonsharedver} )' \
  > %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_system.so

# Relink libcc1 against -lstdc++_nonshared:
sed -i -e '/^postdeps/s/-lstdc++/-lstdc++_system/' libcc1/libtool
rm -f libcc1/libcc1.la
make -C libcc1 libcc1.la
%endif

CC="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cc`"
CXX="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cxx` `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-includes`"

# Build libgccjit separately, so that normal compiler binaries aren't -fpic
# unnecessarily.
mkdir objlibgccjit
cd objlibgccjit
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
    CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
          | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
    XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
    ../../configure --disable-bootstrap --enable-host-shared \
    --enable-languages=jit $CONFIGURE_OPTS
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" all-gcc
cp -a gcc/libgccjit.so* ../gcc/
cd ../gcc/
ln -sf xgcc %{gcc_target_platform}-gcc-%{gcc_major}
cp -a Makefile{,.orig}
sed -i -e '/^CHECK_TARGETS/s/$/ check-jit/' Makefile
touch -r Makefile.orig Makefile
rm Makefile.orig
#make jit.sphinx.html
#make jit.sphinx.install-html jit_htmldir=`pwd`/../../rpm.doc/libgccjit-devel/html
cd ..

%if %{build_isl}
cp -a isl-install/lib/libisl.so.15 gcc/
%endif

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/libquadmath rpm.doc/libitm
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/jit,libstdc++-v3,libgomp,libcc1,libatomic,libsanitizer}

for i in {gcc,gcc/cp,gcc/jit,libstdc++-v3,libgomp,libcc1,libatomic,libsanitizer}/ChangeLog*; do
    cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/fortran; for i in ChangeLog*; do
    cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
    cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
%if 0%{!?build_libquadmath:1}
(cd libquadmath; for i in ChangeLog* COPYING.LIB; do
    cp -p $i ../rpm.doc/libquadmath/$i.libquadmath
done)
%endif
%if %{build_libitm}
(cd libitm; for i in ChangeLog*; do
    cp -p $i ../rpm.doc/libitm/$i.libitm
done)
%endif

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

# Test the nonshared bits.
mkdir libstdc++_compat_test
cd libstdc++_compat_test
readelf -Ws %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 | sed -n '/\.symtab/,$d;/ UND /d;/@GLIBC_PRIVATE/d;/\(GLOBAL\|WEAK\|UNIQUE\)/p' | awk '{ if ($4 == "OBJECT") { printf "%s %s %s %s %s\n", $8, $4, $5, $6, $3 } else { printf "%s %s %s %s\n", $8, $4, $5, $6 }}' | sed 's/ UNIQUE / GLOBAL /;s/ WEAK / GLOBAL /;s/@@GLIBCXX_\(LDBL_\)\?[0-9.]*//;s/@@CXXABI_TM_[0-9.]*//;s/@@CXXABI_FLOAT128//;s/@@CXXABI_\(LDBL_\)\?[0-9.]*//' | LC_ALL=C sort -u > system.abilist
readelf -Ws ../obj-%{gcc_target_platform}/%{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so.6 | sed -n '/\.symtab/,$d;/ UND /d;/@GLIBC_PRIVATE/d;/\(GLOBAL\|WEAK\|UNIQUE\)/p' | awk '{ if ($4 == "OBJECT") { printf "%s %s %s %s %s\n", $8, $4, $5, $6, $3 } else { printf "%s %s %s %s\n", $8, $4, $5, $6 }}' | sed 's/ UNIQUE / GLOBAL /;s/ WEAK / GLOBAL /;s/@@GLIBCXX_\(LDBL_\)\?[0-9.]*//;s/@@CXXABI_TM_[0-9.]*//;s/@@CXXABI_FLOAT128//;s/@@CXXABI_\(LDBL_\)\?[0-9.]*//' | LC_ALL=C sort -u > vanilla.abilist
diff -up system.abilist vanilla.abilist | awk '/^\+\+\+/{next}/^\+/{print gensub(/^+(.*)$/,"\\1","1",$0)}' > system2vanilla.abilist.diff
../obj-%{gcc_target_platform}/gcc/xgcc -B ../obj-%{gcc_target_platform}/gcc/ -shared -o libstdc++_nonshared.so -Wl,--whole-archive ../obj-%{gcc_target_platform}/%{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared%{nonsharedver}.a -Wl,--no-whole-archive %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6
readelf -Ws libstdc++_nonshared.so | sed -n '/\.symtab/,$d;/ UND /d;/@GLIBC_PRIVATE/d;/\(GLOBAL\|WEAK\|UNIQUE\)/p' | awk '{ if ($4 == "OBJECT") { printf "%s %s %s %s %s\n", $8, $4, $5, $6, $3 } else { printf "%s %s %s %s\n", $8, $4, $5, $6 }}' | sed 's/ UNIQUE / GLOBAL /;s/ WEAK / GLOBAL /;s/@@GLIBCXX_\(LDBL_\)\?[0-9.]*//;s/@@CXXABI_TM_[0-9.]*//;s/@@CXXABI_FLOAT128//;s/@@CXXABI_\(LDBL_\)\?[0-9.]*//' | LC_ALL=C sort -u > nonshared.abilist
echo ====================NONSHARED=========================
ldd -d -r ./libstdc++_nonshared.so || :
ldd -u ./libstdc++_nonshared.so || :
diff -up system2vanilla.abilist.diff nonshared.abilist || :
readelf -Ws ../obj-%{gcc_target_platform}/%{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared%{nonsharedver}.a | grep HIDDEN.*UND | grep -v __dso_handle || :
echo ====================NONSHARED END=====================
rm -f libstdc++_nonshared.so
cd ..

%install
rm -rf %{buildroot}

%if %{build_offload_nvptx}
cd nvptx-tools-%{nvptx_tools_gitrev}
cd obj-%{gcc_target_platform}
make install prefix=%{buildroot}%{_prefix}
cd ../..

ln -sf newlib-cygwin-%{newlib_cygwin_gitrev}/newlib newlib
cd obj-offload-nvptx-none
make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
rm -rf %{buildroot}%{_prefix}/libexec/gcc/nvptx-none/%{gcc_major}/install-tools
rm -rf %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/{install-tools,plugin,cc1,cc1plus,f951}
rm -rf %{buildroot}%{_infodir} %{buildroot}%{_mandir}/man7 %{buildroot}%{_prefix}/share/locale
rm -rf %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/{install-tools,plugin}
rm -rf %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/{install-tools,plugin,include-fixed}
rm -rf %{buildroot}%{_prefix}/%{_lib}/libc[cp]1*
mv -f %{buildroot}%{_prefix}/nvptx-none/lib/*.{a,spec} %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/
mv -f %{buildroot}%{_prefix}/nvptx-none/lib/mgomp/*.{a,spec} %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/mgomp/
mv -f %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/*.a %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/
mv -f %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/mgomp/*.a %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/mgomp/
find %{buildroot}%{_prefix}/lib/gcc/nvptx-none %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none \
     %{buildroot}%{_prefix}/nvptx-none/lib -name \*.la | xargs rm
cd ..
rm -f newlib
%endif

%if %{build_libstdcxx_docs}
%if 0%{?rhel} < 7
export PATH=`pwd`/obj-%{gcc_target_platform}/doxygen-install/bin/${PATH:+:${PATH}}
%endif
%endif

%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}
# Also set LD_LIBRARY_PATH so that DTS eu-strip (called from find-debuginfo.sh)
# can find the libraries it needs.
%{?scl:export LD_LIBRARY_PATH=%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}}

perl -pi -e \
  's~href="l(ibstdc|atest)~href="http://gcc.gnu.org/onlinedocs/libstdc++/l\1~' \
  libstdc++-v3/doc/html/api.html

cd obj-%{gcc_target_platform}

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

%if 0%{?scl:1}
rm -f gcc/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
GROUP ( /%{_lib}/libgcc_s.so.1 libgcc.a )' > gcc/libgcc_s.so
%endif

make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install

%if 0%{?scl:1}
rm -f gcc/libgcc_s.so
ln -sf libgcc_s.so.1 gcc/libgcc_s.so
%endif

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}

%if 0%{?scl:1}
ln -sf ../../../../bin/ar $FULLEPATH/ar
ln -sf ../../../../bin/as $FULLEPATH/as
ln -sf ../../../../bin/ld $FULLEPATH/ld
ln -sf ../../../../bin/ld.bfd $FULLEPATH/ld.bfd
ln -sf ../../../../bin/ld.gold $FULLEPATH/ld.gold
ln -sf ../../../../bin/nm $FULLEPATH/nm
ln -sf ../../../../bin/objcopy $FULLEPATH/objcopy
ln -sf ../../../../bin/ranlib $FULLEPATH/ranlib
ln -sf ../../../../bin/strip $FULLEPATH/strip
%endif

%if %{build_isl}
cp -a isl-install/lib/libisl.so.15 $FULLPATH/
%endif

# fix some things
ln -sf gcc %{buildroot}%{_prefix}/bin/cc
mkdir -p %{buildroot}/lib
ln -sf ..%{_prefix}/bin/cpp %{buildroot}/lib/cpp
ln -sf gfortran %{buildroot}%{_prefix}/bin/f95
rm -f %{buildroot}%{_infodir}/dir
gzip -9 %{buildroot}%{_infodir}/*.info*
ln -sf gcc %{buildroot}%{_prefix}/bin/gnatgcc

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/32/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%endif
#else
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
%endif
#endif
#endif
EOF
    break
  fi
done

for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
%if 0%{?rhel} <= 7
  # Force the old ABI unconditionally, the new one does not work in the
  # libstdc++_nonshared.a model against RHEL 6/7 libstdc++.so.6.
  sed -i -e 's/\(define[[:blank:]]*_GLIBCXX_USE_DUAL_ABI[[:blank:]]*\)1/\10/' $f
%endif
done

# Nuke bits/*.h.gch dirs
# 1) there is no bits/*.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/bits/*.h.gch

%if %{build_libstdcxx_docs}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
cp -r -p $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}/man3
cp -r -p $libstdcxx_doc_builddir/man/man3/* %{buildroot}%{_mandir}/man3/
find ../rpm.doc/libstdc++-v3 -name \*~ | xargs rm
%endif

%ifarch sparcv9 sparc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc ppc64 ppc64p7
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif

%ifarch sparcv9 ppc
FULLLPATH=$FULLPATH/lib32
%endif
%ifarch sparc64 ppc64 ppc64p7
FULLLPATH=$FULLPATH/lib64
%endif
if [ -n "$FULLLPATH" ]; then
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f

mv %{buildroot}%{_prefix}/%{_lib}/libgfortran.spec $FULLPATH/
%if %{build_libitm}
mv %{buildroot}%{_prefix}/%{_lib}/libitm.spec $FULLPATH/
%endif
%if %{build_libasan}
mv %{buildroot}%{_prefix}/%{_lib}/libsanitizer.spec $FULLPATH/
%endif

mkdir -p %{buildroot}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_major}-%{DATE}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%ifarch sparcv9 ppc
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%if 0%{?multilib_enabled}
%ifarch %{multilib_64_archs}
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif
%endif

rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
GROUP ( /%{_lib}/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%ifarch sparcv9 ppc
rm -f $FULLPATH/64/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
GROUP ( /lib64/libgcc_s.so.1 libgcc.a )' > $FULLPATH/64/libgcc_s.so
%endif
%if 0%{?multilib_enabled}
%ifarch %{multilib_64_archs}
rm -f $FULLPATH/32/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/32/libgcc_s.so
%endif
%endif

mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/
cp -a %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared%{nonsharedver}.a \
  $FULLLPATH/libstdc++_nonshared.a
cp -a %{gcc_target_platform}/libgfortran/.libs/libgfortran_nonshared80.a \
  $FULLLPATH/libgfortran_nonshared.a

%if 0%{?rhel} <= 7
# Build libgomp_nonshared.a with the system compiler.  Use -O2 to
# get tailcalls.
gcc %{SOURCE6} -O2 -c
ar rcs libgomp_nonshared.a libgomp_nonshared.o
cp -a libgomp_nonshared.a $FULLLPATH
%if 0
%ifarch x86_64
# Only need this for -m32 on x86_64.  devtoolset-N-gcc isn't multilib,
# and we don't have a devtoolset-N-libgomp-devel subpackage.
gcc %{SOURCE6} -O2 -c -m32 -o libgomp_nonshared32.o
ar rcs libgomp_nonshared32.a libgomp_nonshared32.o
cp -a libgomp_nonshared32.a $FULLLPATH/32/libgomp_nonshared.a
%endif
%endif
%endif

mkdir -p %{buildroot}%{_prefix}/libexec/getconf
if gcc/xgcc -B gcc/ -E -P -dD -xc /dev/null | grep '__LONG_MAX__.*\(2147483647\|0x7fffffff\($\|[LU]\)\)'; then
  ln -sf POSIX_V6_ILP32_OFF32 %{buildroot}%{_prefix}/libexec/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 %{buildroot}%{_prefix}/libexec/getconf/default
fi

mkdir -p %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++*gdb.py* \
      %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
pushd ../libstdc++-v3/python
for i in `find . -name \*.py`; do
  touch -r $i %{buildroot}%{_prefix}/share/gcc-%{gcc_major}/python/$i
done
touch -r hook.in %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc++*gdb.py
popd
for f in `find %{buildroot}%{_prefix}/share/gcc-%{gcc_major}/python/ \
           %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/ -name \*.py`; do
  r=${f/$RPM_BUILD_ROOT/}
%if 0%{?rhel} <= 7
  %{__python} -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
  %{__python} -O -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
%else
  %{__python3} -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
  %{__python3} -O -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
%endif
done

rm -f $FULLEPATH/libgccjit.so
mkdir -p %{buildroot}%{_prefix}/%{_lib}/
cp -a objlibgccjit/gcc/libgccjit.so.* %{buildroot}%{_prefix}/%{_lib}/
rm -f $FULLPATH/libgccjit.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{_prefix}/%{_lib}/libgccjit.so.0 )' > $FULLPATH/libgccjit.so
cp -a ../gcc/jit/libgccjit*.h $FULLPATH/include/
/usr/bin/install -c -m 644 objlibgccjit/gcc/doc/libgccjit.info %{buildroot}/%{_infodir}/
gzip -9 %{buildroot}/%{_infodir}/libgccjit.info

pushd $FULLPATH
%if 0%{?rhel} <= 7
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libgomp.so.1 -lgomp_nonshared )' > libgomp.so
%else
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libgomp.so.1 )' > libgomp.so
%endif

%if 0%{?rhel} <= 8
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 -lstdc++_nonshared )' > libstdc++.so
%else
echo '%{oformat}
INPUT ( %{_root_prefix}/%{_lib}/libstdc++.so.6 )' > libstdc++.so
%endif
rm -f libgfortran.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libgfortran.so.5 -lgfortran_nonshared )' > libgfortran.so
%if 0%{!?build_libquadmath:1}
rm -f libquadmath.so
echo '/* GNU ld script */
%{oformat}
%if 0%{!?scl:1}
INPUT ( %{_prefix}/%{_lib}/libquadmath.so.0 )' > libquadmath.so
%else
%if 0%{?rhel} >= 7
INPUT ( %{_root_prefix}/%{_lib}/libquadmath.so.0 )' > libquadmath.so
%else
INPUT ( libquadmath.a )' > libquadmath.so
%endif
%endif
%endif
%if %{build_libitm}
rm -f libitm.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libitm.so.1 )' > libitm.so
%endif
%if %{build_libatomic}
rm -f libatomic.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libatomic.so.1 )' > libatomic.so
%endif
%if %{build_libasan}
rm -f libasan.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libasan.so.6 )' > libasan.so
%endif
%if %{build_libtsan}
rm -f libtsan.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libtsan.so.0 )' > libtsan.so
%endif
%if %{build_libubsan}
rm -f libubsan.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libubsan.so.1 )' > libubsan.so
%endif
%if %{build_liblsan}
rm -f liblsan.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/liblsan.so.0 )' > liblsan.so
%endif
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++fs.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.*a .
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
%if 0%{!?build_libquadmath:1}
mv -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.*a $FULLLPATH/
%endif
%if %{build_libitm}
mv -f %{buildroot}%{_prefix}/%{_lib}/libitm.*a $FULLLPATH/
%endif
%if %{build_libatomic}
mv -f %{buildroot}%{_prefix}/%{_lib}/libatomic.*a $FULLLPATH/
%endif
%if %{build_libasan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libasan.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libasan_preinit.o $FULLLPATH/
%endif
%if %{build_libtsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libtsan.*a $FULLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libtsan_preinit.o $FULLPATH/
%endif
%if %{build_libubsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libubsan.*a $FULLLPATH/
%endif
%if %{build_liblsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/liblsan.*a $FULLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/liblsan_preinit.o $FULLPATH/
%endif

%ifarch sparcv9 ppc
%if 0%{?rhel} <= 8
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libstdc++.so.6 -lstdc++_nonshared )' > 64/libstdc++.so
%else
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( %{_root_prefix}/lib64/libstdc++.so.6 )' > 64/libstdc++.so
%endif
rm -f 64/libgfortran.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libgfortran.so.5 -lgfortran_nonshared )' > 64/libgfortran.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libgomp.so.1 )' > 64/libgomp.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{_prefix}/lib64/libgccjit.so.0 )' > 64/libgccjit.so
%if 0%{!?build_libquadmath:1}
rm -f 64/libquadmath.so
echo '/* GNU ld script */
%{oformat2}
%if 0%{!?scl:1}
INPUT ( %{_prefix}/lib64/libquadmath.so.0 )' > 64/libquadmath.so
%else
%if 0%{?rhel} >= 7
INPUT ( %{_root_prefix}/lib64/libquadmath.so.0 )' > 64/libquadmath.so
%else
INPUT ( libquadmath.a )' > 64/libquadmath.so
%endif
%endif
%endif
%if %{build_libitm}
rm -f 64/libitm.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libitm.so.1 )' > 64/libitm.so
%endif
%if %{build_libatomic}
rm -f 64/libatomic.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libatomic.so.1 )' > 64/libatomic.so
%endif
%if %{build_libasan}
rm -f 64/libasan.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libasan.so.6 )' > 64/libasan.so
%endif
%if %{build_libubsan}
rm -f 64/libubsan.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libubsan.so.1 )' > 64/libubsan.so
%endif
mv -f %{buildroot}%{_prefix}/lib64/libsupc++.*a 64/
mv -f %{buildroot}%{_prefix}/lib64/libgfortran.*a 64/
mv -f %{buildroot}%{_prefix}/lib64/libgomp.*a 64/
%if 0%{!?build_libquadmath:1}
mv -f %{buildroot}%{_prefix}/lib64/libquadmath.*a 64/
%endif
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libstdc++fs.a libstdc++fs.a
ln -sf ../lib64/libstdc++fs.a 64/libstdc++fs.a
ln -sf lib32/libstdc++_nonshared.a libstdc++_nonshared.a
ln -sf ../lib64/libstdc++_nonshared.a 64/libstdc++_nonshared.a
%if 0%{!?build_libquadmath:1}
ln -sf lib32/libquadmath.a libquadmath.a
ln -sf ../lib64/libquadmath.a 64/libquadmath.a
%endif
%if %{build_libitm}
ln -sf lib32/libitm.a libitm.a
ln -sf ../lib64/libitm.a 64/libitm.a
%endif
%if %{build_libatomic}
ln -sf lib32/libatomic.a libatomic.a
ln -sf ../lib64/libatomic.a 64/libatomic.a
%endif
%if %{build_libasan}
ln -sf lib32/libasan.a libasan.a
ln -sf ../lib64/libasan.a 64/libasan.a
ln -sf lib32/libasan_preinit.o libasan_preinit.o
ln -sf ../lib64/libasan_preinit.o 64/libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf lib32/libubsan.a libubsan.a
ln -sf ../lib64/libubsan.a 64/libubsan.a
%endif
%endif
%if 0%{?multilib_enabled}
%ifarch %{multilib_64_archs}
mkdir -p 32
%if 0%{?rhel} <= 8
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libstdc++.so.6 -lstdc++_nonshared )' > 32/libstdc++.so
%else
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( %{_root_prefix}/lib/libstdc++.so.6 )' > 32/libstdc++.so
%endif
rm -f 32/libgfortran.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libgfortran.so.5 -lgfortran_nonshared )' > 32/libgfortran.so

%if 0%{?rhel} <= 7
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libgomp.so.1 -lgomp_nonshared )' > 32/libgomp.so
%else
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libgomp.so.1 )' > 32/libgomp.so
%endif

echo '/* GNU ld script */
%{oformat2}
INPUT ( %{_prefix}/lib/libgccjit.so.0 )' > 32/libgccjit.so
%if 0%{!?build_libquadmath:1}
rm -f 32/libquadmath.so
echo '/* GNU ld script */
%{oformat2}
%if 0%{!?scl:1}
INPUT ( %{_prefix}/lib/libquadmath.so.0 )' > 32/libquadmath.so
%else
%if 0%{?rhel} >= 7
INPUT ( %{_root_prefix}/lib/libquadmath.so.0 )' > 32/libquadmath.so
%else
INPUT ( libquadmath.a )' > 32/libquadmath.so
%endif
%endif
%endif
%if %{build_libitm}
rm -f 32/libitm.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libitm.so.1 )' > 32/libitm.so
%endif
%if %{build_libatomic}
rm -f 32/libatomic.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libatomic.so.1 )' > 32/libatomic.so
%endif
%if %{build_libasan}
rm -f 32/libasan.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libasan.so.6 )' > 32/libasan.so
%endif
%if %{build_libubsan}
rm -f 32/libubsan.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libubsan.so.1 )' > 32/libubsan.so
%endif
mv -f %{buildroot}%{_prefix}/lib/libsupc++.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libgfortran.*a 32/
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
%if 0%{!?build_libquadmath:1}
mv -f %{buildroot}%{_prefix}/lib/libquadmath.*a 32/
%endif
%endif
%endif
%ifarch sparc64 ppc64
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libstdc++fs.a 32/libstdc++fs.a
ln -sf lib64/libstdc++fs.a libstdc++fs.a
%if 0%{?rhel} <= 8
ln -sf ../lib32/libstdc++_nonshared.a 32/libstdc++_nonshared.a
ln -sf lib64/libstdc++_nonshared.a libstdc++_nonshared.a
%endif
%if 0%{?rhel} <= 8
ln -sf ../lib32/libgfortran_nonshared.a 32/libgfortran_nonshared.a
ln -sf lib64/libgfortran_nonshared.a libgfortran_nonshared.a
ln -sf lib64/libgomp_nonshared.a libgomp_nonshared.a
%endif
%if 0%{!?build_libquadmath:1}
ln -sf ../lib32/libquadmath.a 32/libquadmath.a
ln -sf lib64/libquadmath.a libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../lib32/libitm.a 32/libitm.a
ln -sf lib64/libitm.a libitm.a
%endif
%if %{build_libatomic}
ln -sf ../lib32/libatomic.a 32/libatomic.a
ln -sf lib64/libatomic.a libatomic.a
%endif
%if %{build_libasan}
ln -sf ../lib32/libasan.a 32/libasan.a
ln -sf lib64/libasan.a libasan.a
ln -sf ../lib32/libasan_preinit.o 32/libasan_preinit.o
ln -sf lib64/libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../lib32/libubsan.a 32/libubsan.a
mv -f lib64/libubsan.a libubsan.a
%endif
%else
%if 0%{?multilib_enabled}
%ifarch %{multilib_64_archs}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_major}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_major}/libstdc++fs.a 32/libstdc++fs.a
%if 0%{?rhel} <= 8
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_major}/libstdc++_nonshared.a 32/libstdc++_nonshared.a
%endif
%if 0%{?rhel} <= 8
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_major}/libgfortran_nonshared.a 32/libgfortran_nonshared.a
%endif
%if 0%{!?build_libquadmath:1}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_major}/libquadmath.a 32/libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_major}/libitm.a 32/libitm.a
%endif
%if %{build_libatomic}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_major}/libatomic.a 32/libatomic.a
%endif
%if %{build_libasan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_major}/libasan.a 32/libasan.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_major}/libasan_preinit.o 32/libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_major}/libubsan.a 32/libubsan.a
%endif
%endif
%endif
%endif

# If we are building a debug package then copy all of the static archives
# into the debug directory to keep them as unstripped copies.
%if 0%{?_enable_debug_packages}
mkdir -p $RPM_BUILD_ROOT%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
adirs="$FULLPATH"
if [ $FULLLPATH -ne $FULLPATH ]; then
  adirs="$adirs $FULLLPATH"
fi
for f in `find $adirs -maxdepth 1 -a \
         \( -name libgfortran.a -o -name libgomp.a \
            -o -name libgcc.a -o -name libgcc_eh.a -o -name libgcov.a \
            -o -name libquadmath.a -o -name libitm.a \
            -o -name libatomic.a -o -name libasan.a \
            -o -name libtsan.a -o -name libubsan.a \
            -o -name liblsan.a \
            -o -name libcc1.a \
            -o -name libstdc++_nonshared.a \
            -o -name libgomp_nonshared.a \
            -o -name libgfortran_nonshared.a \
            -o -name libsupc++.a \
            -o -name libstdc++.a -o -name libcaf_single.a \
            -o -name libstdc++fs.a \) -a -type f`; do
  cp -a $f $RPM_BUILD_ROOT%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/
done
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a  -o -name libgomp.a \
            -o -name libgcc.a -o -name libgcov.a \
            -o -name libquadmath.a -o -name libitm.a \
            -o -name libatomic.a -o -name libasan.a \
            -o -name libtsan.a -o -name libubsan.a \
            -o -name liblsan.a \
            -o -name libcc1.a \) -a -type f`
popd
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgfortran.so.5.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libcc1.so.0.*
%if 0%{!?build_libquadmath:1}
%if 0%{!?scl:1}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libquadmath.so.0.*
%endif
%endif
%if %{build_libitm}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libitm.so.1.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libitm.so.1* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
%if 0%{?rhel} <= 7
mv %{buildroot}%{_infodir}/libitm.info* %{buildroot}%{_root_infodir}/
%endif
%endif
%endif
%if %{build_libatomic}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libatomic.so.1.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libatomic.so.1* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
%endif
%endif
%if %{build_libasan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libasan.so.6.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libasan.so.6* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
%endif
%endif
%if %{build_libtsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libtsan.so.0.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libtsan.so.0* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
%endif
%endif
%if %{build_libubsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libubsan.so.1.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libubsan.so.1* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
%endif
%endif
%if %{build_liblsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/liblsan.so.0.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/liblsan.so.0* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
%endif
%endif

mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done


cd ..

%if 0%{!?scl:1}
for i in %{buildroot}%{_prefix}/bin/{*gcc,*++,gcov,gfortran,gcc-ar,gcc-nm,gcc-ranlib}; do
  mv -f $i ${i}5
done
%endif

# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f %{buildroot}%{_prefix}/%{_lib}/{libffi*,libiberty.a,libstdc++*,libgfortran*} || :
%if 0%{?scl:1}
rm -f %{buildroot}%{_prefix}/%{_lib}/{libquadmath*,libitm*,libatomic*,libasan*,libtsan*,libubsan*,liblsan*}
%else
%if 0%{?rhel} >= 7
rm -f %{buildroot}%{_prefix}/%{_lib}/{libitm*,libatomic*}
%endif
%endif
rm -f %{buildroot}%{_prefix}/%{_lib}/libgomp*
rm -f %{buildroot}/%{_lib}/libgcc_s*
rm -f $FULLEPATH/install-tools/{mkheaders,fixincl}
rm -f %{buildroot}%{_prefix}/lib/{32,64}/libiberty.a
rm -f %{buildroot}%{_prefix}/%{_lib}/libssp*
rm -f %{buildroot}%{_prefix}/%{_lib}/libvtv* || :
rm -f %{buildroot}/lib/cpp
rm -f %{buildroot}/%{_lib}/libgcc_s*
rm -f %{buildroot}%{_prefix}/bin/{f95,gccbug,gnatgcc*}
rm -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gfortran
%if 0%{!?scl:1}
rm -f %{buildroot}%{_prefix}/bin/{*c++*,cc,cpp}
%endif
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gfortran || :

%if 0%{?multilib_enabled}
%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
rm -f %{buildroot}/lib/libgcc_s*.so*
%else
%ifarch sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
rm -f %{buildroot}/lib64/libgcc_s*.so*
%endif
%endif

%ifnarch sparc64 ppc64
%ifarch %{multilib_64_archs}
cat <<\EOF > %{buildroot}%{_prefix}/bin/%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}-gcc-%{gcc_major}
#!/bin/sh
%ifarch s390x
exec %{gcc_target_platform}-gcc-%{gcc_major} -m31 "$@"
%else
exec %{gcc_target_platform}-gcc-%{gcc_major} -m32 "$@"
%endif
EOF
chmod 755 %{buildroot}%{_prefix}/bin/%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}-gcc-%{gcc_major}
%endif
%endif

%endif

# Help plugins find out nvra.
echo gcc-%{version}-%{release}.%{arch} > $FULLPATH/rpmver

# Add symlink to lto plugin in the binutils plugin directory.
%{__mkdir_p} %{buildroot}%{_libdir}/bfd-plugins/
ln -s ../../libexec/gcc/%{gcc_target_platform}/%{gcc_major}/liblto_plugin.so \
  %{buildroot}%{_libdir}/bfd-plugins/

%check
cd obj-%{gcc_target_platform}

%ifarch s390x ppc64
exit 0
%endif

%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}
%if 0%{?rhel} <= 8
# Test against the system libstdc++.so.6 + libstdc++_nonshared.a combo
mv %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so.6{,.not_here}
mv %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so{,.not_here}
ln -sf %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 \
  %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so.6
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 -lstdc++_nonshared )' \
  > %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so
cp -a %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared%{nonsharedver}.a \
  %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared.a
%endif

%if 0%{?run_tests}
# run the tests.
LC_ALL=C make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ \
%if 0%{?fedora} >= 20 || 0%{?rhel} > 7
     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector-strong}'" || :
%else
%ifnarch ppc ppc64 ppc64le s390x
     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
%else
    || :
%endif
%endif
( LC_ALL=C ../contrib/test_summary -t || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}' > testresults
rm -rf gcc/testsuite.prev
mv gcc/testsuite{,.prev}
rm -f gcc/site.exp
LC_ALL=C make %{?_smp_mflags} -C gcc -k check-gcc check-g++ ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}' compat.exp struct-layout-1.exp" || :
mv gcc/testsuite/gcc/gcc.sum{,.sent}
mv gcc/testsuite/g++/g++.sum{,.sent}
( LC_ALL=C ../contrib/test_summary -o -t || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}' > testresults2
rm -rf gcc/testsuite.compat
mv gcc/testsuite{,.compat}
mv gcc/testsuite{.prev,}
echo ====================TESTING=========================
cat testresults
echo ===`gcc --version | head -1` compatibility tests====
cat testresults2
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
for i in `find gcc/testsuite.compat -name \*.log | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/`basename $i`.compat || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}
%endif

%if 0%{?scl:1}
%post gfortran
if [ -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%preun gfortran
if [ $1 = 0 -a -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi
%endif

%post gdb-plugin -p /sbin/ldconfig

%postun gdb-plugin -p /sbin/ldconfig

%post -n devtoolset-11-libgccjit -p /sbin/ldconfig

%postun -n devtoolset-11-libgccjit -p /sbin/ldconfig

%if 0
%post -n devtoolset-11-libgccjit-docs
if [ -f %{_infodir}/libgccjit.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libgccjit.info.gz || :
fi

%preun -n devtoolset-11-libgccjit-docs
if [ $1 = 0 -a -f %{_infodir}/libgccjit.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgccjit.info.gz || :
fi
%endif

%post -n libquadmath
/sbin/ldconfig
if [ -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%preun -n libquadmath
if [ $1 = 0 -a -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%postun -n libquadmath -p /sbin/ldconfig

%post -n libitm
/sbin/ldconfig
if [ -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%preun -n libitm
if [ $1 = 0 -a -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%postun -n libitm -p /sbin/ldconfig

%post -n libatomic -p /sbin/ldconfig

%postun -n libatomic -p /sbin/ldconfig

%post -n libasan6 -p /sbin/ldconfig

%postun -n libasan6 -p /sbin/ldconfig

%post -n libtsan -p /sbin/ldconfig

%postun -n libtsan -p /sbin/ldconfig

%post -n libubsan1 -p /sbin/ldconfig

%postun -n libubsan1 -p /sbin/ldconfig

%post -n liblsan -p /sbin/ldconfig

%postun -n liblsan -p /sbin/ldconfig

%files
%{_prefix}/bin/gcc%{!?scl:11}
%{_prefix}/bin/gcov%{!?scl:11}
%{_prefix}/bin/gcov-tool%{!?scl:11}
%{_prefix}/bin/gcov-dump%{!?scl:11}
%{_prefix}/bin/gcc-ar%{!?scl:11}
%{_prefix}/bin/gcc-nm%{!?scl:11}
%{_prefix}/bin/gcc-ranlib%{!?scl:11}
%ifarch ppc
%{_prefix}/bin/%{_target_platform}-gcc%{!?scl:11}
%endif
%ifarch sparc64 sparcv9
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}%{?_gnu}-gcc%{!?scl:11}
%endif
%ifarch ppc64 ppc64p7
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}%{?_gnu}-gcc%{!?scl:11}
%endif
%{_prefix}/bin/%{gcc_target_platform}-gcc%{!?scl:11}
%{_prefix}/bin/%{gcc_target_platform}-gcc-%{gcc_major}
%ifnarch sparc64 ppc64
%if 0%{?multilib_enabled}
%ifarch %{multilib_64_archs}
%{_prefix}/bin/%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}-gcc-%{gcc_major}
%endif
%endif
%endif
%if 0%{?scl:1}
%{_prefix}/bin/cc
%{_prefix}/bin/cpp
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/cpp.1*
%{_mandir}/man1/gcov.1*
%{_mandir}/man1/gcov-tool.1*
%{_mandir}/man1/gcov-dump.1*
%{_infodir}/gcc*
%{_infodir}/cpp*
%endif
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/liblto_plugin.so*
%{_libdir}/bfd-plugins/liblto_plugin.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/rpmver
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/openacc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/acc_prof.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdnoreturn.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdatomic.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/gcov.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fxsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsaveintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsaveoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512cdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512erintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512fintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512pfintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/shaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cross-stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512dqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512ifmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512ifmavlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vlbwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vldqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clflushoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clwbintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mwaitxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsavecintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsavesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clzerointrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pkuintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx5124fmapsintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx5124vnniwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vpopcntdqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sgxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/gfniintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cetintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cet.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmi2vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vnniintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vnnivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vaesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vpclmulqdqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vpopcntdqvlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bitalgintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pconfigintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/wbnoinvdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/movdirintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/waitpkgintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cldemoteintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bf16vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bf16intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/enqcmdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vp2intersectintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vp2intersectvlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/serializeintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tsxldtrkintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxtileintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxint8intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxbf16intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86gprintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/uintrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/hresetintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/keylockerintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxvnniintrin.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ia64intrin.h
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ppu_intrinsics.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/si2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/spu2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vec_types.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmxlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amo.h
%endif
%ifarch %{arm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_acle.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_cmse.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_fp16.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_bf16.h
%endif
%ifarch aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_acle.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_fp16.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_bf16.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_sve.h
%endif
%ifarch sparc sparcv9 sparc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/visintrin.h
%endif
%ifarch s390 s390x
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/s390intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmxlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vecintrin.h
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sanitizer
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/collect2
%if 0%{?scl:1}
%if 0%{?rhel} <= 7
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/ar
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/as
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/ld
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/ld.bfd
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/ld.gold
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/nm
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/objcopy
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/ranlib
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/strip
%endif
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.so
%if 0%{?rhel} <= 7
%ifnarch ppc
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp_nonshared.a
%endif
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.spec
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsanitizer.spec
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%if 0%{!?build_libquadmath:1}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.so
%endif
%endif
%if %{build_isl}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libisl.so.*
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgccjit.so
%if 0%{!?build_libquadmath:1}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libubsan.so
%endif
%endif
%if 0%{?multilib_enabled}
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgomp.so

# Add libgomp_nonshared.a
%if 0%{?rhel} <= 7
%ifarch x86_64
# Need it for -m32.
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgomp_nonshared.a
%endif
%ifarch ppc64
# We've created a symlink to lib64/libgomp_nonshared.a, so add it.
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgomp_nonshared.a
%endif
%endif
%endif

%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgccjit.so
%if 0%{!?build_libquadmath:1}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libubsan.so
%endif
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%if 0%{!?build_libquadmath:1}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.so
%endif
%if %{build_libtsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.so
%endif
%if %{build_liblsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.so
%endif
%endif
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* gcc/COPYING* COPYING.RUNTIME

%files c++
%{_prefix}/bin/%{gcc_target_platform}-g++%{!?scl:11}
%{_prefix}/bin/g++%{!?scl:11}
%if 0%{?scl:1}
%{_prefix}/bin/%{gcc_target_platform}-c++
%{_prefix}/bin/c++
%{_mandir}/man1/g++.1*
%endif
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1plus
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/g++-mapper-server
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++_nonshared.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libsupc++.a
%endif
%if 0%{?multilib_enabled}
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++_nonshared.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libsupc++.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsupc++.a
%endif
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++_nonshared.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n devtoolset-11-libstdc++%{!?scl:11}-devel
%defattr(-,root,root,-)
%dir %{_prefix}/include/c++
%{_prefix}/include/c++/%{gcc_major}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libstdc++_nonshared.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libstdc++_nonshared.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++_nonshared.a
%endif
%if 0%{?multilib_enabled}
%ifnarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsupc++.a
%endif
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*


%if %{build_libstdcxx_docs}
%files -n devtoolset-11-libstdc++%{!?scl:11}-docs
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%if %{build_go}
%files go
%{_prefix}/bin/*gccgo
%{_prefix}/bin/*go
%{_prefix}/bin/*gofmt
%{_prefix}/lib64/libgo*
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/go1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet
%dir %{_prefix}/lib64/go
%dir %{_prefix}/lib64/go/%{gcc_major}
%dir %{_prefix}/lib64/go/%{gcc_major}/%{gcc_target_platform}
%{_prefix}/lib64/go/%{gcc_major}/%{gcc_target_platform}/*
%endif

%files gfortran
%{_prefix}/bin/gfortran%{!?scl:11}
%if 0%{?scl:1}
%{_mandir}/man1/gfortran.1*
%{_infodir}/gfortran*
%endif
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ISO_Fortran_binding.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_arithmetic.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_exceptions.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_features.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran_nonshared.a
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/finclude
%endif
%if 0%{?multilib_enabled}
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgfortran_nonshared.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/finclude
%endif
%endif
%ifarch ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgfortran_nonshared.a
%endif
%doc rpm.doc/gfortran/*

%if 0%{!?build_libquadmath:1}
%files -n devtoolset-11-libquadmath-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/quadmath.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/quadmath_weak.h
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libquadmath.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libquadmath.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.so
%endif
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch %{ix86}
# Need it for -m32.
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran_nonshared.a
%endif
%doc rpm.doc/libquadmath/ChangeLog*
%endif

%if %{build_libitm}
%files -n devtoolset-11-libitm-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libitm.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libitm.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.a
%endif
%doc rpm.doc/libitm/ChangeLog*
%endif

%if %{build_libatomic}
%files -n devtoolset-11-libatomic-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libatomic.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libatomic.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.a
%endif
%doc rpm.doc/changelogs/libatomic/ChangeLog*
%endif

%if %{build_libasan}
%files -n libasan6
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libasan.so.6*

%files -n devtoolset-11-libasan-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libasan_preinit.o
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libasan_preinit.o
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan_preinit.o
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%endif

%if %{build_libtsan}
# Use the system libtsan.
%if 0%{?rhel} < 8
%files -n libtsan
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libtsan.so.0*
%endif

%files -n devtoolset-11-libtsan-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan_preinit.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%endif

%if %{build_libubsan}
# GTS 11 libubsan1 would clash with the system RHEL 8 libubsan.
%if 0%{?rhel} < 8
%files -n libubsan1
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libubsan.so.1*
%endif

%files -n devtoolset-11-libubsan-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%endif

%if %{build_liblsan}
# Use the system liblsan.
%if 0%{?rhel} < 8
%files -n liblsan
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/liblsan.so.0*
%endif

%files -n devtoolset-11-liblsan-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan_preinit.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%endif

%files -n devtoolset-11-libgccjit
%{_prefix}/%{_lib}/libgccjit.so*
%doc rpm.doc/changelogs/gcc/jit/ChangeLog*

%files -n devtoolset-11-libgccjit-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgccjit.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/libgccjit*.h

%if 0
%files -n devtoolset-11-libgccjit-docs
%{_infodir}/libgccjit.info*
%doc rpm.doc/libgccjit-devel/*
%doc gcc/jit/docs/examples
%endif

%files plugin-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/gtype.state
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/include
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/plugin

%files gdb-plugin
%{_prefix}/%{_lib}/libcc1.so*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/libcc1plugin.so*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/libcp1plugin.so*
%doc rpm.doc/changelogs/libcc1/ChangeLog*

%if %{build_offload_nvptx}

%{_prefix}/bin/nvptx-none-*
%{_prefix}/bin/%{gcc_target_platform}-accel-nvptx-none-gcc
%{_prefix}/bin/%{gcc_target_platform}-accel-nvptx-none-lto-dump
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel
%{_prefix}/lib/gcc/nvptx-none
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none
%dir %{_prefix}/nvptx-none
%{_prefix}/nvptx-none/bin
%{_prefix}/nvptx-none/include
 %endif

%changelog
* Thu Mar  2 2023 Bernhard Kaindl <bernhard.kaindl@citrix.com> - 11.2.1-6
- CP-42316: Add and enable building the devtoolset-11-gcc-go package

* Wed Apr 13 2022 Andrew Cooper <andrew.cooper3@citrix.com> - 11.2.1-5
- Backport SLS/defunelling/IBT patches

* Mon Apr 11 2022 Edwin Török <edvin.torok@citrix.com> - 11.2.1-4
- remove devtoolset-11-libgccjit-docs dependency

* Mon Mar 14 2022 Rachel Yan <Rachel.Yan@citrix.com> - 11.2.1-3
- Re-enable testing
- Bump release and rebuild

* Thu Mar 10 2022 Rachel Yan <Rachel.Yan@citrix.com> - 11.2.1-2
- Bump release and rebuild

* Fri Oct 29 2021 Marek Polacek <polacek@redhat.com> 11.2.1-1.2
- add -Wbidirectional patch

* Mon Aug 16 2021 Marek Polacek <polacek@redhat.com> 11.2.1-1.1
- add .hidden for _ZNSt10filesystem9_Dir_base7advanceEbRSt10error_code

* Wed Jul 28 2021 Marek Polacek <polacek@redhat.com> 11.2.1-1
- update from releases/gcc-11-branch (#1986841)
  - GCC 11.2 release
  - PRs middle-end/101586, rtl-optimization/101562

* Wed Jul  7 2021 Marek Polacek <polacek@redhat.com> 11.1.1-6.1
- provide libubsan.a on ppc64 in libubsan-devel (#1977855)

* Wed Jun 23 2021 Marek Polacek <polacek@redhat.com> 11.1.1-6
- update from Fedora gcc 11.1.1-6 (#1957522)
  - PRs c++/100876, c++/100879, c++/101106, c/100619, c/100783, fortran/95501,
   fortran/95502, fortran/100283, fortran/101123, inline-asm/100785,
   libstdc++/91488, libstdc++/95833, libstdc++/100806, libstdc++/100940,
   middle-end/100250, middle-end/100307, middle-end/100574,
   middle-end/100684, middle-end/100732, middle-end/100876,
   middle-end/101062, middle-end/101167, target/99842, target/99939,
   target/100310, target/100777, target/100856, target/100871,
   target/101016

* Mon Jun 21 2021 Marek Polacek <polacek@redhat.com> 11.1.1-5
- update from Fedora gcc 11.1.1-5 (#1957522)
- default to -gdwarf-4 (#1974428)

* Wed Jun  2 2021 Marek Polacek <polacek@redhat.com> 11.1.1-3
- update from Fedora gcc 11.1.1-3 (#1957522)

* Wed May 12 2021 Marek Polacek <polacek@redhat.com> 11.1.1-2
- update from Fedora gcc 11.1.1-2
- fix up mausezahn miscompilation (PR tree-optimization/100566)
- fix build with removed linux/cyclades.h header (PR sanitizer/100379)

* Tue May 11 2021 Marek Polacek <polacek@redhat.com> 11.1.1-1
- update to GCC 11 (#1957522)

* Thu Mar 18 2021 Marek Polacek <polacek@redhat.com> 10.2.1-11.1
- update libgomp_nonshared.c with new symbols

* Tue Feb 16 2021 Marek Polacek <polacek@redhat.com> 10.2.1-11
- update from Fedora gcc 10.2.1-11
- apply gcc10-SIZE_MAX.patch

* Tue Feb 16 2021 Marek Polacek <polacek@redhat.com> 10.2.1-10.4
- package 32/libgfortran_nonshared.a (#1927579)

* Mon Feb 15 2021 Marek Polacek <polacek@redhat.com> 10.2.1-10.3
- actually use libgfortran_nonshared.a (#1927579)

* Mon Jan 25 2021 Marek Polacek <polacek@redhat.com> 10.2.1-10.2
- require make
- apply PR97524 fix (#1896092)

* Tue Jan 19 2021 Marek Polacek <polacek@redhat.com> 10.2.1-10.1
- update from Fedora gcc 10.2.1-10 (#1872051)
- drop gcc10-pr96385.patch

* Mon Aug 17 2020 Marek Polacek <polacek@redhat.com> 10.2.1-2.1
- re-enable Fortran patches (#1860413)

* Tue Aug  4 2020 Marek Polacek <polacek@redhat.com> 10.2.1-2
- update from Fedora gcc 10.2.1-2
- emit debug info for C/C++ external function declarations used in the TU
  (PR debug/96383)
- discard SHN_UNDEF global symbols from LTO debuginfo (PR lto/96385)
- strip also -flto=auto from optflags

* Sun Aug  2 2020 Marek Polacek <polacek@redhat.com> 10.2.1-1.2
- avoid stack overflow in std::vector (PR libstdc++/94540, #1859670)
- apply gcc10-libgfortran-compat-2.patch

* Sat Aug  1 2020 Marek Polacek <polacek@redhat.com> 10.2.1-1.1
- add various .hidden symbols to gcc10-libstdc++-compat.patch

* Mon Jul 27 2020 Marek Polacek <polacek@redhat.com> 10.2.1-1
- GCC 10.2 release
- add symlink to liblto_plugin.so in /usr/lib/bfd-plugins
- disable -flto in %%{optflags}, lto bootstrap will be enabled the GCC way
  later
- require MPFR Library version 3.1.0 (or later)

* Wed Jul 22 2020 Marek Polacek <polacek@redhat.com> 10.1.1-1.1
- require libasan6

* Mon Jul 13 2020 Marek Polacek <polacek@redhat.com> 10.1.1-1
- update to GCC 10.1.0 release (#1851053)

* Thu Jun  4 2020 Marek Polacek <polacek@redhat.com> 9.3.1-2.1
- bump for rebuild on ppc/s390

* Wed Apr  8 2020 Marek Polacek <polacek@redhat.com> 9.3.1-2
- update from Fedora gcc-9.3.1-2

* Tue Apr 7 2020 Marek Polacek <polacek@redhat.com> 9.3.1-1.1
- include the c++/93597 fix
- remove several .hidden symbols from gcc9-libstdc++-compat

* Wed Mar 18 2020 Marek Polacek <polacek@redhat.com> 9.3.1-1
- update from Fedora gcc-9.3.1-1 (#1812147)

* Thu Feb  6 2020 Marek Polacek <polacek@redhat.com> 9.2.1-3.8
- remove a few *codecvt_utf8* symbols from gcc9-libstdc++-compat

* Wed Jan 29 2020 Marek Polacek <polacek@redhat.com> 9.2.1-3.7
- gcc9-libstdc++-compat fix: move _ZSt19__throw_ios_failurePKc

* Wed Jan 29 2020 Marek Polacek <polacek@redhat.com> 9.2.1-3.6
- update from Fedora gcc-9.2.1-3 (#1783475)

* Thu Nov 21 2019 Marek Polacek <polacek@redhat.com> 9.1.1-2.6
- fix libgomp_nonshared.a symlink on ppc64

* Tue Nov 19 2019 Marek Polacek <polacek@redhat.com> 9.1.1-2.5
- add libgomp_nonshared.a (#1769957)

* Thu Aug 15 2019 Marek Polacek <polacek@redhat.com> 9.1.1-2.4
- require binutils >= 2.31 so that gcc supports -mpltseq

* Fri Aug  9 2019 Marek Polacek <polacek@redhat.com> 9.1.1-2.3
- fix visibility of symbols in gcc9-libstdc++-compat.patch (#1738677)

* Mon Jul 22 2019 Marek Polacek <polacek@redhat.com> 9.1.1-2.2
- small fixes for the Fortran patches (#1728355)

* Mon Jul 22 2019 Marek Polacek <polacek@redhat.com> 9.1.1-2.1
- updates from GTS 9 gcc

* Fri Jul 19 2019 Marek Polacek <polacek@redhat.com> 9.1.1-2
- fix Release

* Thu Jul 18 2019 Marek Polacek <polacek@redhat.com> 9.1.1-1.1
- fix out-of-ssa with unsupported vector types (PR rtl-optimization/90756,
  #1727979)
- apply Fortran patches (#1728355)

* Tue Jul  9 2019 Marek Polacek <polacek@redhat.com> 9.1.1-1
- new package
- fix library requires: use %{_isa} (#1697655)
