FROM ubuntu:20.04

COPY bin/etcd /usr/local/bin/etcd
COPY bin/etcdctl /usr/local/bin/etcdctl

RUN apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends iproute2 iptables \
    && rm -rf /var/lib/apt/lists/* \
    && chmod +x /usr/local/bin/etcd /usr/local/bin/etcdctl

EXPOSE 2379 2380
