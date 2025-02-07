# MP3 to OGG converter web app.

This is a basic audio converter web app.

## Services

This web app will use three services:

* Backend.
* Frontend.
* audio converter 

## BACKEND

* [NestJS](https://docs.nestjs.com/)
* [TypeScript](https://www.typescriptlang.org/docs/)
* [ioredis](https://www.npmjs.com/package/ioredis)

## FRONTEND

* [NextJS](https://nextjs.org/docs)

## CONVERTER

* [FastAPI](https://fastapi.tiangolo.com/)
* [FFMPEG](https://www.ffmpeg.org/)
* [FFMPEG Python](https://github.com/kkroening/ffmpeg-python)

## DEVOPS

### LOCAL

Build locally with docker-compose.yaml and using mkcert for HTTPs.

### REMOTE

Deploy to digital Ocean with:

* DigitalOcean Spaces [DONE]
* DigitalOcean Kubernetes [TODO]
* Terraform [WIP]
* Ansible [TODO]

[Redis with NESTJS](https://docs.nestjs.com/microservices/redis)

## IDEA:
* Backend upload file to bucket.
* File conversor pull files from bucket, convert them, and upload them again in the bucket.
* Backend stream files from bucket to frontend using websockets, redis, or something. (Or maybe backend just gives URL from S3 / Spaces bucket as response to frontend)
