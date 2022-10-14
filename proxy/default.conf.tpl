server {
    listen ${LISTEN_PORT};
    location /media {
        alias /vol/web/media;
    }
    location /static {
        alias /vol/web/static;
    }
    location / {
        uwsgi_pass            ${APP_HOST}:${APP_PORT};
        include               /etc/nginx/uwsgi_params;
        client_max_body_size  10M;
    }
}