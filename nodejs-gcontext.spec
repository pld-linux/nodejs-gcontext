%define		pkg	gcontext
Summary:	Provide API to use GMainContext in Node.js
Name:		nodejs-%{pkg}
Version:	0.0.2
Release:	2
License:	MIT
Group:		Development/Libraries
Source0:	http://registry.npmjs.org/gcontext/-/%{pkg}-%{version}.tgz
# Source0-md5:	1f0aae37d577a56f46e82ab9f3b1fa67
Patch0:		load-path.patch
URL:		https://github.com/cfsghost/node-gcontext
BuildRequires:	nodejs-gyp
BuildRequires:	rpmbuild(macros) >= 1.657
BuildRequires:	sed >= 4.0
Requires:	nodejs >= 0.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# redefine for arch specific
%define		nodejs_libdir	%{_libdir}/node

%description
node-gcontext is an event loop integration between libuv and GLib, to
make that GLib event loop works with Node.js event engine.

It makes many libraries(GTK+, DBus, Clutter...etc) which are using
GLib event loop to be able to work on Node.js.

%prep
%setup -qc
mv package/* .
%patch -P0 -p1

%{__rm} -r build

%build
node-gyp configure --nodedir=/usr/src/nodejs --gyp=/usr/bin/gyp
node-gyp build --jobs=%{?__jobs} --verbose

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
cp -pr package.json lib $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}
install -p build/Release/%{pkg}.node $RPM_BUILD_ROOT%{nodejs_libdir}/%{pkg}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{nodejs_libdir}/%{pkg}
%{nodejs_libdir}/%{pkg}/package.json
%{nodejs_libdir}/%{pkg}/lib
%attr(755,root,root) %{nodejs_libdir}/%{pkg}/%{pkg}.node
