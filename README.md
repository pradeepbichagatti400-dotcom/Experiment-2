# 🚀 Performance Analysis of Virtual Machines and Docker Containers

### Controlled Performance Comparison of a Virtual Machine and a Docker Container

![VM](https://img.shields.io/badge/Virtual%20Machine-VMware%20Workstation-blue?style=for-the-badge)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED?style=for-the-badge)
![Ubuntu](https://img.shields.io/badge/OS-Ubuntu-E95420?style=for-the-badge)
![Sysbench](https://img.shields.io/badge/CPU-Sysbench-success?style=for-the-badge)
![fio](https://img.shields.io/badge/Disk-fio-orange?style=for-the-badge)
![iperf3](https://img.shields.io/badge/Network-iperf3-purple?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge)

---

# 1. Problem Statement

Virtual Machines and Docker Containers provide isolated execution environments for applications and services, but they use different virtualization and resource-management mechanisms.

The performance of these environments can vary depending on CPU processing, memory operations, disk I/O, networking, application workload, startup behavior, and workload scalability.

Therefore, this experiment investigates:

> **How does the performance of a Virtual Machine compare with a Docker Container when equivalent workloads are executed under controlled resource conditions?**

The comparison is performed using standard benchmarking tools and a common application workload.

---

# 2. Objectives

1. **To compare the performance of a Virtual Machine and a Docker Container under controlled resource conditions.**

2. **To measure CPU, memory, disk I/O, and network performance using standard benchmarking tools.**

3. **To evaluate application throughput, latency, startup time, and scalability using a FastAPI workload.**

4. **To collect, process, and statistically analyze repeated benchmark measurements using Python.**

5. **To determine and present the performance differences between the Virtual Machine and Docker Container using tables and graphs.**

---

# 3. Virtual Machine

## 3.1 VM Configuration

The Virtual Machine configuration follows the controlled configuration specified in the laboratory manual.

| Parameter              | Configuration                   |
| ---------------------- | ------------------------------- |
| Hypervisor             | VMware Workstation              |
| Guest Operating System | Ubuntu 24.04 LTS                |
| vCPU                   | 4                               |
| Memory                 | 8 GB                            |
| Virtual Disk           | 60 GB                           |
| Network                | NAT / Bridged                   |
| Resource Allocation    | Fixed throughout the experiment |

The laboratory manual recommends fixed CPU, memory, disk, and network allocation so that the comparison remains controlled.

### VM Documentation

* [CPU Information](docs/cpu-info.txt)
* [Memory Information](docs/memory-info.txt)
* [Storage Information](docs/storage-info.txt)
* [Kernel Information](docs/kernel-info.txt)
* [VM Configuration](docs/vm-configuration.txt)

---

## 3.2 VM Architecture

```text
                 HOST SYSTEM
                      │
                      ▼
             ┌─────────────────┐
             │ VMware          │
             │ Workstation     │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │   Ubuntu VM     │
             │                 │
             │   4 vCPU        │
             │   8 GB RAM      │
             │   60 GB Disk    │
             │   NAT/Bridged   │
             └────────┬────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
      CPU          Memory       Disk / Network
        │             │             │
        └─────────────┼─────────────┘
                      ▼
                FastAPI Workload
```

---

## 3.3 VM Execution Steps

### Step 1 — Verify the System

```bash
lscpu
free -h
lsblk
df -h
uname -a
```

### Step 2 — Establish Baseline

```bash
sysbench cpu \
    --cpu-max-prime=20000 \
    --threads=4 \
    --time=30 \
    run
```

[Baseline CPU Output](results/raw/baseline/cpu.txt)

### Step 3 — CPU Benchmark

CPU performance was measured using Sysbench with:

```text
Prime limit = 20000
Threads     = 4
Duration    = 30 seconds
```

Ten repeated runs were collected.

### Step 4 — CPU Scalability

The CPU workload was evaluated using:

```text
1 thread
2 threads
4 threads
8 threads
```

### Step 5 — Memory Benchmark

Memory performance was measured using Sysbench.

The benchmark configuration used:

```text
Block size = 1 MiB
Threads    = 4
```

### Step 6 — Disk Benchmark

`fio` was used for:

```text
Sequential Read
Sequential Write
Random Read
Random Write
```

The measured metrics include:

```text
Bandwidth
IOPS
Latency
```

### Step 7 — Network Benchmark

Network performance was measured using:

```text
iperf3
iperf3_P4
```

### Step 8 — FastAPI Benchmark

The application workload was tested through:

```text
/health
/compute
```

using Apache Benchmark.

### Step 9 — Startup Test

Application startup/application-ready time was measured over repeated runs.

### Step 10 — Scalability Test

API scalability was evaluated at increasing workload levels.

### Step 11 — Store Results

Raw benchmark outputs were preserved under:

```text
results/raw/
```

Processed datasets were stored under:

```text
results/processed/
```

---

# 3.4 VM Results

## CPU Performance

| Metric               |                     VM |
| -------------------- | ---------------------: |
| Mean CPU Performance | **5522.52 events/sec** |

[VM CPU Raw Results](results/raw/cpu/vm/)
[CPU Processed Data](results/processed/cpu_results.csv)

---

## Memory Performance

| Metric                 |                   VM |
| ---------------------- | -------------------: |
| Mean Memory Throughput | **66625.29 MiB/sec** |

[VM Memory Results](results/raw/memory/vm/)
[Memory Processed Data](results/processed/memory_results.csv)

---

## Disk Performance

| Operation        |  Bandwidth | IOPS |
| ---------------- | ---------: | ---: |
| Sequential Read  | 1134 MiB/s | 1134 |
| Sequential Write |  864 MiB/s |  864 |
| Random Read      | 36.6 MiB/s | 9372 |
| Random Write     | 33.2 MiB/s | 8489 |

[VM Disk Results](results/raw/disk/vm/)
[Disk Processed Data](results/processed/disk_results.csv)

---

## Network Performance

| Test        |  VM Throughput |
| ----------- | -------------: |
| `iperf3`    | 84.3 Gbits/sec |
| `iperf3_P4` |  259 Gbits/sec |

[VM Network Results](results/raw/network/vm/)
[Network Processed Data](results/processed/network_results.csv)

---

## Application Performance

| Endpoint   | Requests/sec | Mean Latency |
| ---------- | -----------: | -----------: |
| `/health`  |      2212.07 |    45.206 ms |
| `/compute` |        34.94 |   286.199 ms |

[VM Application Results](results/raw/application/vm/)
[Application Processed Data](results/processed/application_results.csv)

---

## Startup Performance

| Metric            |         VM |
| ----------------- | ---------: |
| Mean Startup Time | **350 ms** |

[VM Startup Results](results/raw/startup/vm/)
[Startup Processed Data](results/processed/startup_results.csv)

---

# 4. Docker Container

## 4.1 Docker Configuration

The Docker configuration follows the controlled container configuration specified in the laboratory manual.

| Parameter            | Configuration                                     |
| -------------------- | ------------------------------------------------- |
| Container Platform   | Docker                                            |
| CPU Limit            | 4 CPUs                                            |
| Memory Limit         | 8 GB                                              |
| Base Benchmark Image | Ubuntu 24.04                                      |
| Storage              | Dedicated benchmark directory / documented volume |
| Network              | Fixed documented network configuration            |

Explicit CPU and memory limits are used so that the container benchmark is performed under controlled resource conditions.

---

## 4.2 Docker Architecture

```text
                 HOST SYSTEM
                      │
                      ▼
             ┌─────────────────┐
             │ VMware          │
             │ Workstation     │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │   Ubuntu VM     │
             │                 │
             │   Docker Engine │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Docker          │
             │ Container       │
             │                 │
             │ 4 CPU Limit     │
             │ 8 GB Memory     │
             └────────┬────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
      CPU          Memory       Disk / Network
        │             │             │
        └─────────────┼─────────────┘
                      ▼
                FastAPI Workload
```

---

## 4.3 Docker Configuration Files

### Benchmark Image

[Docker Benchmark Dockerfile](docker/Dockerfile)

### FastAPI Application

[FastAPI Source](api/main.py)

[FastAPI Requirements](api/requirements.txt)

[FastAPI Dockerfile](api/Dockerfile)

---

## 4.4 Docker Execution Steps

### Step 1 — Build the Benchmark Image

```bash
docker build -t vm-container-benchmark -f docker/Dockerfile .
```

### Step 2 — Run the Controlled Container

```bash
docker run --rm \
    --cpus=4 \
    --memory=8g \
    vm-container-benchmark
```

### Step 3 — CPU Benchmark

```bash
docker run --rm \
    --cpus=4 \
    --memory=8g \
    vm-container-benchmark \
    sysbench cpu \
    --cpu-max-prime=20000 \
    --threads=4 \
    --time=30 \
    run
```

### Step 4 — Memory Benchmark

The same memory workload was executed inside the Docker environment.

### Step 5 — Disk Benchmark

The same:

```text
Sequential Read
Sequential Write
Random Read
Random Write
```

workloads were tested.

### Step 6 — Network Benchmark

```text
iperf3
iperf3_P4
```

### Step 7 — FastAPI Application

The FastAPI container was built and executed using:

```text
api/Dockerfile
api/main.py
api/requirements.txt
```

The service was exposed through port:

```text
8000
```

### Step 8 — Startup Test

Startup/application-ready time was measured over repeated runs.

### Step 9 — API Scalability

The API was evaluated at increasing workload levels.

### Step 10 — Store Results

Raw Docker benchmark results were preserved separately from VM results.

---

# 4.5 Docker Results

## CPU Performance

| Metric               |                 Docker |
| -------------------- | ---------------------: |
| Mean CPU Performance | **5552.60 events/sec** |

[Docker CPU Raw Results](results/raw/cpu/container/)
[CPU Processed Data](results/processed/cpu_results.csv)

---

## Memory Performance

| Metric                 |               Docker |
| ---------------------- | -------------------: |
| Mean Memory Throughput | **46467.34 MiB/sec** |

[Docker Memory Results](results/raw/memory/container/)
[Memory Processed Data](results/processed/memory_results.csv)

---

## Disk Performance

| Operation        |  Bandwidth |  IOPS |
| ---------------- | ---------: | ----: |
| Sequential Read  | 1334 MiB/s |  1334 |
| Sequential Write | 1704 MiB/s |  1703 |
| Random Read      | 46.0 MiB/s | 11800 |
| Random Write     | 33.7 MiB/s |  8632 |

[Docker Disk Results](results/raw/disk/container/)
[Disk Processed Data](results/processed/disk_results.csv)

---

## Network Performance

| Test        | Docker Throughput |
| ----------- | ----------------: |
| `iperf3`    |    82.0 Gbits/sec |
| `iperf3_P4` |     250 Gbits/sec |

[Docker Network Results](results/raw/network/container/)
[Network Processed Data](results/processed/network_results.csv)

---

## Application Performance

| Endpoint   | Requests/sec | Mean Latency |
| ---------- | -----------: | -----------: |
| `/health`  |      2496.18 |    40.061 ms |
| `/compute` |        30.84 |   324.281 ms |

[Docker Application Results](results/raw/application/container/)
[Application Processed Data](results/processed/application_results.csv)

---

## Startup Performance

| Metric            |     Docker |
| ----------------- | ---------: |
| Mean Startup Time | **635 ms** |

[Docker Startup Results](results/raw/startup/container/)
[Startup Processed Data](results/processed/startup_results.csv)

---

# 5. Performance Analysis of VM and Container

## 5.1 CPU Performance Comparison

| Environment | Mean Events/sec | Difference |
| ----------- | --------------: | ---------: |
| VM          |         5522.52 |          — |
| Docker      |         5552.60 | **+0.54%** |

Docker recorded a slightly higher mean CPU throughput in the measured dataset.

---

## 5.2 Memory Performance Comparison

| Environment |  Mean Throughput |
| ----------- | ---------------: |
| VM          | 66625.29 MiB/sec |
| Docker      | 46467.34 MiB/sec |

Measured difference:

**-30.26%**

---

## 5.3 Disk Performance Comparison

| Operation        |         VM |     Docker |  Difference |
| ---------------- | ---------: | ---------: | ----------: |
| Sequential Read  | 1134 MiB/s | 1334 MiB/s | **+17.64%** |
| Sequential Write |  864 MiB/s | 1704 MiB/s | **+97.22%** |
| Random Read      | 36.6 MiB/s | 46.0 MiB/s | **+25.68%** |
| Random Write     | 33.2 MiB/s | 33.7 MiB/s |  **+1.51%** |

---

## 5.4 Disk IOPS Comparison

| Operation        |   VM | Docker |  Difference |
| ---------------- | ---: | -----: | ----------: |
| Sequential Read  | 1134 |   1334 | **+17.64%** |
| Sequential Write |  864 |   1703 | **+97.11%** |
| Random Read      | 9372 |  11800 | **+25.91%** |
| Random Write     | 8489 |   8632 |  **+1.68%** |

---

## 5.5 Network Comparison

| Test        |             VM |         Docker | Difference |
| ----------- | -------------: | -------------: | ---------: |
| `iperf3`    | 84.3 Gbits/sec | 82.0 Gbits/sec | **-2.73%** |
| `iperf3_P4` |  259 Gbits/sec |  250 Gbits/sec | **-3.47%** |

---

## 5.6 Application Comparison

### Throughput

| Endpoint   |              VM |          Docker |  Difference |
| ---------- | --------------: | --------------: | ----------: |
| `/health`  | 2212.07 req/sec | 2496.18 req/sec | **+12.84%** |
| `/compute` |   34.94 req/sec |   30.84 req/sec | **-11.73%** |

### Latency

| Endpoint   |         VM |     Docker |  Difference |
| ---------- | ---------: | ---------: | ----------: |
| `/health`  |  45.206 ms |  40.061 ms | **-11.38%** |
| `/compute` | 286.199 ms | 324.281 ms | **+13.31%** |

---

## 5.7 Startup Comparison

| Environment | Mean Startup Time |
| ----------- | ----------------: |
| VM          |            350 ms |
| Docker      |            635 ms |

Measured difference:

**+81.43%**

---

# 6. CPU Scalability Analysis

CPU scalability was evaluated at 1, 2, 4, and 8 threads.

| Threads | VM Events/sec | Docker Events/sec | Difference |
| ------: | ------------: | ----------------: | ---------: |
|       1 |       1364.43 |           1341.14 |     -1.71% |
|       2 |       2804.14 |           2746.87 |     -2.04% |
|       4 |       5607.29 |           5459.08 |     -2.64% |
|       8 |       5611.58 |           5512.99 |     -1.76% |

[CPU Scalability Data](results/processed/cpu_scalability.csv)

---

# 7. API Scalability Analysis

The API was evaluated at increasing workload levels.

| Workload | Threads | Connections |
| -------: | ------: | ----------: |
|        1 |       1 |          10 |
|        2 |       2 |          50 |
|        4 |       4 |         100 |
|        8 |       4 |         200 |

## API Throughput

| Workload | VM Req/sec | Docker Req/sec |  Difference |
| -------: | ---------: | -------------: | ----------: |
|        1 |    2879.12 |        3317.02 | **+15.21%** |
|        2 |    3009.00 |        3897.71 | **+29.54%** |
|        4 |    3022.74 |        3760.39 | **+24.40%** |
|        8 |    2709.11 |        3341.97 | **+23.36%** |

## API Latency

| Workload |       VM |   Docker |  Difference |
| -------: | -------: | -------: | ----------: |
|        1 |  3.57 ms |  3.15 ms | **-11.76%** |
|        2 | 16.66 ms | 12.86 ms | **-22.81%** |
|        4 | 33.06 ms | 26.60 ms | **-19.54%** |
|        8 | 73.70 ms | 59.75 ms | **-18.93%** |

[API Scalability Data](results/processed/api_scalability.csv)

---

# 8. Performance Comparison Table

| Metric                |                 VM |   Docker Container |  Difference |
| --------------------- | -----------------: | -----------------: | ----------: |
| CPU Performance       | 5522.52 events/sec | 5552.60 events/sec |  **+0.54%** |
| Memory Throughput     |   66625.29 MiB/sec |   46467.34 MiB/sec | **-30.26%** |
| Sequential Read       |         1134 MiB/s |         1334 MiB/s | **+17.64%** |
| Sequential Write      |          864 MiB/s |         1704 MiB/s | **+97.22%** |
| Random Read           |         36.6 MiB/s |         46.0 MiB/s | **+25.68%** |
| Random Write          |         33.2 MiB/s |         33.7 MiB/s |  **+1.51%** |
| Network `iperf3`      |     84.3 Gbits/sec |     82.0 Gbits/sec |  **-2.73%** |
| Network `iperf3_P4`   |      259 Gbits/sec |      250 Gbits/sec |  **-3.47%** |
| `/health` Throughput  |    2212.07 req/sec |    2496.18 req/sec | **+12.84%** |
| `/compute` Throughput |      34.94 req/sec |      30.84 req/sec | **-11.73%** |
| `/health` Latency     |          45.206 ms |          40.061 ms | **-11.38%** |
| `/compute` Latency    |         286.199 ms |         324.281 ms | **+13.31%** |
| Startup Time          |             350 ms |             635 ms | **+81.43%** |

[Open Final Comparison CSV](results/processed/final_comparison.csv)

---

# 9. Performance Difference

For throughput metrics:

```text
Difference (%) =
((Docker - VM) / VM) × 100
```

### Interpretation

* **Positive percentage** → Docker measured a higher value.
* **Negative percentage** → Docker measured a lower value.

For latency and startup time, the numerical direction should be interpreted according to whether the measured time increased or decreased.

The comparison values are calculated from the processed experimental measurements.

---

# 10. Statistical Analysis

Repeated measurements were collected for the CPU, memory, and startup experiments.

The following statistical measures were calculated:

```text
Mean
Median
Minimum
Maximum
Standard Deviation
```

| Experiment | Environment |      Mean |    Median |   Minimum |   Maximum | Std. Deviation |
| ---------- | ----------- | --------: | --------: | --------: | --------: | -------------: |
| CPU        | VM          |   5522.52 |   5537.66 |   5392.76 |   5606.86 |          60.19 |
| CPU        | Docker      |   5552.60 |   5575.49 |   5367.42 |   5586.52 |          66.62 |
| Memory     | VM          |  66625.29 |  68408.41 |  49831.38 |  79238.95 |        9780.81 |
| Memory     | Docker      |  46467.34 |  42684.41 |  37089.00 |  76107.66 |       11982.66 |
| Startup    | VM          | 350.00 ms | 341.00 ms | 300.00 ms | 408.00 ms |          45.62 |
| Startup    | Docker      | 635.00 ms | 627.00 ms | 613.00 ms | 677.00 ms |          24.91 |

[Statistical Analysis CSV](results/processed/statistics.csv)

---

# 11. Graphical Analysis

All generated performance graphs are stored in `results/figures/`.

## CPU Performance

![CPU Performance](results/figures/01_cpu_performance.png)

[Open CPU Performance Graph](results/figures/01_cpu_performance.png)

---

## Memory Performance

![Memory Performance](results/figures/02_memory_performance.png)

[Open Memory Performance Graph](results/figures/02_memory_performance.png)

---

## Disk Bandwidth

![Disk Bandwidth](results/figures/03_disk_bandwidth.png)

[Open Disk Bandwidth Graph](results/figures/03_disk_bandwidth.png)

---

## Disk IOPS

![Disk IOPS](results/figures/04_disk_iops.png)

[Open Disk IOPS Graph](results/figures/04_disk_iops.png)

---

## Network Throughput

![Network Throughput](results/figures/05_network_throughput.png)

[Open Network Throughput Graph](results/figures/05_network_throughput.png)

---

## Application Throughput

![Application Throughput](results/figures/06_application_throughput.png)

[Open Application Throughput Graph](results/figures/06_application_throughput.png)

---

## Application Latency

![Application Latency](results/figures/07_application_latency.png)

[Open Application Latency Graph](results/figures/07_application_latency.png)

---

## Startup Time

![Startup Time](results/figures/08_startup_time.png)

[Open Startup Time Graph](results/figures/08_startup_time.png)

---

## CPU Scalability

![CPU Scalability](results/figures/09_cpu_scalability.png)

[Open CPU Scalability Graph](results/figures/09_cpu_scalability.png)

---

## API Scalability

![API Scalability](results/figures/10_api_scalability.png)

[Open API Scalability Graph](results/figures/10_api_scalability.png)

---

# 12. Overall Findings

The measured results show that performance varies according to workload type.

### CPU

The VM and Docker CPU results are very close, with Docker showing a **0.54% higher mean CPU throughput**.

### Memory

The memory measurements show a substantial difference between the two environments.

### Disk

The results vary considerably by I/O pattern. Docker records higher sequential-read, sequential-write, and random-read bandwidth, while random-write performance is nearly the same.

### Network

The VM records slightly higher throughput for both tested `iperf3` configurations.

### Application

Application performance depends on the endpoint. Docker records higher throughput for `/health`, while the VM records higher throughput for `/compute`.

### Startup

The measured mean startup time is lower for the VM.

### Scalability

The CPU scalability measurements remain relatively close between the two environments, while the API scalability experiment shows higher measured throughput for Docker across the tested workload levels.

---

# 13. Conclusion

This experiment provides a controlled comparison of a Virtual Machine and a Docker Container across multiple performance dimensions.

The results demonstrate that there is **no single environment that is universally better for every workload**.

CPU performance is closely matched, while noticeable differences appear in memory throughput, storage behavior, network throughput, application workloads, startup time, and API scalability.

The VM performs better in some measurements, while Docker performs better in others. The final conclusion therefore depends on the specific workload and performance requirement being considered.

The experiment demonstrates the importance of:

```text
Controlled Configuration
        ↓
Consistent Workloads
        ↓
Repeated Measurements
        ↓
Statistical Analysis
        ↓
Performance Comparison
```

---

# 14. Repository Structure

```text
Experiment2/
│
├── README.md
├── .gitignore
│
├── api/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── docker/
│   └── Dockerfile
│
├── docs/
│   ├── cpu-info.txt
│   ├── kernel-info.txt
│   ├── memory-info.txt
│   ├── storage-info.txt
│   ├── vm-configuration.txt
│   └── methodology.md
│
├── analysis/
│   ├── analysis.ipynb
│   ├── comparison_summary.md
│   ├── create_comparison.py
│   ├── generate_plots.py
│   └── process_results.py
│
├── results/
│   ├── raw/
│   │   ├── application/
│   │   ├── baseline/
│   │   ├── cpu/
│   │   ├── disk/
│   │   ├── memory/
│   │   ├── network/
│   │   ├── scalability/
│   │   └── startup/
│   │
│   ├── processed/
│   │   ├── api_scalability.csv
│   │   ├── application_results.csv
│   │   ├── cpu_results.csv
│   │   ├── cpu_scalability.csv
│   │   ├── disk_results.csv
│   │   ├── final_comparison.csv
│   │   ├── memory_results.csv
│   │   ├── network_results.csv
│   │   ├── startup_results.csv
│   │   └── statistics.csv
│   │
│   └── figures/
│       ├── 01_cpu_performance.png
│       ├── 02_memory_performance.png
│       ├── 03_disk_bandwidth.png
│       ├── 04_disk_iops.png
│       ├── 05_network_throughput.png
│       ├── 06_application_throughput.png
│       ├── 07_application_latency.png
│       ├── 08_startup_time.png
│       ├── 09_cpu_scalability.png
│       └── 10_api_scalability.png
│
└── scripts/
    └── run_cpu.sh
```

---

# 15. Reproduction and Analysis

From the project root:

### Process Results

```bash
python analysis/process_results.py
```

### Generate Comparison

```bash
python analysis/create_comparison.py
```

### Generate Graphs

```bash
python analysis/generate_plots.py
```

### Open the Jupyter Notebook

```bash
jupyter notebook
```

Then open:

```text
analysis/analysis.ipynb
```

The notebook performs the Python-based analysis of the processed benchmark results.

---

# 16. Result Files

### Raw Measurements

[Open Raw Benchmark Results](results/raw/)

### Processed Results

[Open Processed CSV Results](results/processed/)

### Statistical Results

[Open Statistics](results/processed/statistics.csv)

### Final Comparison

[Open Final Comparison](results/processed/final_comparison.csv)

### Performance Figures

[Open All Figures](results/figures/)

---

# 17. Author

## Zakiya Tahasildar

**Cloud Computing Lab — Experiment 2**

### Project

**Performance Analysis of Virtual Machines and Docker Containers**

---

> ## ⭐ Measure → Analyze → Compare → Conclude
>
> Performance conclusions in this project are derived from benchmark measurements, processed datasets, statistical analysis, and graphical comparison.
