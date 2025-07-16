import json
import os
import argparse
from datetime import datetime
from collections import defaultdict
import numpy as np

# Helper to parse timestamps
def parse_timestamp(ts):
    try:
        return datetime.fromtimestamp(int(ts))
    except:
        return None

# Feature extraction function
def extract_features(transactions):
    features = defaultdict(lambda: {
        "num_deposits": 0,
        "total_deposited": 0,
        "num_borrows": 0,
        "total_borrowed": 0,
        "num_repayments": 0,
        "total_repaid": 0,
        "num_liquidations": 0,
        "timestamps": []
    })

    for tx in transactions:
        user = tx.get("userWallet")
        action = tx.get("action", "").lower()
        timestamp = parse_timestamp(tx.get("timestamp"))

        if not user or not timestamp:
            continue

        features[user]["timestamps"].append(timestamp)

        # Nested actionData
        action_data = tx.get("actionData", {})
        raw_amount = action_data.get("amount")
        price_usd = action_data.get("assetPriceUSD")

        try:
            # Convert raw token amount × USD price = value in USD
            amount = float(raw_amount) * float(price_usd)
        except:
            amount = 0

        if action == 'deposit':
            features[user]["num_deposits"] += 1
            features[user]["total_deposited"] += amount
        elif action == 'borrow':
            features[user]["num_borrows"] += 1
            features[user]["total_borrowed"] += amount
        elif action == 'repay':
            features[user]["num_repayments"] += 1
            features[user]["total_repaid"] += amount
        elif action == 'liquidationcall':
            features[user]["num_liquidations"] += 1

    return features

# Scoring logic
def compute_score(features):
    scores = {}
    for wallet, f in features.items():
        deposit_score = min(f["total_deposited"] / 1000, 1.0) * 200
        borrow_score = (1 - min(f["total_borrowed"] / max(f["total_deposited"], 1), 1.0)) * 200
        repay_ratio = min(f["total_repaid"] / max(f["total_borrowed"], 1), 1.0)
        repay_score = repay_ratio * 300
        liquidation_penalty = f["num_liquidations"] * 50
        activity = len(f["timestamps"])
        activity_score = min(activity / 50, 1.0) * 100

        # Wallet age feature
        if len(f["timestamps"]) > 1:
            time_span = (max(f["timestamps"]) - min(f["timestamps"])).days + 1
        else:
            time_span = 1
        age_score = min(time_span / 180, 1.0) * 200

        final_score = (
            deposit_score +
            borrow_score +
            repay_score +
            activity_score +
            age_score -
            liquidation_penalty
        )

        scores[wallet] = int(np.clip(final_score, 0, 1000))

    return scores

# Main function
def main(input_file, output_file):
    print("Loading transaction data...")
    with open(input_file, 'r') as f:
        transactions = json.load(f)

    print("Extracting features...")
    features = extract_features(transactions)

    print("Computing scores...")
    scores = compute_score(features)

    print("Saving results...")
    results = [{"wallet": k, "credit_score": v} for k, v in scores.items()]
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"✅ Done! Scores saved to: {output_file}")

# Entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aave V2 Wallet Credit Scoring")
    parser.add_argument("--input", type=str, required=True, help="Path to input JSON file")
    parser.add_argument("--output", type=str, default="output/wallet_scores.json", help="Path to output file")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    main(args.input, args.output)
