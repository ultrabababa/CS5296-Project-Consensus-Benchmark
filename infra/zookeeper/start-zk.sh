#!/bin/bash
mkdir -p /tmp/zookeeper
echo "${ZOO_MY_ID:-1}" > /tmp/zookeeper/myid
cat <<CFG > /opt/zookeeper/conf/zoo.cfg
tickTime=2000
dataDir=/tmp/zookeeper
clientPort=2181
initLimit=5
syncLimit=2
4lw.commands.whitelist=*
CFG

for server in $ZOO_SERVERS; do
  echo "$server" >> /opt/zookeeper/conf/zoo.cfg
done

exec /opt/zookeeper/bin/zkServer.sh start-foreground
