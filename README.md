# Aave Wallet Credit Scoring System

This project builds a credit scoring model for DeFi wallets interacting with the Aave V2 protocol. It analyzes historical transaction behavior and assigns each wallet a **credit score between 0 and 1000**, where higher scores indicate more responsible and reliable behavior.

## Goal

Develop a script to score DeFi wallets based solely on their on-chain interactions such as:

- Deposits
- Borrows
- Repayments
- Liquidations
- Redeems

## 📁 Project Structure

aave_credit_score/
├── data/
│ └── user-wallet-transactions.json # Input file
├── output/
│ ├── wallet_scores.json         # Output scores
│ ├── top_wallets.csv            # Top/bottom wallets
│ ├── wallet_score_chart.png     # Top/bottom graph
│ └── score_distribution.png     # Distribution graph
├── generate_scores.py           # Main scoring script
├── visualize_scores.py          # Analysis & export
├── README.md                    # This file
└── analysis.md                  # Score analysis

## Methodology

### ➤ Feature Engineering

From each transaction, we extract:

- `total_deposited` in USD
- `total_borrowed` in USD
- `total_repaid` in USD
- Number of actions (deposits, borrows, repayments)
- Number of liquidations
- Activity timestamps and wallet age

### ➤ Score Calculation

Each wallet is scored using the following formula:

credit_score = (deposit_score (20%) + borrow_score (20%) + repay_score(30%) + activity_score (10%) + wallet_age_score (20%) - liquidation_penalty)

All features are scaled and clipped into a score from 0–1000.

## How to Run

### 1. Install requirements

pip install numpy matplotlib

1. Generate scores
python generate_scores.py --input data/user-wallet-transactions.json --output output/wallet_scores.json

2. Visualize & export
python visualize_scores.py

📊 Output
wallet_scores.json: Score for each wallet
top_wallets.csv: Top 10 safest and riskiest wallets
wallet_score_chart.png: Bar chart comparing top/bottom wallets
score_distribution.png: Overall score distribution
