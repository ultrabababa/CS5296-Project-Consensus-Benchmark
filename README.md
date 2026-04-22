# Consensus Benchmark Lab

Local-first benchmark lab for consensus systems.

Current scope:
- etcd 3-node cluster on Docker Compose
- ZooKeeper 3-node cluster on Docker Compose
- Consul 3-node cluster on Docker Compose
- Baseline workload (80% write / 20% read)
- Fault injection scenarios (leader kill, delay, loss, partition, majority crash, majority partition)
- STABL-style sensitivity analysis and figure generation (eCDF area + radar)

## Quick Start

```bash
./scripts/pipeline/run_etcd_full.sh
```

Run all systems:

```bash
./scripts/pipeline/run_all_full.sh
```

Artifacts are written to `results/etcd/`, `results/zookeeper/`, `results/consul/`.

Figure-ready artifacts are written to `results/figures/`, including:
- `<system>_fig1_ecdf_leader_kill.png`
- `<system>_fig2_radar.png`
- `all_systems_fig2_radar.png` (Unified radar plot combining all systems)
