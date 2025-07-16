import json
import matplotlib.pyplot as plt
import csv

# ✅ Replace this with your actual path (use double backslashes or forward slashes)
file_path = "C:/Users/tanushree hiremath/OneDrive/Desktop/aave_credit_score/output/wallet_scores.json"

# Load wallet scores
with open(file_path, "r") as f:
    score_data = json.load(f)

# Sort by score
sorted_wallets = sorted(score_data, key=lambda x: x["credit_score"], reverse=True)

# Top 10 safest
top_10_safest = sorted_wallets[:10]
safe_wallets = [entry["wallet"][:10] + "..." for entry in top_10_safest]
safe_scores = [entry["credit_score"] for entry in top_10_safest]

# Top 10 riskiest
top_10_riskiest = sorted_wallets[-10:]
risky_wallets = [entry["wallet"][:10] + "..." for entry in top_10_riskiest]
risky_scores = [entry["credit_score"] for entry in top_10_riskiest]

# 🔢 Save to CSV
csv_path = "C:/Users/tanushree hiremath/OneDrive/Desktop/aave_credit_score/output/top_wallets.csv"
with open(csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Type", "Wallet", "Credit Score"])
    for entry in top_10_safest:
        writer.writerow(["Safest", entry["wallet"], entry["credit_score"]])
    for entry in top_10_riskiest:
        writer.writerow(["Riskiest", entry["wallet"], entry["credit_score"]])

print(f"✅ CSV saved to: {csv_path}")

# 📊 Plot both in subplots
fig, axs = plt.subplots(2, 1, figsize=(12, 10))
fig.suptitle('Top 10 Safest vs Riskiest Wallets (Credit Scores)', fontsize=16)

# Safest
axs[0].barh(safe_wallets[::-1], safe_scores[::-1], color='green')
axs[0].set_title("Top 10 Safest Wallets")
axs[0].set_xlabel("Credit Score")
axs[0].set_xlim(0, 1000)

# Riskiest
axs[1].barh(risky_wallets, risky_scores, color='red')
axs[1].set_title("Top 10 Riskiest Wallets")
axs[1].set_xlabel("Credit Score")
axs[1].set_xlim(0, 1000)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# 💾 Save the plot as a PNG file
plot_path = "C:/Users/tanushree hiremath/OneDrive/Desktop/aave_credit_score/output/wallet_score_chart.png"
plt.savefig(plot_path)
print(f"✅ Chart image saved to: {plot_path}")

# Optionally also show it
plt.show()
