FROM nginx:alpine
WORKDIR /usr/share/nginx/html

COPY static/upload.html index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
