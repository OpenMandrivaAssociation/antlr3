%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global with_bootstrap 0

%global antlr_version 3.2
%global python_runtime_version 3.1.2
%global javascript_runtime_version 3.1

Summary:			ANother Tool for Language Recognition
Name:				antlr3
Version:			%{antlr_version}
Release:			14
URL:				http://www.antlr.org/
Source0:			http://www.antlr.org/download/antlr-%{antlr_version}.tar.gz
Source1:			http://www.antlr.org/download/C/libantlr3c-%{antlr_version}.tar.gz
Source2:			http://www.antlr.org/download/Python/antlr_python_runtime-%{python_runtime_version}.tar.gz
Source3:			http://www.antlr.org/download/antlr-javascript-runtime-%{javascript_runtime_version}.zip
Source5:			antlr3
%if %{with_bootstrap}
Source6:			settings.xml
Source7:			http://www.antlr.org/download/antlr-%{antlr_version}.jar
Source8:			http://mirrors.ibiblio.org/pub/mirrors/maven2/org/antlr/antlr3-maven-plugin/%{antlr_version}/antlr3-maven-plugin-%{antlr_version}.jar
%endif
# No buildnumber and findbugs:
Patch0:				antlr-pom.patch
# Python version mismatch patch, to be possibly upstreamed:
Patch1:				antlr-python-3.1.2-version.patch
License:			BSD
Group:				Development/Java
BuildRoot:			%{_tmppath}/%{name}-%{antlr_version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:		java-devel >= 0:1.6.0
BuildRequires:		jpackage-utils
BuildRequires:		antlr-maven-plugin
BuildRequires:		maven-plugin-bundle
BuildRequires:		maven-assembly-plugin
BuildRequires:		maven-shared-reporting-impl
BuildRequires:		maven-surefire-provider-junit4
BuildRequires:		junit4
BuildRequires:		tomcat6-servlet-2.5-api
BuildRequires:		tomcat6
BuildRequires:		stringtemplate >= 3.2
BuildRequires:		felix-parent
%if ! %{with_bootstrap}
BuildRequires:		antlr3-tool >= 3.2
%endif

%description
ANother Tool for Language Recognition, is a language tool
that provides a framework for constructing recognizers,
interpreters, compilers, and translators from grammatical
descriptions containing actions in a variety of target languages.

%package		tool
Group:			Development/Java
Summary:		ANother Tool for Language Recognition
BuildArch:		noarch
Requires:		jpackage-utils
Requires:		java >= 0:1.6.0
Provides:		%{name} = %{antlr_version}-%{release}
Obsoletes:		%{name} < %{antlr_version}-%{release}
Requires:		%{name}-java = %{antlr_version}-%{release}
Requires:		antlr
Requires:		stringtemplate >= 3.2

%description	tool
ANother Tool for Language Recognition, is a language tool
that provides a framework for constructing recognizers,
interpreters, compilers, and translators from grammatical
descriptions containing actions in a variety of target languages.

%package		gunit
Group:			Development/Java
Summary:		Gunit is a unit testing framework for ANTLR grammars
BuildArch:		noarch
Requires:		jpackage-utils
Requires:		java >= 0:1.6.0
Requires:               %{name}-java = %{antlr_version}-%{release}

%description	gunit
This package provides support for Gunit, a unit testing framework
for ANTLR grammars.

%package		java
Group:			Development/Java
Summary:		Java run-time support for ANTLR-generated parsers
BuildArch:		noarch
Requires:               stringtemplate
Requires:		jpackage-utils
Requires:		java >= 0:1.6.0

%description	java
Java run-time support for ANTLR-generated parsers

%package		javascript
Group:			Development/Java
Summary:		Javascript run-time support for ANTLR-generated parsers
Version:		%{javascript_runtime_version}
BuildArch:		noarch

%description	javascript
Javascript run-time support for ANTLR-generated parsers

%package		C
Group:			Development/Java
Summary:		C run-time support for ANTLR-generated parsers

%description	C
C run-time support for ANTLR-generated parsers

%package		C-devel
Group:			Development/Java
Summary:		Header files for the C bindings for ANTLR-generated parsers
Requires:		%{name}-C = %{antlr_version}-%{release}

%description	C-devel
Header files for the C bindings for ANTLR-generated parsers

%package		C-docs
Group:			Development/Java
Summary:		API documentation for the C run-time support for ANTLR-generated parsers
BuildArch:		noarch
BuildRequires:	graphviz
BuildRequires:	doxygen
Requires:		%{name}-C = %{antlr_version}-%{release}

%description	C-docs
This package contains doxygen documentation with instruction
on how to use the C target in ANTLR and complete API description of the
C run-time support for ANTLR-generated parsers.

%package		python
Group:			Development/Java
Summary:		Python run-time support for ANTLR-generated parsers
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildArch:		noarch
Version:		%{python_runtime_version}

%description	python
Python run-time support for ANTLR-generated parsers

%prep
%setup -q -n antlr-%{antlr_version} -a 1 -a 2 -a 3
%patch0 -p0 -b .pomfix
%patch1 -p0 -b .orig
%if %{with_bootstrap}
cp %{SOURCE6} settings.xml
%endif

%build
sed -i "s,\${buildNumber},`cat %{_sysconfdir}/fedora-release` `date`," tool/src/main/resources/org/antlr/antlr.properties

# remove corrupted files:
rm antlr3-maven-plugin/src/main/java/org/antlr/mojo/antlr3/._*
rm gunit-maven-plugin/src/main/java/org/antlr/mojo/antlr3/._GUnitExecuteMojo.java

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

%if %{with_bootstrap}
# we need antlr3-maven-plugin in place
sed -i -e \
"s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" \
  settings.xml
  sed -i -e \
  "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" \
  settings.xml
  sed -i -e \
  "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" \
  settings.xml
  sed -i -e \
  "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" \
  settings.xml

mkdir -p $MAVEN_REPO_LOCAL/JPP/maven2/default_poms/
mkdir -p $MAVEN_REPO_LOCAL/org.antlr/
cp antlr3-maven-plugin/pom.xml $MAVEN_REPO_LOCAL/JPP/maven2/default_poms/JPP-antlr3-maven-plugin.pom
# install prebuilt antlr and antlr3-maven-plugin into repository
# Man, this is hackish. Hold your nose.
cp %{SOURCE7} $MAVEN_REPO_LOCAL/org.antlr/antlr.jar
cp %{SOURCE8} $MAVEN_REPO_LOCAL/org.antlr/antlr3-maven-plugin.jar
%endif

# Build antlr
%if %{with_bootstrap}
mvn-jpp -s $(pwd)/settings.xml -Dmaven.repo.local=$MAVEN_REPO_LOCAL -Dmaven.test.skip=true install
%else
mvn-jpp -Dmaven.repo.local=$MAVEN_REPO_LOCAL -Dmaven.test.skip=true install
%endif

# Build the plugin
pushd antlr3-maven-plugin
mvn-jpp \
-Dmaven.repo.local=$MAVEN_REPO_LOCAL \
install javadoc:javadoc
popd

# Build the python runtime
pushd antlr_python_runtime-%{python_runtime_version}
%{__python} setup.py build
popd

# Build the C runtime
pushd libantlr3c-%{antlr_version}

mkdir m4
autoreconf -fi

%ifarch x86_64 ppc64
%configure --disable-abiflags --enable-debuginfo --enable-64bit
%endif
%ifarch %{ix86} ppc
%configure --disable-abiflags --enable-debuginfo
%endif

sed -i "s/CFLAGS = .*/CFLAGS = $RPM_OPT_FLAGS/" Makefile
make %{?_smp_mflags}
doxygen -u # update doxygen configuration file
doxygen # build doxygen documentation
popd

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_javadir},%{_mavenpomdir},%{_bindir},%{_datadir}/antlr,%{_mandir}}

# install maven POMs
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-antlr3-master.pom
install -pm 644 runtime/Java/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-antlr3-runtime.pom
install -pm 644 tool/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-antlr3.pom
install -pm 644 antlr3-maven-plugin/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-antlr3-maven-plugin.pom
install -pm 644 gunit-maven-plugin/pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-maven-gunit-plugin.pom
%add_to_maven_depmap org.antlr antlr-master %{antlr_version} JPP antlr3-master
%add_to_maven_depmap org.antlr antlr-runtime %{antlr_version} JPP antlr3-runtime
%add_to_maven_depmap org.antlr antlr %{antlr_version} JPP antlr3
%add_to_maven_depmap org.antlr antlr3-maven-plugin %{antlr_version} JPP antlr3-maven-plugin
%add_to_maven_depmap org.antlr maven-gunit-plugin %{antlr_version} JPP maven-gunit-plugin

# install jars
install -m 644 runtime/Java/target/antlr-runtime-%{antlr_version}.jar \
tool/target/antlr-%{antlr_version}.jar antlr3-maven-plugin/target/antlr3-maven-plugin-%{antlr_version}.jar \
gunit/target/gunit-%{antlr_version}.jar gunit-maven-plugin/target/maven-gunit-plugin-%{antlr_version}.jar \
$RPM_BUILD_ROOT%{_datadir}/java/
pushd $RPM_BUILD_ROOT%{_datadir}/java
ln -s antlr-%{antlr_version}.jar antlr3.jar
ln -s antlr3-maven-plugin-%{antlr_version}.jar antlr3-maven-plugin.jar
ln -s antlr-runtime-%{antlr_version}.jar antlr3-runtime.jar
popd

# install wrapper script
install -m 755 %{SOURCE5} $RPM_BUILD_ROOT%{_bindir}/antlr3

# install python runtime
pushd antlr_python_runtime-%{python_runtime_version}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd

# install C runtime
pushd libantlr3c-%{antlr_version}
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/libantlr3c.{a,la}
pushd api/man/man3
for file in `ls -1 * | grep -vi "^antlr3"`; do
	mv $file antlr3-$file
done
gzip *
popd
mv api/man/man3 $RPM_BUILD_ROOT%{_mandir}/
rmdir api/man
popd

# install javascript runtime
pushd antlr-javascript-runtime-%{javascript_runtime_version}
install -pm 644 *.js $RPM_BUILD_ROOT%{_datadir}/antlr/
popd

%post java
%update_maven_depmap

%postun java
%update_maven_depmap

%post C -p /sbin/ldconfig

%postun C -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files tool
%defattr(-,root,root,-)
%doc tool/{README.txt,LICENSE.txt,CHANGES.txt}
%{_javadir}/antlr3.jar
%{_javadir}/antlr3-maven*.jar
%{_javadir}/antlr-%{antlr_version}.jar
%{_bindir}/antlr3

%files python
%defattr(0644,root,root,-)
%{python_sitelib}/antlr3/*
%{python_sitelib}/antlr_python_runtime-*

%files C
%defattr(-,root,root,-)
%{_libdir}/libantlr3c.so

%files C-devel
%defattr(-,root,root,-)
%{_includedir}/antlr3*
%{_mandir}/man3/*

%files C-docs
%defattr(-,root,root,-)
%doc libantlr3c-%{antlr_version}/api/

%files java
%defattr(-,root,root,-)
%{_javadir}/*runtime*.jar
%{_mavenpomdir}/*.pom
%config %{_mavendepmapfragdir}/antlr3

%files javascript
%defattr(-,root,root,-)
%{_datadir}/antlr/

%files gunit
%defattr(-,root,root,-)
%{_javadir}/*gunit*.jar

