# ninjam-vm: utilization recorder for the Oracle VM

Measures what a real jam costs, so the VM can be sized (target: 1 OCPU / 6 GB)
and the balcony's share seen once it runs.

- `ninjam-metrics`: Python, reads only `/proc`. `record` samples every 5 s until
  stopped; `summary [FILE.csv]` prints averages and peaks over the samples where
  someone was connected, plus total traffic.
- `ninjam-metrics.service`: `WantedBy=ninjam.service` and `PartOf=ninjam.service`,
  so it starts and stops with the room (`ninjam-room open` / `close`). Runs as
  `nobody`.

Each run leaves `/var/lib/ninjam-metrics/<start>.csv` and `<start>.summary.txt`
on the VM. Columns: whole-VM CPU %, ninjamsrv and balcony CPU % (of all CPUs),
memory used, their RSS, network in/out in kbit/s, clients on port 2049, load.
From this machine: `ninjam-room metrics [FILE.csv]`.

Install or update (from this directory):

    K="-i ~/.ssh/oracle-ninjam"
    scp $K ninjam-metrics ninjam-metrics.service ubuntu@163.192.60.76:/tmp/
    ssh $K ubuntu@163.192.60.76 'sudo install -m 755 /tmp/ninjam-metrics /usr/local/bin/ &&
      sudo install -m 644 /tmp/ninjam-metrics.service /etc/systemd/system/ &&
      sudo systemctl daemon-reload && sudo systemctl enable ninjam-metrics'

Remove: `sudo systemctl disable ninjam-metrics`, then delete the two files.
