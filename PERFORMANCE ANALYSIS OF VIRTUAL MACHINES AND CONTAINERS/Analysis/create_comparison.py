from pathlib import Path
import csv
import statistics

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "results" / "processed"
ANALYSIS = ROOT / "analysis"

def read_csv(name):
    with open(DATA / name, newline="") as f:
        return list(csv.DictReader(f))

def pct_change(vm, container):
    return ((container - vm) / vm) * 100

# ----------------------------------------
# Final direct comparison
# ----------------------------------------
comparison = []

# CPU
data = read_csv("cpu_results.csv")
vm = [float(r["events_per_second"]) for r in data if r["system"] == "vm"]
container = [float(r["events_per_second"]) for r in data if r["system"] == "container"]

comparison.append({
    "benchmark": "CPU",
    "test": "Average",
    "metric": "Events/sec",
    "vm": statistics.mean(vm),
    "container": statistics.mean(container),
    "container_minus_vm_percent": pct_change(statistics.mean(vm), statistics.mean(container))
})

# Memory
data = read_csv("memory_results.csv")
vm = [float(r["memory_mib_per_sec"]) for r in data if r["system"] == "vm"]
container = [float(r["memory_mib_per_sec"]) for r in data if r["system"] == "container"]

comparison.append({
    "benchmark": "Memory",
    "test": "Average",
    "metric": "MiB/sec",
    "vm": statistics.mean(vm),
    "container": statistics.mean(container),
    "container_minus_vm_percent": pct_change(statistics.mean(vm), statistics.mean(container))
})

# Startup
data = read_csv("startup_results.csv")
vm = [float(r["startup_ms"]) for r in data if r["system"] == "vm"]
container = [float(r["startup_ms"]) for r in data if r["system"] == "container"]

comparison.append({
    "benchmark": "Startup",
    "test": "Average",
    "metric": "Milliseconds",
    "vm": statistics.mean(vm),
    "container": statistics.mean(container),
    "container_minus_vm_percent": pct_change(statistics.mean(vm), statistics.mean(container))
})

# Disk
data = read_csv("disk_results.csv")
for operation in ["seq-read", "seq-write", "random-read", "random-write"]:
    row_vm = next(r for r in data if r["system"] == "vm" and r["operation"] == operation)
    row_c = next(r for r in data if r["system"] == "container" and r["operation"] == operation)

    vm_bw = float(row_vm["bandwidth"])
    c_bw = float(row_c["bandwidth"])
    comparison.append({
        "benchmark": "Disk",
        "test": operation,
        "metric": "MiB/sec",
        "vm": vm_bw,
        "container": c_bw,
        "container_minus_vm_percent": pct_change(vm_bw, c_bw)
    })

    vm_iops = float(row_vm["iops"])
    c_iops = float(row_c["iops"])
    comparison.append({
        "benchmark": "Disk",
        "test": operation,
        "metric": "IOPS",
        "vm": vm_iops,
        "container": c_iops,
        "container_minus_vm_percent": pct_change(vm_iops, c_iops)
    })

# Network
data = read_csv("network_results.csv")
for test in ["iperf3", "iperf3_P4"]:
    vm = float(next(r["gbits_per_sec"] for r in data
                   if r["system"] == "vm" and r["test"] == test))
    container = float(next(r["gbits_per_sec"] for r in data
                          if r["system"] == "container" and r["test"] == test))

    comparison.append({
        "benchmark": "Network",
        "test": test,
        "metric": "Gbits/sec",
        "vm": vm,
        "container": container,
        "container_minus_vm_percent": pct_change(vm, container)
    })

# Application
data = read_csv("application_results.csv")
for endpoint in ["health", "compute"]:
    vm = next(r for r in data if r["system"] == "vm" and r["endpoint"] == endpoint)
    container = next(r for r in data if r["system"] == "container" and r["endpoint"] == endpoint)

    vm_rps = float(vm["requests_per_second"])
    c_rps = float(container["requests_per_second"])
    comparison.append({
        "benchmark": "Application",
        "test": endpoint,
        "metric": "Requests/sec",
        "vm": vm_rps,
        "container": c_rps,
        "container_minus_vm_percent": pct_change(vm_rps, c_rps)
    })

    vm_lat = float(vm["time_per_request_ms"])
    c_lat = float(container["time_per_request_ms"])
    comparison.append({
        "benchmark": "Application",
        "test": endpoint,
        "metric": "Latency (ms)",
        "vm": vm_lat,
        "container": c_lat,
        "container_minus_vm_percent": pct_change(vm_lat, c_lat)
    })

# Save comparison CSV
csv_out = DATA / "final_comparison.csv"
fields = [
    "benchmark",
    "test",
    "metric",
    "vm",
    "container",
    "container_minus_vm_percent"
]

with open(csv_out, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for row in comparison:
        writer.writerow({
            **row,
            "vm": f"{row['vm']:.2f}",
            "container": f"{row['container']:.2f}",
            "container_minus_vm_percent": f"{row['container_minus_vm_percent']:.2f}"
        })

# ----------------------------------------
# CPU scalability
# ----------------------------------------
data = read_csv("cpu_scalability.csv")
cpu_scale = []

for threads in [1, 2, 4, 8]:
    vm = float(next(r["events_per_second"] for r in data
                   if r["system"] == "vm" and int(r["threads"]) == threads))
    container = float(next(r["events_per_second"] for r in data
                           if r["system"] == "container" and int(r["threads"]) == threads))

    cpu_scale.append(
        f"| {threads} | {vm:.2f} | {container:.2f} | {pct_change(vm, container):+.2f}% |"
    )

# ----------------------------------------
# API scalability
# ----------------------------------------
data = read_csv("api_scalability.csv")
api_scale = []

for workload in [1, 2, 4, 8]:
    vm_row = next(r for r in data
                  if r["system"] == "vm" and int(r["workload"]) == workload)
    c_row = next(r for r in data
                 if r["system"] == "container" and int(r["workload"]) == workload)

    vm_rps = float(vm_row["requests_per_second"])
    c_rps = float(c_row["requests_per_second"])

    vm_lat = float(vm_row["latency_ms"])
    c_lat = float(c_row["latency_ms"])

    api_scale.append({
        "workload": workload,
        "vm_rps": vm_rps,
        "container_rps": c_rps,
        "rps_change": pct_change(vm_rps, c_rps),
        "vm_latency": vm_lat,
        "container_latency": c_lat,
        "latency_change": pct_change(vm_lat, c_lat)
    })

# ----------------------------------------
# Markdown report
# ----------------------------------------
md_out = ANALYSIS / "comparison_summary.md"

with open(md_out, "w") as f:
    f.write("# VM vs Container Performance Comparison\n\n")

    f.write("## Direct comparison\n\n")
    f.write("| Benchmark | Test | Metric | VM | Container | Container vs VM |\n")
    f.write("|---|---|---|---:|---:|---:|\n")

    for row in comparison:
        f.write(
            f"| {row['benchmark']} | {row['test']} | {row['metric']} | "
            f"{row['vm']:.2f} | {row['container']:.2f} | "
            f"{row['container_minus_vm_percent']:+.2f}% |\n"
        )

    f.write("\n## CPU scalability\n\n")
    f.write("| Threads | VM Events/sec | Container Events/sec | Container vs VM |\n")
    f.write("|---:|---:|---:|---:|\n")
    f.write("\n".join(cpu_scale))

    f.write("\n\n## API scalability\n\n")
    f.write("| Workload | VM Req/sec | Container Req/sec | Req/sec Change | VM Latency (ms) | Container Latency (ms) | Latency Change |\n")
    f.write("|---:|---:|---:|---:|---:|---:|---:|\n")

    for row in api_scale:
        f.write(
            f"| {row['workload']} | {row['vm_rps']:.2f} | {row['container_rps']:.2f} | "
            f"{row['rps_change']:+.2f}% | {row['vm_latency']:.2f} | "
            f"{row['container_latency']:.2f} | {row['latency_change']:+.2f}% |\n"
        )

print("Created:")
print(csv_out)
print(md_out)
