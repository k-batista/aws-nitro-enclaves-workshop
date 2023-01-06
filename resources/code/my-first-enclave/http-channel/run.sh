# // Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# // SPDX-License-Identifier: MIT-0

#!/bin/sh

# Assign an IP address to local loopback 
ip addr add 127.0.0.1/32 dev lo

ip link set dev lo up

# Enabling redirect through vsock
socat vsock-listen:9091,reuseaddr,fork tcp-connect:127.0.0.1:9090 &

# Run http server
python3 /app/http.py 0.0.0.0 9090
