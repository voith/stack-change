#!/bin/bash

cd /root/stackXchange
source /root/stackXchange/venv/bin/activate

python -m contracts.contract_filter_listener
