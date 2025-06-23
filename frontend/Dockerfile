FROM node:18.12 as build-stage
WORKDIR /app

COPY . .

RUN npm install -g pnpm@8.15.1
RUN pnpm install

RUN pnpm run build

FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]


