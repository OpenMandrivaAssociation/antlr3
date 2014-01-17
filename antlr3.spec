
%undefine _compress
%undefine _extension
%global _duplicate_files_terminate_build 0
%global _files_listed_twice_terminate_build 0
%global _unpackaged_files_terminate_build 0
%global _nonzero_exit_pkgcheck_terminate_build 0
%global _use_internal_dependency_generator 0
%global __find_requires /bin/sed -e 's/.*//'
%global __find_provides /bin/sed -e 's/.*//'

Name:		antlr3-java
Version:	3.4
Release:	15.0
License:	GPLv3+
Source0:	antlr3-java-3.4-15.0-omv2014.0.noarch.rpm
Source1:	antlr3-javascript-3.1-15.0-omv2014.0.noarch.rpm
Source2:	antlr3-tool-3.4-15.0-omv2014.0.noarch.rpm

URL:		https://abf.rosalinux.ru/openmandriva/antlr3-java
BuildArch:	noarch
Summary:	antlr3-java bootstrap version
Requires:	javapackages-bootstrap
Requires:	java >= 1:1.6.0
Requires:	jpackage-utils
Requires:	stringtemplate
Requires:	stringtemplate4
Provides:	antlr3-java = 3.4-15.0:2014.0
Provides:	mvn(org.antlr:antlr) = 3.4
Provides:	mvn(org.antlr:antlr-master) = 3.4
Provides:	mvn(org.antlr:antlr-master:pom:) = 3.4
Provides:	mvn(org.antlr:antlr-runtime) = 3.4
Provides:	mvn(org.antlr:antlr3-maven-plugin) = 3.4
Provides:	osgi(org.antlr.runtime) = 3.2.0

%description
antlr3-java bootstrap version.

%files
/usr/share/doc/antlr3-java
/usr/share/doc/antlr3-java/LICENSE.txt
/usr/share/java/antlr3-runtime.jar
/usr/share/maven-fragments/antlr3
/usr/share/maven-poms/JPP-antlr3-master.pom
/usr/share/maven-poms/JPP-antlr3-maven-plugin.pom
/usr/share/maven-poms/JPP-antlr3-runtime.pom
/usr/share/maven-poms/JPP-antlr3.pom
/usr/share/maven-poms/JPP-maven-gunit-plugin.pom

#------------------------------------------------------------------------
%package	-n antlr3-javascript
Version:	3.1
Release:	15.0
Summary:	antlr3-javascript bootstrap version
Requires:	javapackages-bootstrap
Provides:	antlr3-javascript = 3.1-15.0:2014.0

%description	-n antlr3-javascript
antlr3-javascript bootstrap version.

%files		-n antlr3-javascript
/usr/share/antlr
/usr/share/antlr/antlr3-all-min.js
/usr/share/antlr/antlr3-all.js
/usr/share/antlr/antlr3-cli-min.js
/usr/share/antlr/antlr3-cli.js
/usr/share/doc/antlr3-javascript
/usr/share/doc/antlr3-javascript/LICENSE.txt

#------------------------------------------------------------------------
%package	-n antlr3-tool
Version:	3.4
Release:	15.0
Summary:	antlr3-tool bootstrap version
Requires:	javapackages-bootstrap
Requires:	antlr3-java = 3.4-15.0
Requires:	java >= 1:1.6.0
Requires:	jpackage-utils
Requires:	stringtemplate4
Provides:	antlr3 = 3.4-15.0
Provides:	antlr3-tool = 3.4-15.0:2014.0
Obsoletes:	antlr3 < 3.4-15.0

%description	-n antlr3-tool
antlr3-tool bootstrap version.

%files		-n antlr3-tool
/usr/bin/antlr3
/usr/share/doc/antlr3-tool
/usr/share/doc/antlr3-tool/CHANGES.txt
/usr/share/doc/antlr3-tool/LICENSE.txt
/usr/share/doc/antlr3-tool/README.txt
/usr/share/java/antlr3-maven-plugin.jar
/usr/share/java/antlr3.jar

#------------------------------------------------------------------------
%prep

%build

%install
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -id
rpm2cpio %{SOURCE1} | cpio -id
rpm2cpio %{SOURCE2} | cpio -id
