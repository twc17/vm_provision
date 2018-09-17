vm_provision
======

CLI for provisioning virtual machines in VMWare's vShpere

## How to Run

### Build image
```
docker build -t vm_provision .
```

### Run
```
docker run --rm --name vm_provision vm_provision:latest <PYTHON_SCRIPT.py> <-args>
```
