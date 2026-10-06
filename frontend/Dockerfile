FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

ARG VITE_API_URL=""
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:1.27-alpine

WORKDIR /usr/share/nginx/html

COPY --from=build /app/dist ./
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

ENV PORT=80
ENV API_PROXY_TARGET=http://127.0.0.1:8000

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
