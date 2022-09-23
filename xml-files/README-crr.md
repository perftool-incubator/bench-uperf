# crr.xml
The crr test may exhaust client-side port numbers, due to TCP close_time_wait, which keeps TCP connections around for 60 seconds.  Due to this situation, we recommend not exceeding ~800 connections per second, per client.  To drive a server at a higher connection rate, use multiple clients (with different IP addresses) to multiple servers (on same host with same IP address).
