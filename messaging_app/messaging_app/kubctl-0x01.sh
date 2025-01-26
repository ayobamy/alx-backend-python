#!/bin/bash

kubectl scale deployment django-messaging-app --replicas=3

echo "Waiting for pods to be ready..."
kubectl rollout status deployment/django-messaging-app

echo "Current Pods:"
kubectl get pods

if ! command -v wrk &> /dev/null
then
    echo "Installing wrk..."
    sudo apt-get update
    sudo apt-get install -y wrk
fi

# Perform load testing
echo "Starting load test..."
wrk -t12 -c400 -d30s http://your-app-endpoint

echo "Checking resource usage:"
kubectl top pods
