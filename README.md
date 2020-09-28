# qsl-generator

## Running

Simple `docker-compose` example:

```yaml
version: '3'
services:
    qslgen:
        image: "docker.pkg.github.com/classabbyamp/qsl-generator/qsl-generator:latest"
        restart: always
```

Running outside of docker: install dependencies (python3.8 + requirements.txt), then `flask run`
