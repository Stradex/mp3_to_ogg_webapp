#!/bin/bash
export SOPS_AGE_KEY_FILE="secrets/age-key.txt"
sops decrypt .enc.env > .env
