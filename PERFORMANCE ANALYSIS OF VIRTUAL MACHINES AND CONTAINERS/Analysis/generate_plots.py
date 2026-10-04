from pathlib import Path
import csv
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "results" / "processed"
FIG = ROOT / "results" / "figures"
FIG.mkdir(parents=True, exist_ok=True)


def read_csv(filename):
    with open(DATA / filename, newline="") as f:
        return list(csv.DictReader(f))


def save(fig, filename):
    fig.tight_layout()
    fig.savefig(FIG / filename, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("Created:", filename)


# -------------------------------------------------
# 1. CPU PERFORMANCE
# -------------------------------------------------
data = read_csv("cpu_results.csv")

vm = [float(r["events_per_second"]) for r in data if r["system"] == "vm"]
container = [float(r["events_per_second"]) for r in data if r["system"] == "container"]

fig, ax = plt.subplots()
ax.boxplot([vm, container], tick_labels=["VM", "Container"])
ax.set_title("CPU Performance")
ax.set_ylabel("Events per second")
ax.grid(axis="y", alpha=0.3)
save(fig, "01_cpu_performance.png")


# -------------------------------------------------
# 2. MEMORY PERFORMANCE
# -------------------------------------------------
data = read_csv("memory_results.csv")

vm = [float(r["memory_mib_per_sec"]) for r in data if r["system"] == "vm"]
container = [float(r["memory_mib_per_sec"]) for r in data if r["system"] == "container"]

fig, ax = plt.subplots()
ax.boxplot([vm, container], tick_labels=["VM", "Container"])
ax.set_title("Memory Performance")
ax.set_ylabel("MiB/sec")
ax.grid(axis="y", alpha=0.3)
save(fig, "02_memory_performance.png")


# -------------------------------------------------
# 3. DISK BANDWIDTH
# -------------------------------------------------
data = read_csv("disk_results.csv")

operations = ["seq-read", "seq-write", "random-read", "random-write"]

vm_bw = [
    float(next(r["bandwidth"] for r in data
               if r["system"] == "vm" and r["operation"] == op))
    for op in operations
]

container_bw = [
    float(next(r["bandwidth"] for r in data
               if r["system"] == "container" and r["operation"] == op))
    for op in operations
]

x = range(len(operations))
width = 0.35

fig, ax = plt.subplots()
ax.bar([i - width/2 for i in x], vm_bw, width, label="VM")
ax.bar([i + width/2 for i in x], container_bw, width, label="Container")
ax.set_xticks(list(x))
ax.set_xticklabels(operations, rotation=20)
ax.set_ylabel("MiB/sec")
ax.set_title("Disk Bandwidth")
ax.legend()
ax.grid(axis="y", alpha=0.3)
save(fig, "03_disk_bandwidth.png")


# -------------------------------------------------
# 4. DISK IOPS
# -------------------------------------------------
vm_iops = [
    float(next(r["iops"] for r in data
               if r["system"] == "vm" and r["operation"] == op))
    for op in operations
]

container_iops = [
    float(next(r["iops"] for r in data
               if r["system"] == "container" and r["operation"] == op))
    for op in operations
]

fig, ax = plt.subplots()
ax.bar([i - width/2 for i in x], vm_iops, width, label="VM")
ax.bar([i + width/2 for i in x], container_iops, width, label="Container")
ax.set_xticks(list(x))
ax.set_xticklabels(operations, rotation=20)
ax.set_ylabel("IOPS")
ax.set_title("Disk IOPS")
ax.legend()
ax.grid(axis="y", alpha=0.3)
save(fig, "04_disk_iops.png")


# -------------------------------------------------
# 5. NETWORK THROUGHPUT
# -------------------------------------------------
data = read_csv("network_results.csv")

tests = ["iperf3", "iperf3_P4"]

vm_net = [
    float(next(r["gbits_per_sec"] for r in data
               if r["system"] == "vm" and r["test"] == t))
    for t in tests
]

container_net = [
    float(next(r["gbits_per_sec"] for r in data
               if r["system"] == "container" and r["test"] == t))
    for t in tests
]

x = range(len(tests))

fig, ax = plt.subplots()
ax.bar([i - width/2 for i in x], vm_net, width, label="VM")
ax.bar([i + width/2 for i in x], container_net, width, label="Container")
ax.set_xticks(list(x))
ax.set_xticklabels(tests)
ax.set_ylabel("Gbits/sec")
ax.set_title("Network Throughput")
ax.legend()
ax.grid(axis="y", alpha=0.3)
save(fig, "05_network_throughput.png")


# -------------------------------------------------
# 6. APPLICATION PERFORMANCE
# -------------------------------------------------
data = read_csv("application_results.csv")

endpoints = ["health", "compute"]

vm_rps = [
    float(next(r["requests_per_second"] for r in data
               if r["system"] == "vm" and r["endpoint"] == e))
    for e in endpoints
]

container_rps = [
    float(next(r["requests_per_second"] for r in data
               if r["system"] == "container" and r["endpoint"] == e))
    for e in endpoints
]

x = range(len(endpoints))

fig, ax = plt.subplots()
ax.bar([i - width/2 for i in x], vm_rps, width, label="VM")
ax.bar([i + width/2 for i in x], container_rps, width, label="Container")
ax.set_xticks(list(x))
ax.set_xticklabels(endpoints)
ax.set_ylabel("Requests/sec")
ax.set_title("Application Throughput")
ax.legend()
ax.grid(axis="y", alpha=0.3)
save(fig, "06_application_throughput.png")


# -------------------------------------------------
# 7. APPLICATION LATENCY
# -------------------------------------------------
vm_latency = [
    float(next(r["time_per_request_ms"] for r in data
               if r["system"] == "vm" and r["endpoint"] == e))
    for e in endpoints
]

container_latency = [
    float(next(r["time_per_request_ms"] for r in data
               if r["system"] == "container" and r["endpoint"] == e))
    for e in endpoints
]

fig, ax = plt.subplots()
ax.bar([i - width/2 for i in x], vm_latency, width, label="VM")
ax.bar([i + width/2 for i in x], container_latency, width, label="Container")
ax.set_xticks(list(x))
ax.set_xticklabels(endpoints)
ax.set_ylabel("Milliseconds")
ax.set_title("Application Latency")
ax.legend()
ax.grid(axis="y", alpha=0.3)
save(fig, "07_application_latency.png")


# -------------------------------------------------
# 8. STARTUP TIME
# -------------------------------------------------
data = read_csv("startup_results.csv")

vm = [float(r["startup_ms"]) for r in data if r["system"] == "vm"]
container = [float(r["startup_ms"]) for r in data if r["system"] == "container"]

fig, ax = plt.subplots()
ax.boxplot([vm, container], tick_labels=["VM", "Container"])
ax.set_title("Application Startup Time")
ax.set_ylabel("Milliseconds")
ax.grid(axis="y", alpha=0.3)
save(fig, "08_startup_time.png")


# -------------------------------------------------
# 9. CPU SCALABILITY
# -------------------------------------------------
data = read_csv("cpu_scalability.csv")

threads = [1, 2, 4, 8]

vm = [
    float(next(r["events_per_second"] for r in data
               if r["system"] == "vm" and int(r["threads"]) == t))
    for t in threads
]

container = [
    float(next(r["events_per_second"] for r in data
               if r["system"] == "container" and int(r["threads"]) == t))
    for t in threads
]

fig, ax = plt.subplots()
ax.plot(threads, vm, marker="o", label="VM")
ax.plot(threads, container, marker="o", label="Container")
ax.set_xticks(threads)
ax.set_xlabel("Threads")
ax.set_ylabel("Events per second")
ax.set_title("CPU Scalability")
ax.legend()
ax.grid(True, alpha=0.3)
save(fig, "09_cpu_scalability.png")


# -------------------------------------------------
# 10. API SCALABILITY
# -------------------------------------------------
data = read_csv("api_scalability.csv")

workloads = [1, 2, 4, 8]

vm = [
    float(next(r["requests_per_second"] for r in data
               if r["system"] == "vm" and int(r["workload"]) == w))
    for w in workloads
]

container = [
    float(next(r["requests_per_second"] for r in data
               if r["system"] == "container" and int(r["workload"]) == w))
    for w in workloads
]

fig, ax = plt.subplots()
ax.plot(workloads, vm, marker="o", label="VM")
ax.plot(workloads, container, marker="o", label="Container")
ax.set_xticks(workloads)
ax.set_xlabel("Concurrent Workload")
ax.set_ylabel("Requests/sec")
ax.set_title("API Scalability")
ax.legend()
ax.grid(True, alpha=0.3)
save(fig, "10_api_scalability.png")


print("\nAll figures generated successfully.")
print("Location:", FIG)
