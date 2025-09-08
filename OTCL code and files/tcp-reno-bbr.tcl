set sim [new Simulator]

$sim color 1 Green
$sim color 2 Orange

set nam_file [open project_BBR.nam w]
$sim namtrace-all $nam_file
set trace_file [open project_trace_BBR.tr w]
$sim trace-all $trace_file

set random_gen [new RNG]
$random_gen seed 2
set delay_var [new RandomVariable/Uniform]
$delay_var use-rng $random_gen
$delay_var set min_ 5.0
$delay_var set max_ 25.0

proc end_simulation {} {
    global sim nam_file trace_file
    $sim flush-trace
    close $nam_file
    close $trace_file
    exit 0
}

set server1 [$sim node]
set server2 [$sim node]
set router1 [$sim node]
set router2 [$sim node]
set server3 [$sim node]
set server4 [$sim node]

set delay1 [$delay_var value]
set delay2 [$delay_var value]

set delay1_rounded [format "%.2f" $delay1]
set delay2_rounded [format "%.2f" $delay2]

puts $delay1_rounded
puts $delay2_rounded

$sim duplex-link $server1 $router1 100Mb 5ms DropTail
$sim duplex-link $server2 $router1 100Mb ${delay1_rounded}ms DropTail
$sim duplex-link $router1 $router2 100kb 1ms DropTail
$sim duplex-link $router2 $server3 100Mb 5ms DropTail
$sim duplex-link $router2 $server4 100Mb ${delay2_rounded}ms DropTail
$sim queue-limit $router1 $router2 10
$sim queue-limit $router2 $router1 10
$sim duplex-link-op $server1 $router1 orient right-down
$sim duplex-link-op $server2 $router1 orient right-up
$sim duplex-link-op $router1 $router2 orient right
$sim duplex-link-op $router2 $server3 orient right-up
$sim duplex-link-op $router2 $server4 orient right-down

set sender1 [new Agent/TCP/Reno/BBR]
$sender1 set class_ 2
$sender1 set ttl_ 64
$sim attach-agent $server1 $sender1
set receiver1 [new Agent/TCPSink]
$sim attach-agent $server3 $receiver1
$sim connect $sender1 $receiver1
$sender1 set fid_ 1
set sender2 [new Agent/TCP/Reno/BBR]
$sender2 set class_ 1
$sender2 set ttl_ 64
$sim attach-agent $server2 $sender2
set receiver2 [new Agent/TCPSink]
$sim attach-agent $server4 $receiver2
$sim connect $sender2 $receiver2
$sender2 set fid_ 2

$sender1 attach $trace_file
$sender1 tracevar cwnd_
$sender1 tracevar ssthresh_
$sender1 tracevar ack_
$sender1 tracevar maxseq_
$sender1 tracevar rtt_
$sender2 attach $trace_file
$sender2 tracevar cwnd_
$sender2 tracevar ssthresh_
$sender2 tracevar ack_
$sender2 tracevar maxseq_
$sender2 tracevar rtt_

set ftp_app1 [new Application/FTP]
$ftp_app1 attach-agent $sender1
set ftp_app2 [new Application/FTP]
$ftp_app2 attach-agent $sender2

$sim at 0.0 "$ftp_app2 start"
$sim at 0.0 "$ftp_app1 start"
$sim at 1000.0 "end_simulation"
$sim run

