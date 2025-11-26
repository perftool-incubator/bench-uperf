# Limitatins (NOT implemented in this version)

- irqbalance needs to be manually enabled/disabled (chroot/systemd limitation)
- stop test when latency hits a threshold (not implemented)
- trace marker (tracefs sync)
- cpubound affinity in the xml file (multiple threads)
- print index of max latency (not implemented)
- warmup stage (start recording samples after x sec)
