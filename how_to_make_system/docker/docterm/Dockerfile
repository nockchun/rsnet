FROM alpine:latest
MAINTAINER RealStudy.NET <nockchun@gmail.com>

# Timezone
ENV TIMEZONE Asia/Seoul

# Install some tools in the container.
RUN apk update && apk upgrade\
    && apk add bind-tools curl wget nmap procps tcpdump busybox-extras mtr openssl nginx tzdata openssh-server openssh-client postgresql-client mysql-client rsync jq git iputils lftp netcat-openbsd socat iproute2 net-tools bash perl-net-telnet iperf3 ethtool apache2-utils nmap-ncat nmap-scripts \
    && cp /usr/share/zoneinfo/${TIMEZONE} /etc/localtime \
    && echo "${TIMEZONE}" > /etc/timezone \
    && mkdir /etc/nginx/certificates \
    && openssl req \
		-x509 \
		-newkey rsa:2048 \
		-keyout /etc/nginx/certificates/key.pem \
		-out /etc/nginx/certificates/cert.pem \
		-days 365 \
		-nodes \
		-subj /CN=localhost \
	&& mkdir /www \
	&& mkdir /var/run/nginx \
	&& apk del tzdata \
	&& rm -rf /var/cache/apk/*

COPY conf/nginx.conf /etc/nginx/nginx.conf
COPY conf/common.conf /etc/nginx/common.conf
COPY conf/conf.d/default.conf /etc/nginx/conf.d/default.conf
COPY conf/conf.d/ssl.conf /etc/nginx/conf.d/ssl.conf

# Expose volumes
VOLUME ["/etc/nginx", "/var/log/nginx", "/www"]

# Expose ports
EXPOSE 80 443

# Entry point
ENTRYPOINT ["/usr/sbin/nginx", "-g", "daemon off;"]