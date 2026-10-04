# VM vs Container Performance Comparison

## Direct comparison

| Benchmark | Test | Metric | VM | Container | Container vs VM |
|---|---|---|---:|---:|---:|
| CPU | Average | Events/sec | 5522.52 | 5552.60 | +0.54% |
| Memory | Average | MiB/sec | 66625.29 | 46467.34 | -30.26% |
| Startup | Average | Milliseconds | 350.00 | 635.00 | +81.43% |
| Disk | seq-read | MiB/sec | 1134.00 | 1334.00 | +17.64% |
| Disk | seq-read | IOPS | 1134.00 | 1334.00 | +17.64% |
| Disk | seq-write | MiB/sec | 864.00 | 1704.00 | +97.22% |
| Disk | seq-write | IOPS | 864.00 | 1703.00 | +97.11% |
| Disk | random-read | MiB/sec | 36.60 | 46.00 | +25.68% |
| Disk | random-read | IOPS | 9372.00 | 11800.00 | +25.91% |
| Disk | random-write | MiB/sec | 33.20 | 33.70 | +1.51% |
| Disk | random-write | IOPS | 8489.00 | 8632.00 | +1.68% |
| Network | iperf3 | Gbits/sec | 84.30 | 82.00 | -2.73% |
| Network | iperf3_P4 | Gbits/sec | 259.00 | 250.00 | -3.47% |
| Application | health | Requests/sec | 2212.07 | 2496.18 | +12.84% |
| Application | health | Latency (ms) | 45.21 | 40.06 | -11.38% |
| Application | compute | Requests/sec | 34.94 | 30.84 | -11.73% |
| Application | compute | Latency (ms) | 286.20 | 324.28 | +13.31% |

## CPU scalability

| Threads | VM Events/sec | Container Events/sec | Container vs VM |
|---:|---:|---:|---:|
| 1 | 1364.43 | 1341.14 | -1.71% |
| 2 | 2804.14 | 2746.87 | -2.04% |
| 4 | 5607.29 | 5459.08 | -2.64% |
| 8 | 5611.58 | 5512.99 | -1.76% |

## API scalability

| Workload | VM Req/sec | Container Req/sec | Req/sec Change | VM Latency (ms) | Container Latency (ms) | Latency Change |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2879.12 | 3317.02 | +15.21% | 3.57 | 3.15 | -11.76% |
| 2 | 3009.00 | 3897.71 | +29.54% | 16.66 | 12.86 | -22.81% |
| 4 | 3022.74 | 3760.39 | +24.40% | 33.06 | 26.60 | -19.54% |
| 8 | 2709.11 | 3341.97 | +23.36% | 73.70 | 59.75 | -18.93% |
