FROM ubuntu:20.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y unzip curl iproute2 iptables && rm -rf /var/lib/apt/lists/*
RUN curl -L https://releases.hashicorp.com/consul/1.18.2/consul_1.18.2_linux_amd64.zip -o consul.zip && \
    unzip consul.zip && \
    mv consul /usr/local/bin/ && \
    rm consul.zip
