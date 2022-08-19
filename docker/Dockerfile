FROM centos:centos8
LABEL TAG=v1.0

RUN sed -i -e "s|mirrorlist=|#mirrorlist=|g" /etc/yum.repos.d/CentOS-* && \
    sed -i -e "s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g" /etc/yum.repos.d/CentOS-* && \
    yum install -y  nc  \
    net-tools \
    tar \
    telnet  \
    --nogpgcheck

ARG GRADLE_VERSION=gradle-7.4
ENV GRADLE_HOME=/home/${GRADLE_VERSION}
ENV DM_HOME=/opt/dmdbms
ENV PATH=${GRADLE_HOME}/bin:${DM_HOME}:${PATH}
ENV DJANGO_SETTINGS_MODULE=website.settings
ENV C_FORCE_ROOT=true
ENV LANG C.UTF-8

COPY ./dmdbms /opt/dmdbms
#COPY ./gradle-7.4 /home/
#COPY /root/.gradle ~/

RUN chmod +x /opt/dmdbms/bin/*

COPY ./client  /home/client
COPY ./server  /home/server
WORKDIR /home/server/website

COPY ./docker/credentials.py  ./
COPY ./docker/install.sh ./docker/start.sh  ./docker/wait-for-it.sh ./

#RUN ./install.sh && chmod +x ./*.sh
EXPOSE 8000 5555
#ENTRYPOINT ["./start.sh"]
CMD ["sleep","3600"]


