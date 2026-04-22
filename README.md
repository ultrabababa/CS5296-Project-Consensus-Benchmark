# Consensus Benchmark Lab

A reproducible, local-first and cloud-ready benchmarking suite for evaluating the robustness of distributed consensus systems (etcd, ZooKeeper, Consul) under stress.

This project adapts the **STABL Sensitivity Metric** to traditional consensus protocols, generating rigorous distribution-level comparisons under injected cloud network failures (e.g., delays, partitions, process crashes).

## Key Features

- **Multi-System Support**: `etcd` (v3.5), `ZooKeeper` (v3.9), and `Consul` (v1.18) implemented as 3-node clusters.
- **Deterministic Workload**: Python-based load generators interacting directly with native APIs (80% write / 20% read).
- **Chaos Engineering**: Automated fault injection using Linux `tc netem` and `iptables` running entirely inside Docker network namespaces. Supported scenarios include:
  - `leader_kill`
  - `delay_120ms`
  - `loss_8pct`
  - `partition`
  - `majority_crash`
  - `majority_partition`
- **STABL Sensitivity Analysis**: Automated aggregation of empirical Cumulative Distribution Functions (eCDFs) and absolute area difference calculations.
- **Report Generation**: Produces pure JSON reports, eCDF visualization plots, and unified logarithmic radar charts for academic reporting.

## Prerequisites

- **OS**: Linux (Ubuntu 22.04/24.04 recommended) or WSL2.
- **Dependencies**: Docker Engine, Docker Compose, Python 3.10+.

To initialize a raw Ubuntu/EC2 environment with all prerequisites, run:
```bash
./scripts/pipeline/setup_ec2.sh
```

## Repository Structure

```
consensus-benchmark-lab/
├── analysis/               # STABL sensitivity metric logic and plotting (figures.py, multi_system_radar.py)
├── aws-results/
│   ├── awd-results/        # Running results for AWS EC2 Environment
├── infra/                  # Docker Compose files and Dockerfiles for etcd, ZooKeeper, Consul
├── scripts/                # Automated experiment runner scripts
│   ├── cluster/            # Etcd cluster control (up, down, health)
│   ├── consul/             # Consul-specific cluster, fault, and workload runners
│   ├── fault/              # Etcd fault injection scripts (tc netem, iptables, docker stop)
│   ├── pipeline/           # Full end-to-end runners (run_all_full.sh, setup_ec2.sh)
│   ├── workload/           # Python load generators for etcd, ZooKeeper, Consul
│   └── zookeeper/          # ZooKeeper-specific cluster, fault, and workload runners
└── tests/                  # Unit tests for metric extraction and figure rendering
```

## Quick Start

### 1. Build Local Images
Due to the need for advanced network manipulation (`tc`, `iptables`) inside containers, we use custom Dockerfiles based on official binaries. Build them first:
```bash
docker build -t local/zookeeper-lab:3.9 infra/zookeeper
docker build -t local/consul-lab:1.18 infra/consul
```

### 2. Run the Full Pipeline
You can run an end-to-end benchmark for all systems. This automatically spins up clusters, runs baselines, injects faults, collects latencies, calculates the sensitivity metric, and generates the final plots:

```bash
./scripts/pipeline/run_all_full.sh
```

Or run a specific system individually:
```bash
./scripts/pipeline/run_etcd_full.sh
./scripts/pipeline/run_zookeeper_full.sh
./scripts/pipeline/run_consul_full.sh
```

## Outputs

All artifacts are deterministically written to the `results/` directory.

- **Raw Data**: `results/<system>/baseline/run_*.json` and `results/<system>/fault/<scenario>/run_*.json`
- **Computed Reports**: `results/<system>/report_<scenario>.json`
- **Visualizations** (`results/figures/`):
  - `<system>_fig1_ecdf_leader_kill.png` (Example STABL eCDF area plot)
  - `<system>_fig2_radar.png` (Radar plot per system)
  - `all_systems_fig2_radar.png` (Unified cross-system sensitivity radar plot)
  - Data CSVs backing all generated figures.

