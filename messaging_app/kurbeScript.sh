#!/bin/bash

# Ensure script is run with sudo
if [ "$EUID" -ne 0 ]
then
    echo "Please run as root or with sudo"
    exit
fi

apt-get update && apt-get upgrade -y

apt-get install -y curl wget software-properties-common apt-transport-https

if ! command -v minikube &> /dev/null
then
    wget https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    chmod +x minikube-linux-amd64
    mv minikube-linux-amd64 /usr/local/bin/minikube
fi

if ! command -v kubectl &> /dev/null
then
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    mv kubectl /usr/local/bin/kubectl
fi

minikube start --driver=docker

minikube kubectl -- get po -A

echo "Cluster Information:"
kubectl cluster-info

# List all pods
echo "Listing all pods:"
kubectl get pods --all-namespaces
