FROM python:3.12

ARG DOCKER_TAG
ENV APP_VERSION=$DOCKER_TAG
EXPOSE 5500
RUN echo "Bulding Docker image version: $APP_VERSION"

RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN echo 'deb [arch=amd64,arm64,armhf] https://packages.microsoft.com/debian/12/prod bookworm main' | tee /etc/apt/sources.list.d/mssql-release.list

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive ACCEPT_EULA=Y apt install -y msodbcsql18 mssql-tools18 unixodbc-dev libgssapi-krb5-2

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
 