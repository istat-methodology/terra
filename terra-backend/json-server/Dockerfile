FROM node:18-alpine

ARG DOCKER_TAG
ARG NPM_REPO_URL

ENV APP_VERSION=${DOCKER_TAG}
ENV NPM_REPO_URL=${NPM_REPO_URL}

RUN echo "Bulding Docker image version: $APP_VERSION"

COPY . /app
WORKDIR /app

EXPOSE 5300

RUN npm install ${NPM_REPO_URL:+--registry=}${NPM_REPO_URL}
CMD ["node", "/app/server.js"]
