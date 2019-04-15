#!/usr/bin/perl

# send_cot_packets: send CoT packets to the specified address and port.
#               Looks for newline-delimited packets on stdin.
#
# --stevens 1-8-10

use strict;
use Socket;

if(@ARGV !~ /^(3|4)$/){
    print "Usage: send_cot_packets.pl ip_address port rawdata [packet_count]\n";
    exit -1;
}

my $ip = $ARGV[0];
my $port = $ARGV[1];
my $rawdata = $ARGV[2];
my $max_packets = defined $ARGV[3] ? $ARGV[3] : 1_000_000;
my $sleep_interval = 1;  # seconds

socket(my $msgsock,PF_INET,SOCK_DGRAM,getprotobyname("udp")) || die "couldn't open UDP socket: $!";

setsockopt($msgsock,SOL_SOCKET,SO_BROADCAST,1) || die "setsockopt: $!";

my $destpaddr = sockaddr_in($port,inet_aton($ip));

open(PACKETS,$rawdata) || die "couldn't open raw data from file '$rawdata'";

my $count = 1;
while(<PACKETS>){
    last if($count > $max_packets);

    # ignore comments
    next if (/^#/);

    print "Packet $count: sending on $ip:$port: ";

    my $lat=0;
    my $lon=0;
    my $alt=0;
    my $rv=0;

    if(/lat="([^"]+)"/){
	$lat = $1;
	print "lat=$lat ";
    }

    if(/lon="([^"]+)"/){
	$lon = $1;
	print "lon=$lon ";
    }

    if(/hae="([^"]+)"/){
	$alt = $1;
	print "alt=$alt ";
    }

    $count++;

    $rv=send($msgsock,$_,0,$destpaddr) || die "send: $!";
    print "rv=$rv\n";
    sleep($sleep_interval);
}

