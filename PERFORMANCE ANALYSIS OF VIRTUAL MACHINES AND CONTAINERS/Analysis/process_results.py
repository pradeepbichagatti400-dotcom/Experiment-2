from pathlib import Path
import re
import csv
import statistics

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "results" / "raw"
OUT = ROOT / "results" / "processed"

OUT.mkdir(parents=True, exist_ok=True)


def read(path):
    return path.read_text(errors="ignore")


def extract(pattern, text, group=1):
    m = re.search(pattern, text, re.MULTILINE)
    return float(m.group(group)) if m else None


def write_csv(filename, rows, fields):
    path = OUT / filename
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Created: {path}")


# ============================================================
# CPU
# ============================================================

rows = []

for system in ["vm", "container"]:
    folder = RAW / "cpu" / system

    for i in range(1, 11):
        path = folder / f"run{i}.txt"
        text = read(path)

        value = extract(
            r"events per second:\s*([\d.]+)",
            text
        )

        rows.append({
            "system": system,
            "run": i,
            "events_per_second": value
        })

write_csv(
    "cpu_results.csv",
    rows,
    ["system", "run", "events_per_second"]
)


# ============================================================
# CPU SCALABILITY
# ============================================================

rows = []

for system in ["vm", "container"]:
    folder = RAW / "cpu" / "scalability" / system

    for threads in [1, 2, 4, 8]:
        path = folder / f"threads_{threads}.txt"
        text = read(path)

        value = extract(
            r"events per second:\s*([\d.]+)",
            text
        )

        rows.append({
            "system": system,
            "threads": threads,
            "events_per_second": value
        })

write_csv(
    "cpu_scalability.csv",
    rows,
    ["system", "threads", "events_per_second"]
)


# ============================================================
# MEMORY
# ============================================================

rows = []

for system in ["vm", "container"]:
    folder = RAW / "memory" / system

    for i in range(1, 11):
        path = folder / f"run{i}.txt"
        text = read(path)

        value = extract(
            r"MiB transferred \(([\d.]+) MiB/sec\)",
            text
        )

        rows.append({
            "system": system,
            "run": i,
            "memory_mib_per_sec": value
        })

write_csv(
    "memory_results.csv",
    rows,
    ["system", "run", "memory_mib_per_sec"]
)


# ============================================================
# DISK
# ============================================================

rows = []

for system in ["vm", "container"]:
    folder = RAW / "disk" / system

    for operation in [
        "seq-read",
        "seq-write",
        "random-read",
        "random-write"
    ]:
        path = folder / f"{operation}.txt"
        text = read(path)

        # Read/write line such as:
        # READ: bw=1134MiB/s ...
        bw = extract(
            r"(?:READ|WRITE):\s*bw=([\d.]+)([KMG]iB/s)",
            text
        )

        iops = extract(
            r"(?:read|write):\s*IOPS=([\d.]+)",
            text,
        )

        rows.append({
            "system": system,
            "operation": operation,
            "bandwidth": bw,
            "iops": iops
        })

write_csv(
    "disk_results.csv",
    rows,
    ["system", "operation", "bandwidth", "iops"]
)


# ============================================================
# NETWORK
# ============================================================

rows = []

for system in ["vm", "container"]:
    for test in ["iperf3", "iperf3_P4"]:
        path = RAW / "network" / system / f"{test}.txt"
        text = read(path)

        matches = re.findall(
            r"\d+\.\d+-\d+\.\d+\s+sec.*?([\d.]+)\s+Gbits/sec",
            text
        )

        bitrate = None

        if matches:
            bitrate = float(matches[-1])

        rows.append({
            "system": system,
            "test": test,
            "gbits_per_sec": bitrate
        })

write_csv(
    "network_results.csv",
    rows,
    ["system", "test", "gbits_per_sec"]
)


# ============================================================
# APPLICATION
# ============================================================

rows = []

for system in ["vm", "container"]:
    folder = RAW / "application" / system

    for endpoint in ["health", "compute"]:
        path = folder / f"{endpoint}.txt"
        text = read(path)

        rps = extract(
            r"Requests per second:\s*([\d.]+)",
            text
        )

        latency = extract(
            r"Time per request:\s*([\d.]+)\s+\[ms\] \(mean\)",
            text
        )

        rows.append({
            "system": system,
            "endpoint": endpoint,
            "requests_per_second": rps,
            "time_per_request_ms": latency
        })

write_csv(
    "application_results.csv",
    rows,
    ["system", "endpoint", "requests_per_second",
     "time_per_request_ms"]
)


# ============================================================
# STARTUP
# ============================================================

rows = []

for system in ["vm", "container"]:
    folder = RAW / "startup" / system

    for i in range(1, 6):
        path = folder / f"run{i}.txt"
        text = read(path)

        value = extract(
            r"application-ready time:\s*([\d.]+)\s*ms",
            text
        )

        rows.append({
            "system": system,
            "run": i,
            "startup_ms": value
        })

write_csv(
    "startup_results.csv",
    rows,
    ["system", "run", "startup_ms"]
)


# ============================================================
# API SCALABILITY
# ============================================================

rows = []

for system in ["vm", "container"]:
    folder = RAW / "scalability" / system

    for workload in [1, 2, 4, 8]:
        path = folder / f"workload{workload}.txt"
        text = read(path)

        rps = extract(
            r"Requests/sec:\s*([\d.]+)",
            text
        )

        latency = extract(
            r"Latency\s+([\d.]+)ms",
            text
        )

        rows.append({
            "system": system,
            "workload": workload,
            "requests_per_second": rps,
            "latency_ms": latency
        })

write_csv(
    "api_scalability.csv",
    rows,
    ["system", "workload",
     "requests_per_second", "latency_ms"]
)


print("\nProcessing complete!")
print(f"Processed files are in: {OUT}")
