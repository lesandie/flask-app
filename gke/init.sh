#!/bin/bash

# create the cluster
gcloud container clusters create "hello-gke-regional" \
  --region "europe-west3" \
  --machine-type "e2-standard-2" --disk-type "pd-standard" --disk-size "100" \
  --num-nodes "1" --node-locations "europe-west3-b","europe-west3-c"
# get the credentials
gcloud container clusters get-credentials hello-gke-regional --region europe-west3
# create the pv, deploy postgres and service to gke
kubectl apply -f postgres-persistentvol.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
# Create image deployment
kubectl apply -f helloapp.yml
#kubectl create deployment hello-app --image=eu.gcr.io/encoded-mark-332220/helloapp
#kubectl scale deployment hello-app --replicas=2
#kubectl autoscale deployment hello-app --cpu-percent=80 --min=1 --max=5
#kubectl expose deployment hello-app --name=hello-app-service --type=LoadBalancer --port 80 --target-port 6000


