Summary: phpMyAdmin for Nethserver
Name: nethserver-phpmyadmin
Version: 1.2.5
Release: 2%{?dist}
License: GPL
Source: %{name}-%{version}.tar.gz
URL: http://dev.nethserver.org/projects/nethforge/wiki/%{name}
BuildArch: noarch

Requires: phpMyAdmin >= 4.0.10.4

Requires: nethserver-mysql
Requires: nethserver-httpd

BuildRequires: perl
BuildRequires: nethserver-devtools 

%description
Implementation of phpMyAdmin for Nethserver
Access with admin username/password via: https://yourdomain/phpmyadmin.



%prep
%setup

%build
mkdir  -p root/var/lib/phpMyAdmin/tmp
perl createlinks
sed -i 's/_RELEASE_/%{version}/' %{name}.json
 
%install
/bin/rm -rf $RPM_BUILD_ROOT
(cd root   ; /usr/bin/find . -depth -print | /bin/cpio -dump $RPM_BUILD_ROOT)

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
cp -a manifest.json %{buildroot}/usr/share/cockpit/%{name}/
cp -a logo.png %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/

%{genfilelist} %{buildroot}   \
     --dir /var/lib/phpMyAdmin/tmp 'attr(0750,apache,apache)' \
   $RPM_BUILD_ROOT > %{name}-%{version}-filelist
echo "%doc phpmyadmin.sql" >> %{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc COPYING
%dir %{_nseventsdir}/%{name}-update
%attr(0440,root,root) /etc/sudoers.d/50_nsapi_nethserver_phpmyadmin

%clean 
rm -rf $RPM_BUILD_ROOT

%postun
if [ $1 == 0 ] ; then
  /usr/bin/rm -f /etc/httpd/conf.d/phpMyAdmin.conf
  /usr/bin/systemctl reload httpd
fi

%changelog
* Sun Jul 05 2020 stephane de Labrusse <stephdl@de-labrusse.fr> 1.2.5
- Remove http templates after rpm removal

* Thu Mar 05 2020  stephane de Labrusse <stephdl@de-labrusse.fr> 1.2.4-1.ns7
- Fix bad sudoers permission

* Mon Oct 14 2019 Stephane de Labrusse <stephdl@de-labrusse.fr> 1.2.3-1.ns7
- cockpit. added to legacy apps

* Sun Sep 10 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> 1.2.2-1.ns7
- Restart httpd service on trusted-network

* Wed Mar 29 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.2.1-2.ns7
- Template expansion on trusted-network

* Sun Mar 12 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.2.0-2.ns7
- GPL license

* Thu Sep 29 2016 stephane de labrusse <stephdl@de-labrusse.fr> - 1.2.0-1.ns7
- NS7 version
- Only the cooky session is used now, because the admin user does't exist anymore

* Wed Nov 05 2014 stephane de labrusse <stephdl@de-labrusse.fr> - 1.1.0-1.ns6
- updated to phpMyAdmin-4.0.10.4-1.el6.noarch - Feature #2934 [NethForge]
- added a tmp folder other that the /tmp
- added some db values to adjust php limits (PostMaxSize,UploadMaxSize,MemoryLimit)
- added a phpmyadmin.sql db to save settings in db
- new cool features (bookmarktable,relation,userconfig,table_info,column_info,history,
- recent,table_uiprefs,tracking,table_coords,pdf_pages,designer_coords)
- the http://url/setup page is now forbidden by apache
- a db 'status' exists now to disable simply phpmyadmin in httpd.conf
- removed the openbasedir of /tmp to /var/lib/phpMyAdmin/tmp
- add memory value up to 500M
- add php upload/post up to 100M
- add session.use_trans_sid 0
- directory 'scripts' removed of httpd templates
- VersionCheck is off now
- pointers are created  in the Dashboard Application menu to use directly phpmyadmin
 
* Mon Aug 18 2014 Davide Principi <davide.principi@nethesis.it> - 1.0.0-1.ns6
- First nethforge release. Refs #2754

* Sun May 25 2014 stephane de labrusse <stephdl@de-labrusse.fr> 3.5.8.2
- first release to nethserver.

* Mon May 19 2014 stephane de labrusse <stephdl@de-labrusse.fr> 3.5.8.2
-first release to sme9
 
* Sat Jun 22 2013 JP Pialasse <tests@pialasse.com> 3.5.2.2-6
- Obsolete multiuser [SME: 7685]

* Tue Jun 18 2013 JP Pialasse <tests@pialasse.com> 3.5.2.2-5
- added full 3.5 configuration to avoid errors [SME: 7153] [SME: 7194]
- incorporated multiuser contrib in this package [SME: 7628 7627 ]
- increased security [SME: 5007]
- configext.patch
- release bump to 4 to fix spec file
- patch1 to fix config.inc.php syntax error

* Thu Aug 06 2012 JP Pialasse  aka Unnilennium  <tests@pialasse.com> 3.5.2.2-2
- first version for SME 8
- adaptation for phpMyAdmin3 3.5.2.2

* Thu May 15 2008 Jonathan Martens <smeserver-contribs@snetram.nl> 2.11.1.2-3
- Protect sensible data and prevent access error by setting 
  proper permissions to config.inc.php template [SME: 4343]

* Wed May 14 2008 Jonathan Martens <smeserver-contribs@snetram.nl>
- Converted RPM to be an integrational RPM [SME: 4298]:
- Convert and move templates to RPMForge (Dag) install location [SME: 4339]
- Automatically expand phpmyadmin configuation file (config.php.inc) [SME: 4340]
- Remove PHPMyAdmin core [SME: 4341]

* Mon Apr 21 2008 Shad L. Lords <slords@mail.com>
- Prep for import into buildsys
- Clean up spec

* Fri Oct 19 2007 Darrell May <dmay@myezserver.com>
- accounts and configuration db phpmyadmin defaults added
- default access restricted to private (private|public)
- phpMyAdmin 2.11.1.2
- [ 2.11.1.2-0]
* Fri Mar 09 2007 Darrell May <dmay@myezserver.com>
- phpMyAdmin 2.10.0.2
- [ 2.10.0.2-0]
* Thu Oct 12 2006 Darrell May <dmay@myezserver.com>
- phpMyAdmin 2.9.0.2
- [ 2.9.0.2-0]
* Thu Dec 15 2005 Darrell May <dmay@myezserver.com>
- phpMyAdmin 2.6.4-pl4
- [ 2.6.4-pl4]
* Fri Apr 22 2005 Darrell May <dmay@myezserver.com>
- added support for SME 7.x
- [ 2.6.2-2]
* Mon Apr 18 2005 Darrell May <dmay@myezserver.com>
- Release 2.6.2 of phpMyAdmin
- change rpm name to smeserver-phpmyadmin
- change install dir to /opt/phpmyadmin
- [ 2.6.2-1]
