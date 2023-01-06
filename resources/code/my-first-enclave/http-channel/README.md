
# Enclave Examples 

## Setup EC2

> Reference: https://docs.aws.amazon.com/enclaves/latest/user/nitro-enclave-cli-install.html

### Install nitro enclave 
```
sudo amazon-linux-extras install aws-nitro-enclaves-cli -y
sudo yum install aws-nitro-enclaves-cli-devel -y
```

Install socat on the client
```
sudo yum groupinstall "Development Tools" -y
curl http://www.dest-unreach.org/socat/download/socat-1.7.4.4.tar.gz --output socat-1.7.4.4.tar.gz
tar -xvzf socat-1.7.4.4.tar.gz
cd socat-1.7.4.4
./configure
make 
sudo make install
cd ..
```

### Config Nitro Enclave Allocator:  CPU and Memory 

It is necessary to increase the memory of the allocator

```
sudo vi /etc/nitro_enclaves/allocator.yaml
```

/etc/nitro_enclaves/allocator.yaml
``` 
memory_mib: 4096
cpu_count: 2
```


### Enable nitro enclave and docker
```
sudo systemctl start nitro-enclaves-allocator.service && sudo systemctl enable nitro-enclaves-allocator.service
sudo systemctl start docker && sudo systemctl enable docker
```


---
## Example: Http Channel
> Reference : https://nitro-enclaves.workshop.aws/en/my-first-enclave/secure-local-channel.html

### 1. Download Example
```
curl https://codeload.github.com/k-batista/aws-nitro-enclaves-workshop/zip/refs/heads/http --output main.zip
unzip main.zip -d example
cd example/aws-nitro-enclaves-workshop-http/resources/code/my-first-enclave/http-channel/
```

### 2. Build enclave image

> On the server, the communication via vsock will be activated
> 
> `socat vsock-listen:9091,reuseaddr,fork tcp-connect:127.0.0.1:9090 &`

```
sudo docker build ./ -t http-example
sudo nitro-cli build-enclave --docker-uri http-example:latest --output-file http-example.eif
```

### 3. Running the enclave - server
```
sudo nitro-cli run-enclave --cpu-count 2 --memory 4096 --enclave-cid 17 --eif-path http-example.eif --debug-mode
```

### 4. Enable de Vsock proxy

```
echo "allowlist:" >> vsock-proxy.yaml
echo "- {address: polygon.shekel.com, port: 80}" >> vsock-proxy.yaml
vsock-proxy 8001 dummy.restapiexample.com 80 --config vsock-proxy.yaml &
```

### 5. Running the client

Enable the communication via vsock
```
socat tcp4-listen:9090,reuseaddr,fork vsock-connect:17:9091 &
```

Testing using curl
```
curl http://localhost:9090
```

### See the logs
```
nitro-cli console --enclave-name http-example
```

---
## Helpers 

### Config Nitro Enclave Allocator:  CPU and Memory 
```
sudo vi /etc/nitro_enclaves/allocator.yaml
```

### Nitro-cli Commands 
```
sudo nitro-cli console --enclave-name ${ENCLAVE_NAME}
sudo nitro-cli console --enclave-id ${ENCLAVE_ID}
sudo nitro-cli describe-enclaves
sudo nitro-cli terminate-enclave --all
```

### Troubleshooting

```
sudo systemctl restart nitro-enclaves-allocator.service
systemctl status nitro-enclaves-allocator.service

cat /var/log/nitro_enclaves/nitro_enclaves.log
```


