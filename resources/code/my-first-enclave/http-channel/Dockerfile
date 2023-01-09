# // Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# // SPDX-License-Identifier: MIT-0

#vsock demo image
FROM public.ecr.aws/amazonlinux/amazonlinux:2 as socat-image

# Install python for running the server and net-tools for modifying network config
RUN yum groupinstall "Development Tools" -y

RUN curl http://www.dest-unreach.org/socat/download/socat-1.7.4.4.tar.gz --output socat-1.7.4.4.tar.gz
RUN tar -xvzf socat-1.7.4.4.tar.gz
WORKDIR /socat-1.7.4.4
RUN ./configure
RUN make 
RUN make install

# RUN ls /usr/local/bin && socat


FROM public.ecr.aws/amazonlinux/amazonlinux:2 as final

# Install python for running the server and net-tools for modifying network config
RUN yum install python3 iproute  -y

COPY --from=socat-image /usr/local/bin/ /usr/local/bin/

WORKDIR /app

COPY server.py ./
COPY run.sh ./

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]