FROM node:18-alpine

ARG DOCKER_TAG
ENV APP_VERSION=$DOCKER_TAG
RUN echo "Bulding Docker image version: $APP_VERSION"

COPY . /app
WORKDIR /app

EXPOSE 5300

RUN npm install
CMD ["node", "/app/server.js"]
