#!/bin/bash

kubectl apply -f blue_deployment.yaml

kubectl rollout status deployment/django-messaging-app-blue

kubectl port-forward service/django-service 8080:80 &
FORWARD_PID=$!

while true; do
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080)
    if [ $response -ne 200 ]; then
        echo "Potential downtime detected! Status code: $response"
    else
        echo "App responding normally. Status code: $response"
    fi
    sleep 1
done

kill $FORWARD_PID

# Verify current pods
kubectl get pods
