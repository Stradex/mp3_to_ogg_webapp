#!/bin/bash
export SOPS_AGE_RECIPIENTS=$(<secrets/public-age-key.txt)
sops encrypt --age $SOPS_AGE_RECIPIENTS .env > .enc.env
