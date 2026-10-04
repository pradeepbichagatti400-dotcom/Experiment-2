#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUTPUT_DIR="$PROJECT_ROOT/results/raw/cpu"

mkdir -p "$OUTPUT_DIR"

for threads in 1 2 4 8
do
    echo "Running CPU test with $threads threads"

    sysbench cpu \
        --cpu-max-prime=20000 \
        --threads="$threads" \
        --time=30 \
        run > "$OUTPUT_DIR/cpu_${threads}_threads.txt"
done

echo "CPU benchmark completed."
