vm_provision
======

CLI for provisioning virtual machines in VMWare's vShpere

Docker image based off official Python image

https://hub.docker.com/_/python/

## How to Run

### Build image
```
docker build -t vm_provision .
```

### Run
```
docker run -it --rm --name vm_provision vm_provision:latest <PYTHON_SCRIPT.py> <-args>
```
