# BioMANIA-Server

This repository contains the FastAPI app to provide a RESTful API for
[BioMANIA-backend](https://github.com/OSU-BMBL/BioMANIA-backend). It is used in the
[BioMANIA-Next](https://github.com/OSU-BMBL/BioMANIA-Next) web application.

## Installation

## Local Build

You can also run the following code to build and start the server locally:

```console
docker build -t biomania-server .
docker run -p 5001:5001 -d biomania-server
```

## API docs

API docs are work in progress. Use swagger to explore the API by opening the
server's `/docs` URI. For example, for localhost it will be:
```
http://0.0.0.0:5001/docs
```

## Developer

We build the Docker image using the following command to account for ARM and
AMD64 architectures:

```console
docker buildx build --tag biocypher/biochatter-server:latest --tag biocypher/biochatter-server:<version> --platform linux/amd64,linux/arm64 --push .
```

The version on Dockerhub should match the version in the `pyproject.toml` file.
