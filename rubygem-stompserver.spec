%define	oname	stompserver

Summary:	A basic message queue processing server
Name:		rubygem-%{oname}
Version:	0.9.9
Release:	%mkrel 2
License:	MIT
Group:		Development/Ruby
URL:		http://%{oname}.rubyforge.org/
Source0:	http://gems.rubyforge.org/gems/%{oname}-%{version}.gem
Source1:	%{oname}.init
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	ruby-RubyGems
BuildArch:	noarch

%description
Stomp messaging server with file/dbm/memory/activerecord based FIFO queues,
queue monitoring, and basic authentication.

%prep

%build

%install
rm -rf %{buildroot}
gem install -E -n %{buildroot}%{_bindir} --local --install-dir %{buildroot}/%{ruby_gemdir} --force %{SOURCE0}

rm -rf %{buildroot}%{ruby_gemdir}/{cache,gems/%{oname}-%{version}/ext}

install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/%{oname}
install -m644 %{buildroot}%{ruby_gemdir}/gems/%{oname}-%{version}/config/%{oname}.conf -D %{buildroot}%{_sysconfdir}/%{oname}.conf
sed	-e 's#:daemon:.*#:daemon: true#g' \
	-e 's#:working_dir:.*#:working_dir: %{_localstatedir}/lib/%{oname}#g' \
	-e 's#:user:.*#:user: %{oname}#g' \
	-e 's#:group:.*#:group: %{oname}#g' \
	-i %{buildroot}%{_sysconfdir}/%{oname}.conf
echo ':logdir: ../../log/stompserver' >> %{buildroot}%{_sysconfdir}/%{oname}.conf
echo ':pidfile: ../../run/stompserver/stompserver.pid' >> %{buildroot}%{_sysconfdir}/%{oname}.conf

install -m644 %{buildroot}%{ruby_gemdir}/gems/%{oname}-%{version}/etc/passwd.example -D %{buildroot}%{_localstatedir}/lib/%{oname}/etc/.passwd
sed -e 's/testuser:testpass/#testuser:testpass/g' -i %{buildroot}%{_localstatedir}/lib/%{oname}/etc/.passwd

install -d %{buildroot}%{_localstatedir}/lib/%{oname}/.queue
install -d %{buildroot}%{_var}/{log,run}/%{oname}

%pre
%_pre_useradd %{oname} %{_localstatedir}/lib/%{oname} /sbin/nologin

%post
%{_post_service %{oname}}

%preun
%{_preun_service %{oname}}

%postun
%_postun_userdel %{oname}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{ruby_gemdir}/doc/%{oname}-%{version}
%{ruby_gemdir}/gems/%{oname}-%{version}
%{ruby_gemdir}/specifications/%{oname}-%{version}.gemspec
%{_bindir}/%{oname}
%{_initrddir}/%{oname}
%config(noreplace) %{_sysconfdir}/%{oname}.conf
%attr(700,%{oname},%{oname}) %dir %{_localstatedir}/lib/%{oname}
%attr(700,%{oname},%{oname}) %dir %{_localstatedir}/lib/%{oname}/etc
%config(noreplace) %attr(640,root,stompserver) %{_localstatedir}/lib/%{oname}/etc/.passwd
%attr(700,%{oname},%{oname}) %dir %{_localstatedir}/lib/%{oname}/.queue
%attr(700,%{oname},%{oname}) %dir %{_localstatedir}/log/%{oname}
%attr(700,%{oname},%{oname}) %dir %{_localstatedir}/run/%{oname}
