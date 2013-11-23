#
# Conditional build:
%bcond_without	doc		# do not build doc

Summary:	A source-based package manager for OCaml
Name:		opam
Version:	1.1.0
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://www.ocamlpro.com/pub/%{name}-full-%{version}.tar.gz
# Source0-md5:	272aa408dcc77464ebf884aa44129b46
URL:		http://opam.ocamlpro.com/
BuildRequires:	ocaml-camlp4
BuildRequires:	hevea
BuildRequires:	ocaml
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
%setup -q -n %{name}-full-%{version}

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
