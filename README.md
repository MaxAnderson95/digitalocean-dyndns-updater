# DigitalOcean Dynamic DNS Updater
This is a Python script that determines your public egress IP address, then calls to the DigitalOcean API to either create or update a record with this IP.

This script is designed to run, perform the action, and then shutdown. It doesn't run as a daemon. The idea is to run this script (or ideally container image) on a system that allows for scheduling (such as a Kubernetes cron job).

## Configuration
To configure the script, set the following environment variables prior to execution:

|Name|Description|Required|Default|Example|
|---|---|---|---|---|
|DIGITALOCEAN_TOKEN|Must have read and write access|*true*||*N/A*|
|RECORD_NAME|The name of the DNS record to update|*true*||server01|
|ZONE_NAME|The name of the zone where the record should be created or updated|*true*||example.com|
|TTL|The time to live of the DNS record|*false*|3600|60|
|LOG_LEVEL|The log level of the script|*false*|INFO|DEBUG|

## Docker Image
A docker image which runs this script on startup has been published to the [DockerHub](https://hub.docker.com/repository/docker/maxanderson95/digitalocean-dyndns-updater).

## Run as a Kubernetes Cron Job
First create a secret that stores the DigitalOcean token
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: digitalocean-token
type: Opaque
data:
  token: <Base64 Encoded Token>
```
Then create a CronJob that runs the container image (for example) once per hour.
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: dyndns
spec:
  schedule: "0 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: dyndns-updater
            image: maxanderson95/digitalocean-dyndns-updater:latest
            imagePullPolicy: IfNotPresent
            env:
              - name: DIGITALOCEAN_TOKEN
                valueFrom:
                  secretKeyRef:
                    name: digitalocean-token
                    key: token
              - name: RECORD_NAME
                value: "server01"
              - name: ZONE_NAME
                value: "example.com"
          restartPolicy: OnFailure
```