# // Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# // SPDX-License-Identifier: MIT-0

#!/bin/sh

# Assign an IP address to local loopback
ip addr add 127.0.0.1/32 dev lo

ip link set dev lo up

# Add a hosts record, pointing target site calls to local loopback
echo "127.0.0.1   dummy.restapiexample.com" >> /etc/hosts

# Enabling redirect through vsock
socat vsock-listen:9091,reuseaddr,fork tcp-connect:127.0.0.1:9090 &
socat tcp4-listen:80,reuseaddr,fork vsock-connect:3:8001 &

# Run http server
python3 /app/server.py 0.0.0.0 9090