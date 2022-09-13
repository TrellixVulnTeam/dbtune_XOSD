FROM alpine:latest AS build_mysql
COPY ./mysql-8.0.30-linux-glibc2.17-x86_64-minimal.tar.xz /home/mysql.tar.xz
WORKDIR /home
RUN tar -xvf  mysql.tar.xz && \
    mv mysql-8.0.30-linux-glibc2.17-x86_64-minimal  /usr/local/mysql  &&  \
    chmod -R 755 /usr/local/mysql && \
    rm -rf mysql.tar.xz

FROM centos:centos8
LABEL TAG=v1.0

RUN sed -i -e "s|mirrorlist=|#mirrorlist=|g" /etc/yum.repos.d/CentOS-* && \
    sed -i -e "s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g" /etc/yum.repos.d/CentOS-* && \
    yum install -y python3 python3-setuptools python3-pip python36-devel \
    nc net-tools tar telnet java-1.8.0-openjdk make gcc  \
    python3-PyMySQL libaio-devel numactl-devel ncurses-compat-libs \
    --nogpgcheck  && \
    yum clean all

ENV DM_HOME=/opt/dmdbms
ENV PATH=/usr/local/mysql/bin:${PATH}
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DM_HOME/bin
ENV DJANGO_SETTINGS_MODULE=website.settings
ENV C_FORCE_ROOT=true
ENV LANG C.UTF-8


COPY --from=build_mysql /usr/local/mysql /usr/local/mysql

WORKDIR /home
COPY ./dmdbms /opt/dmdbms
COPY ./sysbench ./sysbench
COPY ./client  ./client
COPY ./server  ./server
WORKDIR ./server/website

COPY ./whl ./whl
COPY ./docker/credentials.py  ./website/settings/credentials.py
COPY ./docker/install.sh ./docker/start.sh  ./docker/wait-for-it.sh ./docker/check-celery.sh  ./

RUN echo "Asia/shanghai" > /etc/timezone && ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN chmod +x /opt/dmdbms/bin/* && chmod +x ./*.sh
#    ./install.sh

EXPOSE 8000 5555

ENTRYPOINT ["./start.sh"]
