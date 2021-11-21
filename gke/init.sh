#!/bin/bash

# create the cluster
gcloud container clusters create "cluster-gke-regional" \
  --region "europe-west3" \
  --machine-type "e2-standard-2" --disk-type "pd-standard" --disk-size "100" \
  --num-nodes "1" --node-locations "europe-west3-b","europe-west3-c"
# get the credentials
gcloud container clusters get-credentials cluster-gke-regional --region europe-west3
# create the pv, deploy postgres and service to gke
kubectl apply -f postgres-persistentvol.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
# Create image deployment
kubectl apply -f helloapp-deployments.yml



