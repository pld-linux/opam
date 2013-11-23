# TODO:
# - handle building without external deps. possible?

# Conditional build:
%bcond_without	doc		# do not build doc

Summary:	A source-based package manager for OCaml
Name:		opam
Version:	1.1.0
Release:	1
License:	GPL
Group:		Applications
Source0:	https://github.com/ocaml/opam/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8a6d9eae64fa1f88cddb5c96d8d96a80
Source1:	https://gforge.inria.fr/frs/download.php/31910/cudf-0.6.3.tar.gz
# Source1-md5:	40c4e2c50ea96d0c9e565db16d20639a
Source2:	http://ocaml-extlib.googlecode.com/files/extlib-1.5.3.tar.gz
# Source2-md5:	3de5f4e0a95fda7b2f3819c4a655b17c
Source3:	https://github.com/ocaml/ocaml-re/archive/ocaml-re-1.2.0.tar.gz
# Source3-md5:	5cbfc137683ef2b0e91f931577f2e673
Source4:	http://pkgs.fedoraproject.org/repo/pkgs/ocaml-ocamlgraph/ocamlgraph-1.8.1.tar.gz/5aa256e9587a6d264d189418230af698/ocamlgraph-1.8.1.tar.gz
# Source4-md5:	5aa256e9587a6d264d189418230af698
Source5:	https://gforge.inria.fr/frs/download.php/31595/dose3-3.1.2.tar.gz
# Source5-md5:	e98ff720fcc3873def46c85c6a980a1b
Source6:	http://erratique.ch/software/cmdliner/releases/cmdliner-0.9.3.tbz
# Source6-md5:	d63dd3b03966d65fc242246859c831c7
URL:		http://opam.ocamlpro.com/
BuildRequires:	hevea
BuildRequires:	ocaml
BuildRequires:	ocaml-camlp4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OPAM stands for OCaml PAckage Manager. It aims to suit to a vast
number of users and use cases, and has unique features:

 - Powerful handling of dependencies: versions constraints, optional
   dependencies, conflicts, etc.
 - Multiple repositories backends: HTTP, rsync, git
 - Ease to create packages and repositories
 - Ability to switch between different compiler versions

Typically, OPAM will probably make your life easier if you recognize
yourself in at least one of these profiles:

 - You use multiple versions of the OCaml compiler, or you hack the
   compiler yourself and needs to frequently switch between compiler
   versions.
 - You use or develop software that needs a specific and/or modified
   version of the OCaml compiler to be installed.
 - You use or develop software that depends on a specific version of an
   OCaml library, or you just want to install a specific version of a
   package, not just the latest one.
 - You want to create your own packages yourself, put them on your own
   repository, with minimal effort.

%package    doc
Summary:	Documentation files for %{name}
Group:		Development
Requires:	%{name} = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
The %{name}-doc package contains documentation for using %{name}.

%prep
%setup -q

ln -s %{SOURCE1} src_ext
ln -s %{SOURCE2} src_ext
ln -s %{SOURCE3} src_ext
ln -s %{SOURCE4} src_ext
ln -s %{SOURCE5} src_ext
ln -s %{SOURCE6} src_ext

%build
%configure
%{__make} all opt -j1

%if %{with doc}
# make doc
cd doc/dev-manual
%{__make} html
%{__make} clean
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE CHANGES AUTHORS CONTRIBUTING
%attr(755,root,root) %{_bindir}/opam
%attr(755,root,root) %{_bindir}/opam-admin
%{_mandir}/man1/opam.1*
%{_mandir}/man1/opam-*.1*

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/
%doc tests/
%doc jenkins/
%doc shell/
%endif
