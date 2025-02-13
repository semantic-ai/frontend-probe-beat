FROM node:22-alpine AS builder

ARG MODE=production

WORKDIR /usr/src/app

COPY package.json yarn.lock ./
RUN yarn install

COPY . .
RUN yarn run build --mode $MODE

FROM nginxinc/nginx-unprivileged:1.27-alpine

COPY --from=builder /usr/src/app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080
