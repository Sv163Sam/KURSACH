# KURSACH

Python 3.11

https://github.com/Sv163Sam/KURSACH.git

brew update

brew apt install nginx

brew services start nginx 

brew services stop nginx

sudo nano /opt/homebrew/etc/nginx/sites-enabled/KURSACH.conf

/opt/homebrew/etc/nginx/sites-enabled/KURSACH.conf: 


server 
{

       listen 80; 
       
       server_name localhost;
       
       root /absolute_path_to_project; 

       # Доступ к файлам статики (HTML, CSS, JS)
       location /static/ {
           alias /absolute_path_to_static/;
       }

       location / {
           proxy_pass http://127.0.0.1:5000; 
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }

