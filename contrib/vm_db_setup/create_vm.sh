#!/bin/bash

set -e
set -x

#WORK_DIR=$(mktemp --tmpdir /tmp --directory vm-create-XXXXXXXXXX)
WORK_DIR=vm-create-HvZu281SXi

function cleanup() {
    rm -fr ${WORK_DIR}
}

# trap cleanup EXIT

# gcloud beta compute --project=covid19datapool instances create covid19dp-psql-01 --zone=us-central1-a --machine-type=f1-micro --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --service-account=servacc-covid19datapool@covid19datapool.iam.gserviceaccount.com --scopes=https://www.googleapis.com/auth/cloud-platform --image=debian-10-buster-v20200326 --image-project=debian-cloud --boot-disk-size=25GB --boot-disk-type=pd-standard --boot-disk-device-name=covid19dp-psql-01 --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any --format=json >${WORK_DIR}/vm-info.json

#gcloud compute --project=covid19datapool firewall-rules create default-allow-http --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:80 --source-ranges=0.0.0.0/0 --target-tags=http-server

# ???
#gcloud compute --project=covid19datapool firewall-rules create allow-psql --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:5432 --source-ranges=0.0.0.0/0 --target-tags=postgresql-server

IP_ADDR=$(jq -r '.[0].networkInterfaces[0].accessConfigs[0].natIP' ${WORK_DIR}/vm-info.json)

cat >hosts.yaml <<EOF
---
all:
  hosts:
    covid19dp:
      ansible_host: ${IP_ADDR}
EOF

# Create connector
# https://cloud.google.com/appengine/docs/standard/python3/connecting-vpc
