leadersofdigital_splavy_rosseti

# Запуск фронтенда
1. Скачать nginx
2. Закинуть всё из `frontend` в '/var/www/html' удалив стоковый index.html
3. В /etc/nginx/sites-available в файл default залить конфиг:
```
server {
 listen 80 default_server;
 listen [::]:80 default_server;


 root /var/www/html;

 # Add index.php to the list if you are using PHP
 index index.html index.htm index.nginx-debian.html;

 server_name _;

 location / {
  # First attempt to serve request as file, then
  # as directory, then fall back to displaying a 404.
  try_files $uri $uri/ =404;

        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Max-Age 3600;
        add_header Access-Control-Expose-Headers Content-Length;
        add_header Access-Control-Allow-Headers Range;
 }
}

```
