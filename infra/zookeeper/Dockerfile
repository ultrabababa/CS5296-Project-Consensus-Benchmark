FROM ubuntu:20.04
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y default-jre-headless curl iproute2 iptables netcat && rm -rf /var/lib/apt/lists/*
RUN curl -L https://archive.apache.org/dist/zookeeper/zookeeper-3.9.2/apache-zookeeper-3.9.2-bin.tar.gz -o zk.tar.gz && \
    tar xzf zk.tar.gz && \
    mv apache-zookeeper-3.9.2-bin /opt/zookeeper && \
    rm zk.tar.gz
COPY start-zk.sh /opt/zookeeper/bin/start-zk.sh
RUN chmod +x /opt/zookeeper/bin/start-zk.sh
CMD ["/opt/zookeeper/bin/start-zk.sh"]
