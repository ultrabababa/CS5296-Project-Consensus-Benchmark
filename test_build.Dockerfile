FROM ubuntu:20.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y unzip curl iproute2 iptables && rm -rf /var/lib/apt/lists/*
