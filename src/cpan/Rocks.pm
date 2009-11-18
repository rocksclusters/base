#
# This file is part of CPANPLUS::Dist::RPM
#
# This program is free software; you can redistribute it and/or modify
# it under the same terms as Perl itself.
#

package CPANPLUS::Dist::Rocks;

use strict;
use warnings;

use base 'CPANPLUS::Dist::Base';

use English '-no_match_vars';

# imports error(), msg()
use CPANPLUS::Error; 

use Cwd;
use Data::Section -setup;
use File::Basename;
use File::Copy       qw{ copy };
use File::Find::Rule;
use IPC::Cmd         qw{ run can_run };
use List::Util       qw{ first };
use List::MoreUtils  qw{ uniq };
use Path::Class;
use Pod::POM;
use Pod::POM::View::Text;
use POSIX           qw{ strftime };
use Readonly;
use Software::LicenseUtils;
use Text::Autoformat;
use Template;

our $VERSION = '0.0.8';

# debugging
#use Smart::Comments '###', '####';

Readonly my $RPMDIR => do { chomp(my $d=qx[ rpm --eval %_topdir ]); $d; };
Readonly my $PACKAGER => 
    do { my $d = `rpm --eval '%{packager}'`; chomp $d; $d };
Readonly my $DEFAULT_LICENSE => 'CHECK(GPL+ or Artistic)';
Readonly my $DIR => cwd;

#--
# class methods

#
# my $bool = CPANPLUS::Dist::RPM->format_available;
#
# Return a boolean indicating whether or not you can use this package to
# create and install modules in your environment.
#
sub format_available {

    my $flag;

    # check prereqs
    for my $prog ( qw{ rpm rpmbuild gcc } ) {

        next if can_run($prog);
        error "'$prog' is a required program to build RPM packages";
        $flag++;
    }

    return not $flag;
}

#--
# public methods

#
# my $bool = $fedora->init;
#
# Sets up the C<CPANPLUS::Dist::RPM> object for use, and return true if
# everything went fine.
#
sub init {
    my $self = shift @_;

    # e.g...
    # distname: Foo-Bar
    # distvers: 1.23
    # extra_files: qw[ /bin/foo /usr/bin/bar ] 
    # rpmname:     perl-Foo-Bar
    # rpmpath:     $RPMDIR/RPMS/noarch/perl-Foo-Bar-1.23-1mdv2008.0.noarch.rpm
    # rpmvers:     1
    # rpmdir:      $DIR
    # srpmpath:    $RPMDIR/SRPMS/perl-Foo-Bar-1.23-1mdv2008.0.src.rpm
    # specpath:    $RPMDIR/SPECS/perl-Foo-Bar.spec
    # is_noarch:   true if pure-perl
    # license:     try to figure out the actual license
    # summary:     one-liner summary
    # description: a paragraph summary or so

    $self->status->mk_accessors(
        qw{ 
            distname distvers extra_files rpmname rpmpath rpmvers 
            rpmdir srpmpath specpath is_noarch license summary 
            description packager license_comment
          }
    );

    return 1;
}

sub prepare {
    my $self = shift @_;
    my %opts = $self->_parse_args(@_);

    my $status = $self->status;               # Private hash
    my $module = $self->parent;               # CPANPLUS::Module
    my $intern = $module->parent;             # CPANPLUS::Internals
    my $conf   = $intern->configure_object;   # CPANPLUS::Configure
    my $distmm = $module->status->dist_cpan;  # CPANPLUS::Dist::MM

    # Dry-run with makemaker: find build prereqs.
    msg( "dry-run prepare with makemaker..." );
    $self->SUPER::prepare(@_);

    # populate our status object
    $self->_prepare_status;

    # check whether package has been built
    if ($self->_package_exists) {
        my $modname = $self->parent->module;
        my $rpmname = $status->rpmname;

        msg( "'$rpmname' is already installed (for $modname)" );

        if (!$opts{force}) {
            msg( "won't re-spec package since --force isn't in use" );
            # c::d::rpm store
            #$status->rpmpath($pkg); # store the path of rpm
            # cpanplus api
            $status->prepared(1);
            $status->created(1);
            $status->installed(1); # right?
            $status->dist($rpmname);
            return $rpmname;
            # XXX check if it works
        }

        msg( '--force in use, re-specing anyway' );
        # FIXME: bump rpm release
    } 
    else {
        msg( "writing specfile for '$self->distname'..." );
    }

    # create the specfile
    $self->_prepare_spec;

    # copy package.
    my $tarball = $status->rpmdir . '/' . basename $module->status->fetch;
    copy $module->status->fetch, $tarball;

    msg "specfile for '" . $status->distname . "' written";
    # return success
    return $status->prepared(1);
}


sub create {
    my $self = shift @_;
    my %opts = $self->_parse_args(@_);

    my $status = $self->status;               # private hash
    my $module = $self->parent;               # CPANPLUS::Module
    my $intern = $module->parent;             # CPANPLUS::Internals
    my $conf   = $intern->configure_object;   # CPANPLUS::Configure
    my $distmm = $module->status->dist_cpan;  # CPANPLUS::Dist::MM

    # check if we need to rebuild package.
    if ($status->created && defined $status->dist) {
        if ( not $opts{force} ) {
            msg "won't re-build package since --force isn't in use";
            return $status->dist;
        }
        msg '--force in use, re-building anyway';
    }

    RPMBUILD: {
        # dry-run with makemaker: handle prereqs.
        msg 'dry-run build with makemaker...';
        #$self->SUPER::create(%args);
        $self->SUPER::create(@_);

        my $spec     = $status->specpath;
        my $distname = $status->distname;
        my $rpmname  = $status->rpmname;
        my $dir      = $status->rpmdir;

        msg "Building '$distname' from specfile $spec...";

        # run rpmbuild
        my ($success, $buffer) = $self->_build_rpm(@_);

        # check if the dry-run finished correctly
        if ($success) {

            # FIXME we may have multiple RPMs.
            my ($rpm)  = (sort glob "$dir/*/$rpmname-*.rpm")[-1];
            my ($srpm) = (sort glob "$dir/$rpmname-*.src.rpm")[-1];
            msg( "RPM created successfully: $rpm" );
            msg( "SRPM available: $srpm" );
            # c::d::rpm store
            $status->rpmpath($rpm);
            $status->srpmpath($srpm);
            # cpanplus api
            $status->created(1);
            $status->dist($rpm);
            last RPMBUILD;
        }

        $success = $self->_handle_rpmbuild_error(
            success => $success, 
            buffer  => $buffer,
            @_
        );

        if (not $success) {
            
            # unknown error, aborting.
            error "Failed to create RPM package for '$distname': $buffer";
            $status->created(0);
            last RPMBUILD;
        }

        redo RPMBUILD;
    }

    return $status->created;
}

sub install {
    my $self = shift @_;
    my %opts = $self->_parse_args(@_);

    #my $rpm = $self->status->rpm;
    my $rpmcmd = 'rpm -Uvh ';
    if ( $opts{force} ){
	$rpmcmd = $rpmcmd . '--force --nodeps ';
	}
    $rpmcmd = $rpmcmd . $self->status->rpmpath;

    if ($EUID != 0) {

        msg 'trying to invoke rpm via sudo';

        $rpmcmd = "sudo $rpmcmd";
    }
    
    my $buffer;
    my $success = run(
        command => $rpmcmd,
        verbose => $opts{verbose},
        buffer  => \$buffer,
    );

    if (not $success) {

        error "error installing! ($success)";
        printf STDERR $buffer;
        #die;
        return $self->status->installed(0);
    }

    return $self->status->installed(1);
}

##################################################################
# prepare (private methods)

sub _prepare_spec {
    my $self = shift @_;
    
    # Prepare our template
    #my $tmpl = Template->new({ EVAL_PERL => 1 });
    my $tmpl = Template->new;
    
    # Process template into spec
    $tmpl->process(
        $self->section_data('spec'),
        {
            status    => $self->status,
            module    => $self->parent,
            buildreqs => $self->_buildreqs,
            date      => strftime("%a %b %d %Y", localtime),
            packager  => $PACKAGER,
            docfiles  => join(' ', @{ $self->_docfiles }),

            packagervers => $VERSION,
        },
        $self->status->specpath,
    );
}

sub _package_exists {
    my $self    = shift @_;
    my $rpmname = shift @_ || $self->status->rpmname;

    #my $pkg = ( sort glob "$RPMDIR/RPMS/*/$name-$vers-*.rpm" )[-1];
    #return $pkg;

    my $output = `rpm -q $rpmname`;
    
    return $output =~ /is not installed/ ? 0 : 1;
}

sub _prepare_status {
    my $self = shift @_;

    my $status = $self->status;               # Private hash
    my $module = $self->parent;               # CPANPLUS::Module
    my $intern = $module->parent;             # CPANPLUS::Internals
    my $conf   = $intern->configure_object;   # CPANPLUS::Configure
    my $distmm = $module->status->dist_cpan;  # CPANPLUS::Dist::MM

    # Compute & store package information
    $status->distname($module->package_name);
    $status->rpmdir($DIR.'/'.$status->distname);
    $status->rpmname($self->_mk_pkg_name);
    $status->distvers($module->package_version);
    $status->summary($self->_module_summary($module));
    $status->description(autoformat $self->_module_description($module));
    $status->rpmvers('0');    # FIXME probably need make this malleable
    $status->is_noarch($self->_is_noarch);
    $status->specpath($status->rpmdir . '/' . $status->rpmname . '.spec');

    # _module_license sets both license and license_comment
    #$status->license($self->_module_license($module));
    $self->_module_license($module);

    return;
}

##################################################################
# create (private methods)

sub _build_rpm {
    my $self = shift @_;
    my %opts = $self->_parse_args(@_);

    my ($buffer, $success);
    my $dir = $self->status->rpmdir;

    #local $ENV{LC_ALL} = 'C'; # FIXME um, why?

    $success = run(
        #command => "rpmbuild -ba --quiet $spec",
        command => 'rpmbuild -ba '
            . qq{--define '_sourcedir $dir' }
            . qq{--define '_builddir $dir'  }
            . qq{--define '_srcrpmdir $dir' }
            . qq{--define '_rpmdir $dir'    }
            . $self->status->specpath,
        verbose => $opts{verbose},
        buffer  => \$buffer,
    );

    return ($success, $buffer);
}

sub _handle_rpmbuild_error {
    my $self = shift @_;
    my %opts = $self->_parse_args(@_);

    # error: Failed build dependencies:
    #    perl(App::Cmd) is needed by perl-MooseX-App-Cmd-0.04-0.1.fc9.noarch

    my $builddep = qr/^error: Failed build dependencies/;
    
    # error: Installed (but unpackaged) file(s) found:
    #   /usr/bin/pm_which
    #   /usr/share/man/man1/pm_which.1.gz

    # often from tests:  cannot open display

    my $unpackaged_re =
        qr/^\s+Installed .but unpackaged. file.s. found:\n(.*)\z/ms;
        #qr/Installed .but unpackaged. file.s. found/;

    if ($opts{buffer} =~ $unpackaged_re ) {

        # additional files need to be packaged
        msg 'Installed but unpackaged files found, fixing spec file';

        # massage into a filelist we want...
        my $files = $1;
        $files =~ s/^\s+//mg; # remove spaces
        my @files = split /\n/, $files;

        # FIXME this isn't going to work where _docdir != /usr/bin
        @files = 
            map { $_ =~ s!^/opt/rocks/bin!%{_bindir}!;       $_ }
            map { $_ =~ s!^/opt/rocks/share/man!%{_mandir}!; $_ }
            @files
            ;

        ### @files
        $self->status->extra_files(\@files);
        $self->prepare(%opts, force => 1);
        return 1;
    }
    elsif ($opts{buffer} =~ $builddep) {

        error "unsatisfied builddeps!\n\n$opts{buffer}\n";
    }

    return 0;
}

sub _parse_args {
    my $self = shift @_;
    my %args = @_;
    my $conf = $self->parent->parent->configure_object;

    # parse args.
    my %opts = (
        force   => $conf->get_conf('force'),  # force rebuild
        perl    => $^X,
        verbose => $conf->get_conf('verbose'),
        %args,
    );

    return %args;
}

# quickly determine if the module is pure-perl (noarch) or not
sub _is_noarch {
    my $self = shift @_;
 
    my @files = @{ $self->parent->status->files };
    return do { first { /\.(c|xs)$/i } @files } ? 0 : 1;
}

# generate our hashref of buildreqs
sub _buildreqs {
    my $self = shift @_;

    # Handle build/test/requires
    my $buildreqs = $self->parent->status->prereqs;

    # Module::Build::Compat should not be a build
    # requirement for anything. It's already present
    # in perl-core, and should not be rebuilt for 
    # every bloody package that requires it
    #$buildreqs->{'Module::Build::Compat'} = 0
    #    if $self->_is_module_build_compat;

    return $buildreqs;
}

sub _docfiles {
    my $self = shift @_;

    # FIXME this is really not complete enough    
    my @docfiles =
        grep { /(README|Change(s|log)|LICENSE|Copyright)$/i }
        map { basename $_ }
        @{ $self->parent->status->files }
        ;

    return \@docfiles;
}

sub _is_module_build_compat {
    my $self   = shift @_;
    my $module = shift @_ || $self->parent;

    my $makefile = file $module->_status->extract . '/Makefile.PL';
    my $content  = $makefile->slurp;

    return $content =~ /Module::Build::Compat/;
}

sub _mk_pkg_name {
    my ($self, $dist) = @_;

    # use our our dist name if we're not passed one.
    $dist = $self->status->distname if not defined $dist;

    return "foundation-perl-$dist";
}

# determine the module license. 
#
# FIXME! Look for 'LICENSE' / 'Copying' / etc files

# right now we use the Fedora shortnames, for lack of anything more generic.
#
# see http://fedoraproject.org/wiki/Licensing#Good_Licenses

my %shortname = (

    # classname                         => shortname
    'Software::License::AGPL_3'         => 'AGPLv3',
    'Software::License::Apache_1_1'     => 'ASL 1.1',
    'Software::License::Apache_2_0'     => 'ASL 2.0',
    'Software::License::Artistic_1_0'   => 'Artistic',
    'Software::License::Artistic_2_0'   => 'Artistic 2.0',
    'Software::License::BSD'            => 'BSD',
    'Software::License::FreeBSD'        => 'BSD',
    'Software::License::GFDL_1_2'       => 'GFDL',
    'Software::License::GPL_1'          => 'GPL',
    'Software::License::GPL_2'          => 'GPLv2',
    'Software::License::GPL_3'          => 'GPLv3',
    'Software::License::LGPL_2_1'       => 'LGPLv2',
    'Software::License::LGPL_3_0'       => 'LGPLv3',
    'Software::License::MIT'            => 'MIT',
    'Software::License::Mozilla_1_0'    => 'MPLv1.0',
    'Software::License::Mozilla_1_1'    => 'MPLv1.1',
    'Software::License::Perl_5'         => 'GPL+ or Artistic',
    'Software::License::QPL_1_0'        => 'QPL',
    'Software::License::Sun'            => 'SPL',
    'Software::License::Zlib'           => 'zlib',
);

sub _module_license { 
    my $self = shift @_;

    my $module = $self->parent;
    
    my $lic_comment = q{};
    
    # First, check what CPAN says
    my $cpan_lic = $module->details->{'Public License'};

    ### $cpan_lic

    # then, check META.yml (if existing)
    my $extract_dir = dir $module->extract;
    my $meta_file   = file $extract_dir, 'META.yml';
    my @meta_lics;

    if (-e "$meta_file" && -r _) {

        my $meta = $meta_file->slurp;
        @meta_lics = 
            Software::LicenseUtils->guess_license_from_meta_yml($meta);
    }
        
    # FIXME we pretty much just ignore the META.yml license right now

    ### @meta_lics

    # then, check the pod in all found .pm/.pod's
    my $rule = File::Find::Rule->new;
    my @pms = File::Find::Rule
        ->or(
            File::Find::Rule->new->directory->name('blib')->prune->discard,
            File::Find::Rule->new->file->name('*.pm', '*.pod')
            )
        ->in($extract_dir)
        ;

    my %pm_lics;

    for my $file (@pms) {

        $file = file $file;
        #my $text = file($file)->slurp;
        my $text = $file->slurp;
        my @lics = Software::LicenseUtils->guess_license_from_pod($text);

        ### file: "$file"
        ### @lics
        
        #push @pm_lics, @lics;
        $pm_lics{$file->relative($extract_dir)} = [ @lics ]
            if @lics > 0;
    }

    ### %pm_lics

    my @lics;

    for my $file (sort keys %pm_lics) {

       my @file_lics = map { $shortname{$_} } @{$pm_lics{"$file"}};

       $lic_comment .= "# $file -> " . join(q{, }, @file_lics) . "\n";
       push @lics, @file_lics;
    }

    # FIXME need to sort out the licenses here
    @lics = uniq @lics;

    ### $lic_comment
    ### @lics

    if (@lics > 0) {

        $self->status->license(join(' or ', @lics));
        $self->status->license_comment($lic_comment);
    }
    else {
        
        $self->status->license($DEFAULT_LICENSE);
        $self->status->license_comment("# license auto-determination failed\n");
    }

    ### license: $self->status->license
    return;
}

#
# my $description = _module_description($module);
#
# given a cpanplus::module, try to extract its description from the
# embedded pod in the extracted files. this would be the first paragraph
# of the DESCRIPTION head1.
#
sub _module_description {
    my ($self, $module) = @_;

    # where tarball has been extracted
    my $path   = dirname $module->_status->extract;
    my $parser = Pod::POM->new;

    my @docfiles =
        map  { "$path/$_" }               # prepend extract directory
        sort { length $a <=> length $b }  # sort by length
        grep { /\.(pod|pm)$/ }            # filter potentially pod-containing
        @{ $module->_status->files };     # list of embedded files

    my $desc;

    # parse file, trying to find a header
    DOCFILE:
    foreach my $docfile ( @docfiles ) {

        # extract pod; the file may contain no pod, that's ok
        my $pom = $parser->parse_file($docfile);
        next DOCFILE unless defined $pom; 

        HEAD1:
        foreach my $head1 ($pom->head1) {

            next HEAD1 unless $head1->title eq 'DESCRIPTION';

            my $pom  = $head1->content;
            my $text = $pom->present('Pod::POM::View::Text');
            
            # limit to a single paragraph at the moment
            my $paragraph = (split /\n\n/, $text)[0]; 
            #$text = join "\n\n", @paragraphs;
            $text = q{};
	    $text = $paragraph;

            # autoformat and return...
            return autoformat $text, { all => 1 };
        }
    }

    return 'no description found';
}


#
# my $summary = _module_summary($module);
#
# given a cpanplus::module, return its registered description (if any)
# or try to extract it from the embedded pod in the extracted files.
#
sub _module_summary {
    my ($self, $module) = @_;

    # registered modules won't go farther...
    return $module->description if $module->description;

    my $path = dirname $module->_status->extract;

    my @docfiles =
        map  { "$path/$_" }               # prepend extract directory
        sort { length $a <=> length $b }  # we prefer top-level module summary
        grep { /\.(pod|pm)$/ }            
        @{ $module->_status->files };     # list of files embedded

    # parse file, trying to find a header
    my $parser = Pod::POM->new;
    DOCFILE:
    foreach my $docfile ( @docfiles ) {

        my $pom = $parser->parse_file($docfile);  
        next unless defined $pom;                 # no pod, that's ok
    
        HEAD1:
        foreach my $head1 ($pom->head1) {

            my $title = $head1->title;
            next HEAD1 unless $title eq 'NAME';
            my $content = $head1->content;
            next DOCFILE unless $content =~ /^[^-]+ - (.*)$/m;
            return $1 if $content;
        }
    }

    return 'no summary found';
}

1;

__DATA__
__[ spec ]__
Name:       [% status.rpmname %] 
Version:    [% status.distvers %] 
Release:    [% status.rpmvers %]%{?dist}
[% status.license_comment -%]
License:    [% status.license %] 
Group:      Development/Libraries
Summary:    [% status.summary %] 
Source:     http://search.cpan.org/CPAN/[% module.path %]/[% status.distname %]-%{version}.[% module.package_extension %] 
Url:        http://search.cpan.org/dist/[% status.distname %]
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
%define __perl /opt/rocks/bin/perl
%define _bindir /opt/rocks/bin
%define _mandir /opt/rocks/share/man
%define _docdir /opt/rocks/share/doc
Requires:   foundation-perl
[% IF status.is_noarch %]BuildArch:  noarch[% END %]

[% brs = buildreqs; FOREACH br = brs.keys.sort -%]
BuildRequires: perl([% br %])[% IF (brs.$br != 0) %] >= [% brs.$br %][% END %]
[% END -%]



%description
[% status.description -%]


%prep
%setup -q -n [% status.distname %]-%{version}

%build
[% IF (!status.is_noarch) -%]
%{__perl} Makefile.PL INSTALLDIRS=site OPTIMIZE="%{optflags}"
[% ELSE -%]
%{__perl} Makefile.PL INSTALLDIRS=site
[% END -%]
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
[% IF (!status.is_noarch) -%]
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
[% END -%]
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
/*

%changelog
* [% date %] [% packager %] [% status.distvers %]-[% status.rpmvers %]
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::Rocks version [% packagervers %])

__[ pod ]__

=head1 NAME

CPANPLUS::Dist::Rocks - a CPANPLUS backend to build Rocks RPM


=head1 SYNOPSIS

    cpan2dist --format=CPANPLUS::Dist::RPM Some::Random::Package

=head1 DESCRIPTION

CPANPLUS::Dist::RPM is a distribution class to create RPM packages
from CPAN modules, and all its dependencies. This allows you to have
the most recent copies of CPAN modules installed, using your package
manager of choice, but without having to wait for central repositories
to be updated.

You can either install them using the API provided in this package, or
manually via rpm.

Note that these packages are built automatically from CPAN and are
assumed to have the same license as perl and come without support.
Please always refer to the original CPAN package if you have questions.


=head1 CLASS METHODS

=head2 $bool = CPANPLUS::Dist::RPM->format_available;

Return a boolean indicating whether or not you can use this package to
create and install modules in your environment.

It will verify if you have all the necessary components available to build 
your own rpm packages. You will need at least these dependencies installed: 
C<rpm>, C<rpmbuild> and C<gcc>.


=head1 PUBLIC METHODS

=head2 $bool = $rpm->init;

Sets up the C<CPANPLUS::Dist::RPM> object for use. Creates all the needed 
status accessors.

Called automatically whenever you create a new C<CPANPLUS::Dist> object.


=head2 $bool = $rpm->prepare;

Prepares a distribution for creation. This means it will create the rpm
spec file needed to build the rpm and source rpm. This will also satisfy
any prerequisites the module may have.

Note that the spec file will be as accurate as possible. However, some
fields may wrong (especially the description, and maybe the summary)
since it relies on pod parsing to find those information.

Returns true on success and false on failure.

You may then call C<< $rpm->create >> on the object to create the rpm
from the spec file, and then C<< $rpm->install >> on the object to
actually install it.


=head2 $bool = $rpm->create;

Builds the rpm file from the spec file created during the C<create()>
step.

Returns true on success and false on failure.

You may then call C<< $rpm->install >> on the object to actually install it.


=head2 $bool = $rpm->install;

Installs the rpm using C<rpm -U>.

B</!\ Work in progress: not implemented.>

Returns true on success and false on failure


=head1 PRIVATE METHODS

These are only documented here as it may be useful to override them.

=head2 _prepare_status()

Prepare our $status.

=head2 _prepare_spec()

Generate and write out the spec file.

=head2 _package_exists()

Checks to see if an RPM for this module is already installed on the system.
Note that we only check the rpmdb; we leave checking package repos to
distribution-specific subclasses.

=head2 _buildreqs()

Takes no arguments; returns a hashref of the buildrequires of this module.

=head2 _docfiles()

Takes no arguments; returns an arrayref of the files which should be included
as %doc in the spec.

=head2 _is_noarch()

Takes no arguments; returns true if the module is pure-perl; false otherwise.

=head2 _is_module_build_compat()

Return true if the Makefile.PL is actually a front for Module::Build.

=head2 _mk_pkg_name()

If passed an argument, makes an rpm package name out of it; returns the rpm
package name of the module we're operating against if none given.

=head2 _module_summary()

Get the one-liner summary of the module for %summary.

=head2 _module_description()

Get the module's description for %description.

=head2 _module_license

Get the module's license for License:.  Note that while this is still
incomplete, we now use L<Software::License> to try to figure out the correct
license from the .pm/.pod files.

=head1 STANDARDS COMPLIANCE

This particular base class does not endeavour to satisfy any Linux
distribution's packaging guidelines.  It does, however, strive to create
clean, sane specs and resulting rpm packages.

Until subclassing, users should not be surprised to note a marked similarity
to the Fedora/RedHat Perl packaging guidelines.

=head1 TODO

=over

=item o Deeper scan for proper license

We do use L<Software::License> to scan any .pm/.pod files.  However, we could
and should be checking META.yml and any COPYING/LICENSE files that happen to
be bundled.

=item o Long description

Right now we provide the description as given by the module in its
meta data. However, not all modules provide this meta data and rather
than scanning the files in the package for it, we simply default to the
name of the module.


=back


=head1 BUGS

Please report any bugs or feature requests to C<< < bug-CPANPLUS-Dist-RPM at
rt.cpan.org> >>, or through the web interface at
L<http://rt.cpan.org/NoAuth/ReportBug.html?Queue=CPANPLUS-Dist-RPM>.  I
will be notified, and then you'll automatically be notified of progress
on your bug as I make changes.



=head1 SEE ALSO

L<CPANPLUS::Backend>, L<CPANPLUS::Module>, L<CPANPLUS::Dist>,
C<cpan2dist>, C<rpm>


C<CPANPLUS::Dist::RPM> development takes place at
L<http://code.google.com/p/cpanplus-dist-rpm/>.

You can also look for information on this module at:

=over 4

=item * AnnoCPAN: Annotated CPAN documentation
L<http://annocpan.org/dist/CPANPLUS-Dist-RPM>

=item * CPAN Ratings

L<http://cpanratings.perl.org/d/CPANPLUS-Dist-RPM>

=item * RT: CPAN's request tracker

L<http://rt.cpan.org/NoAuth/Bugs.html?Dist=CPANPLUS-Dist-RPM>

=back



=head1 AUTHOR

Originally based on CPANPLUS-Dist-Mdv by:

Jerome Quelin, C<< <jquelin at cpan.org> >>

Shlomi Fish ( L<http://www.shlomifish.org/> ) changed it into 
CPANPLUS-Dist-Fedora.

Chris Weyl C<< <cweyl@alumni.drew.edu> >> changed it again to
CPANPLUS-Dist-RPM.

=head1 COPYRIGHT & LICENSE

Copyright (c) 2007 Jerome Quelin, Shlomi Fish, Chris Weyl.

This program is free software; you can redistribute it and/or modify
it under the same terms as Perl itself.

Modified by Shlomi Fish, 2008 - all ownership disclaimed.

Modified again by Chris Weyl <cweyl@alumni.drew.edu> 2008.

=cut

