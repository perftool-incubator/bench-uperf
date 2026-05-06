#!/usr/bin/env python3
# -*- mode: python; indent-tabs-mode: nil; python-indent-level: 4 -*-
# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

import argparse
import json
import os
import re
import sys
from pathlib import Path

TOOLBOX_HOME = os.environ.get("TOOLBOX_HOME")
if TOOLBOX_HOME:
    sys.path.append(str(Path(TOOLBOX_HOME) / "python"))

from toolbox.cdm_metrics import CDMMetrics
from toolbox.fileio import open_read_text_file


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--test-type", default=None)
    parser.add_argument("--nthreads", type=int, default=1)
    parser.add_argument("--remotehost", default=None)
    parser.add_argument("--wsize", type=int, default=None)
    parser.add_argument("--rsize", type=int, default=None)
    parser.add_argument("--think", type=float, default=None)
    parser.add_argument("--protocol", default=None)
    parser.add_argument("--duration", type=int, default=None)
    parser.add_argument("--ifname", default=None)
    parser.add_argument("--cpu-pin", default=None)
    parser.add_argument("--ipv", type=int, default=None)
    args, _ = parser.parse_known_args()

    test_type = args.test_type
    nthreads = args.nthreads

    if test_type is None:
        print("uperf-post-process(): test-type not defined, assuming this is server and exiting")
        sys.exit(0)

    if test_type in ("rr", "ping-pong"):
        primary_metric = "transactions-sec"
    elif test_type == "crr":
        primary_metric = "connections-sec"
    else:
        primary_metric = "Gbps"

    metrics = CDMMetrics()
    result_file = "uperf-client-result.txt"

    try:
        fh, _ = open_read_text_file(result_file)
    except FileNotFoundError:
        print(f"uperf-post-process(): could not open {result_file}")
        print("Is the current directory for a uperf server (no result file)?")
        return

    ts = None
    prev_ts = None
    start_ts = None
    bytes_val = None
    prev_bytes = None
    ops = None
    prev_ops = None
    names = {}

    for line in fh:
        line = line.rstrip("\n")

        if test_type == "crr":
            m = re.match(r'^timestamp_ms:(\d+)\.\d+\s+name:Txn1\s+nr_bytes:(\d+)\s+nr_ops:(\d+)', line)
            if m:
                ts, bytes_val, ops = int(m.group(1)), int(m.group(2)), int(m.group(3))
                if prev_ts is not None:
                    ts_diff = (ts - prev_ts) / 1000
                    if ts_diff > 0:
                        desc = {"source": "uperf", "class": "throughput", "type": "Gbps"}
                        names_rw = {"cmd": "readandwrite"}
                        sample = {"end": ts, "value": 8.0 * (bytes_val - prev_bytes) / 1000000000 / ts_diff}
                        metrics.log_sample("0", desc, names_rw, sample)

                        cps = (ops - prev_ops) / ts_diff / 5
                        desc = {"source": "uperf", "class": "throughput", "type": "connections-sec"}
                        sample = {"end": ts, "value": float(cps)}
                        metrics.log_sample("0", desc, names, sample)

                        if cps > 0:
                            desc = {"source": "uperf", "class": "count", "type": "round-trip-usec"}
                            sample = {"end": ts, "value": float(nthreads / cps * 1000000)}
                            metrics.log_sample("0", desc, names, sample)

                prev_ts = ts
                prev_bytes = bytes_val
                prev_ops = ops
        else:
            m = re.match(
                r'^Difference\(%\)\s+(-?\d+\.\d+)%\s+(-?\d+\.\d+)%\s+(-?\d+\.\d+)%\s+(-?\d+\.\d+)%\s+(-?\d+\.\d+)%',
                line,
            )
            if m and start_ts is not None and ts is not None:
                desc = {"source": "uperf", "class": "count", "type": "throughput-delta-pct"}
                sample = {"begin": start_ts, "end": ts, "value": float(m.group(3))}
                metrics.log_sample("0", desc, names, sample)

            m = re.match(r'^timestamp_ms:(\d+)\.\d+\s+name:Txn2\s+nr_bytes:(\d+)\s+nr_ops:(\d+)', line)
            if m:
                ts, bytes_val, ops = int(m.group(1)), int(m.group(2)), int(m.group(3))
                if prev_ts is not None:
                    ts_diff = (ts - prev_ts) / 1000
                    if ts_diff > 0:
                        desc = {"source": "uperf", "class": "throughput", "type": "Gbps"}
                        names_rw = {"cmd": "readandwrite"}
                        sample = {"end": ts, "value": 8.0 * (bytes_val - prev_bytes) / 1000000000 / ts_diff}
                        metrics.log_sample("0", desc, names_rw, sample)

                        if test_type in ("rr", "ping-pong"):
                            tps = (ops - prev_ops) / ts_diff / 2
                            desc = {"source": "uperf", "class": "throughput", "type": "transactions-sec"}
                            sample = {"end": ts, "value": float(tps)}
                            metrics.log_sample("0", desc, names, sample)

                            if tps > 0:
                                desc = {"source": "uperf", "class": "count", "type": "round-trip-usec"}
                                sample = {"end": ts, "value": float(nthreads / tps * 1000000)}
                                metrics.log_sample("0", desc, names, sample)
                else:
                    start_ts = ts

                prev_ts = ts
                prev_bytes = bytes_val
                prev_ops = ops

    fh.close()
    metric_data_name = metrics.finish_samples()

    sample_data = {
        "rickshaw-bench-metric": {"schema": {"version": "2021.04.12"}},
        "benchmark": "uperf",
        "primary-period": "measurement",
        "primary-metric": primary_metric,
        "periods": [
            {
                "name": "measurement",
                "metric-files": [metric_data_name],
            }
        ],
    }

    with open("post-process-data.json", "w") as f:
        json.dump(sample_data, f)


if __name__ == "__main__":
    main()
