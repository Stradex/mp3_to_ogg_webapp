#!/bin/bash

terraform init
source .env
#terraform plan -var "do_token=$DO_TOKEN"
terraform apply -auto-approve -var "do_token=$DO_TOKEN" -var "spaces_access_id=$SPACES_KEY_ID" -var "spaces_access_key=$SPACES_KEY"
