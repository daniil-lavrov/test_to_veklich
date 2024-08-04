FROM nginx:latest

COPY default.conf /etc/nginx/nginx.conf

COPY create_cert.sh /usr/local/bin/create_cert.sh

RUN chmod +x /usr/local/bin/create_cert.sh && \
    /usr/local/bin/create_cert.sh

CMD ["nginx", "-g", "daemon off;"]
