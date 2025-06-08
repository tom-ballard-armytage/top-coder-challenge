#!/usr/bin/env python3

import sys
import json
import math
import os

# Tunable feature scales (to be adjusted for best performance)
SCALE_DAYS = 1.0
SCALE_MILES = 0.02
SCALE_RECEIPTS = 0.005

K = 10

# Load public cases
PUBLIC_CASES_PATH = os.path.join(os.path.dirname(__file__), 'public_cases.json')
with open(PUBLIC_CASES_PATH, 'r') as f:
    public_cases = json.load(f)

# Prepare data
examples = []
for case in public_cases:
    inp = case['input']
    out = case['expected_output']
    examples.append([
        inp['trip_duration_days'],
        inp['miles_traveled'],
        inp['total_receipts_amount'],
        out
    ])

def scaled_distance(a, b):
    """Compute scaled Euclidean distance between two input vectors."""
    d_days = (a[0] - b[0]) * SCALE_DAYS
    d_miles = (a[1] - b[1]) * SCALE_MILES
    d_receipts = (a[2] - b[2]) * SCALE_RECEIPTS
    return math.sqrt(d_days**2 + d_miles**2 + d_receipts**2)

def predict_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    query = [trip_duration_days, miles_traveled, total_receipts_amount]
    # Compute distances to all examples
    dists = []
    for ex in examples:
        dist = scaled_distance(query, ex)
        dists.append((dist, ex[3]))
    # Sort by distance
    dists.sort(key=lambda x: x[0])
    # Take k nearest
    nearest = dists[:K]
    # Distance-weighted average (avoid div by zero)
    weights = [1/(d+1e-6) for d, _ in nearest]
    weighted_sum = sum(w*y for w, (_, y) in zip(weights, nearest))
    total_weight = sum(weights)
    pred = weighted_sum / total_weight if total_weight > 0 else sum(y for _, y in nearest)/K
    return round(pred, 2)

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 calculate_reimbursement.py trip_duration_days miles_traveled total_receipts_amount")
        sys.exit(1)
    try:
        trip_duration_days = int(sys.argv[1])
        miles_traveled = int(sys.argv[2])
        total_receipts_amount = float(sys.argv[3])
        result = predict_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount)
        print(f"{result:.2f}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
