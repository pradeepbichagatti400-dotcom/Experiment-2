# VM vs Container Performance Experiment — Methodology

## 1. Objective

The objective of this experiment is to compare the performance of an Ubuntu virtual machine and a Docker container under controlled resource conditions.

The comparison covers CPU performance, CPU scalability, memory performance, disk bandwidth and IOPS, network throughput, application throughput and latency, application startup time, and API scalability.

## 2. Experimental Environment

### Virtual Machine

The experiments were performed inside an Ubuntu VM running under VMware.

- vCPU: 4
- RAM: approximately 4.8 GiB
- Swap: 4 GiB

### Docker Container

The Docker benchmark container was executed with resource limits corresponding closely to the VM configuration.

- CPU limit: 4 CPUs
- Memory limit: 5101731840 bytes (~4.75 GiB)

## 3. Benchmark Workloads

### CPU

CPU performance was measured using Sysbench with 10 repeated runs.

The main CPU benchmark used 4 threads with a prime limit of 20000.

CPU scalability was evaluated using 1, 2, 4 and 8 threads.

### Memory

Memory throughput was measured using 10 repeated runs.

Because the VM had approximately 4.8 GiB RAM, the memory workload was intentionally limited to:

- Block size: 1 MiB
- Total size: 2 GiB
- Threads: 4

This adjustment was made to keep the workload appropriate for the available VM memory.

### Disk

Disk performance was evaluated using fio for:

- Sequential read
- Sequential write
- Random read
- Random write

Both bandwidth and IOPS were recorded.

### Network

Network throughput was measured using iperf3.

Two tests were collected:

- iperf3
- iperf3_P4

The measurements were obtained from the configured local test path and should therefore be interpreted as measurements of that virtual/local network configuration rather than general Internet throughput.

### Application

Application performance was measured using ApacheBench against:

- health
- compute

Requests per second and mean time per request were recorded.

### Application Startup

Application-ready time was measured over five runs for each environment.

### API Scalability

API scalability was evaluated using workload levels of 1, 2, 4 and 8.

Requests per second and average latency were recorded for each workload.

## 4. Data Processing

Raw benchmark outputs are stored under `results/raw/`.

The processing script `analysis/process_results.py` converts the raw outputs into structured CSV files under `results/processed/`.

Summary statistics were calculated for repeated CPU, memory and startup measurements.

The final comparison was generated using `analysis/create_comparison.py`.

## 5. Visualization

Ten figures were generated and stored under `results/figures/`.

The figures cover CPU, memory, disk, network, application performance, startup time, CPU scalability and API scalability.

## 6. Experimental Notes

The results represent the specific VMware and Docker configuration used in this experiment.

They should not be interpreted as universal performance characteristics of all VMs or containers.

The memory workload was intentionally limited to 2 GiB because of the available VM memory.

The network measurements were obtained from the configured local test path and should not be interpreted as Internet performance.
