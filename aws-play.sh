#!/bin/bash

# Get all access id's keys for all users 
# install `jq` for parsing json in bash before executing this script
# sudo apt install jq

users=$(aws iam list-users)
target_keys=($(echo "$users" | jq -r '.Users[].UserName'))


for key in "${target_keys[@]}"; do
    access_keys=$(aws iam list-access-keys --user-name "$key")
    echo "Access created keys for $key"
    echo "$access_keys"
    echo ""
done 
