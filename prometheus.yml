FROM prom/prometheus:v2.41.0
COPY prometheus.yml /etc/prometheus/prometheus.yml
EXPOSE 9090
CMD [ "/bin/prometheus", "--config.file=/etc/prometheus/prometheus.yml" ]
