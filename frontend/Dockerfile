FROM node:20.9-alpine as build-deps

ARG MODE
ARG VITE_BACKEND_URL
ARG VITE_FRONTEND_URL
ARG VITE_MSAL_CLIENT_ID
ARG VITE_MSAL_AUTHORITY

WORKDIR /usr/src/app
COPY package.json /usr/src/app/package.json
COPY yarn.lock /usr/src/app/yarn.lock
RUN yarn install
COPY . ./
RUN yarn run build --mode $MODE

FROM nginx:1.25-alpine
COPY --from=build-deps /usr/src/app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
