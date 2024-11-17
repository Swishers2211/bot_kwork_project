FROM nginx:latest

COPY ./nginx.conf /etc/nginx/nginx.conf

COPY ./frontend/build /usr/share/nginx/html
COPY ./backend/static /app_backend/static
COPY ./backend/media /app_backend/media

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
