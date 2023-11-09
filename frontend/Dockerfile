FROM node:20.9-alpine as build-deps

ARG MODE=production

WORKDIR /usr/src/app
COPY package.json /usr/src/app/package.json
COPY yarn.lock /usr/src/app/yarn.lock
RUN yarn install
COPY . ./
RUN yarn run build --mode $MODE

FROM nginxinc/nginx-unprivileged:1.25-alpine
COPY --from=build-deps --chown=101:101 /usr/src/app/dist /usr/share/nginx/html
USER root
RUN chown 101:101 /usr/share/nginx/html
USER 101
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080

CMD ["/bin/sh",  "-c",  "envsubst < /usr/share/nginx/html/env.template.js > /usr/share/nginx/html/env.js && exec nginx -g 'daemon off;'"]