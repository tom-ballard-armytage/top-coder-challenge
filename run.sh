#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 trip_duration_days miles_traveled total_receipts_amount"
    exit 1
fi

python3 calculate_reimbursement.py "$1" "$2" "$3" 
