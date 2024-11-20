# KURSACH
Запуска server.py -> click "http://127.0.0.1:5000"

# REQUIREMENTS
Python 3.11

# LINK
https://github.com/Sv163Sam/KURSACH.git

# NGINX MANUAL
brew update

brew apt install nginx

brew services start nginx 

brew services stop nginx

sudo nano /opt/homebrew/etc/nginx/sites-enabled/KURSACH.conf

/opt/homebrew/etc/nginx/sites-enabled/KURSACH.conf: 


server<br> 
{<br> 
<br> 
       listen 80;<br> 
       server_name localhost;<br> 
       root /absolute_path_to_project;<br>
       # Доступ к файлам статики (HTML, CSS, JS)<br> 
       location /static/ {<br> 
           alias /absolute_path_to_static/;<br> 
       }<br>
       location / {<br> 
           proxy_pass http://127.0.0.1:5000; <br> 
           proxy_set_header Host $host;<br> 
           proxy_set_header X-Real-IP $remote_addr;<br> 
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;<br> 
       }<br> 
}<br> 

