package testdb;
# module that provides connectivity to our local lab database
#
use DBI;
use strict;

our $host = $ENV{'DBLOCALHOST'};
our $port = $ENV{'DBLOCALPORT'};
our $db = 'bfl';
our $user = $ENV{'DBPRIVUSER'};
our $password = $ENV{'DBPRIVPW'};

our $dsn;
our $dh;

sub conn {
    my ($h, $p, $d, $u, $pw) = @_;
    $h = $host unless defined $h;
    $p = $port unless defined $p;
    $d = $db unless defined $d;
    $u = $user unless defined $u;
    $pw = $password unless defined $pw;
    $dsn = "DBI:mysql:database=$d;host=$h;port=$p";
    $dh = DBI->connect($dsn, $u, $pw) or die DBI->errstr;
    return $dh;
}

1;
