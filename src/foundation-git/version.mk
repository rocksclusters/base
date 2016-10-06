NAME = foundation-git
VERSION = 2.9.2
RELEASE = 2
RPM.EXTRAS=%define __os_install_post /usr/lib/rpm/redhat/brp-compress; /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip}; /usr/lib/rpm/redhat/brp-python-hardlink;%{!?__jar_repack:/usr/lib/rpm/redhat/brp-java-repack-jars}

RPM.FILES="/opt/rocks/bin/*\\n/opt/rocks/etc/gitconfig\\n/opt/rocks/lib64/perl5/auto/Git/.packlist\\n/opt/rocks/lib64/perl5/perllocal.pod\\n/opt/rocks/libexec/git-core\\n/opt/rocks/share/git-core\\n/opt/rocks/share/git-gui\\n/opt/rocks/share/gitk\\n/opt/rocks/share/gitweb\\n/opt/rocks/share/locale/*/LC_MESSAGES/git*\\n/opt/rocks/share/man/man[1357]/*\\n/opt/rocks/share/perl5/Git*"
