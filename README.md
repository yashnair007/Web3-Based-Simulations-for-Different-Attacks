# Web3-Based-Attack-Simulations-for-Different-Attacks

Honeypot Detector (Honeypot.py)
This Python script automates the process of checking whether a given Ethereum token contract is a honeypot (a scam where you can buy but not sell a token) by using the honeypot.is API.

✨ Features
Sends a request to the honeypot.is public API for each provided token address.

Parses and extracts important security information such as:

Whether the token is a honeypot or not

Risk level and risk score

Buy/Sell/Transfer tax rates

Gas fees for buying and selling

Open source status of the smart contract

Proxy contract detection

Liquidity available in the trading pair

Total number of holders

Displays a clean, readable risk report for each token.

Includes error handling for API failures and unexpected issues.

Includes debug logging to show raw API responses for troubleshooting.

📜 How It Works
A list of Ethereum token contract addresses is provided.

For each token address:

The script calls the Honeypot API.

It safely extracts key security metrics from the API response.

Based on honeypot status and risk score, it classifies the token as:

High Risk 🚨

Medium Risk ⚠️

Low Risk ✅

The detailed risk report is printed in the console.

Errors (such as timeouts or invalid responses) are gracefully handled.

📈 Output Example
🔍 Token Address: 0x8b9773e03e987BeD942d1F9695fE6895395ca386
📛 Name: ExampleToken (EXT)
🚨 WARNING: This is a Honeypot!
🔴 Risk Level: High Risk (Critical - 90/100)
📌 Honeypot Reason: Cannot sell
💰 Buy Tax: 10% | Sell Tax: 99% | Transfer Tax: 1%
⛽ Gas Fees - Buy: 120000 | Sell: 210000
📜 Open Source Contract: Yes
🔄 Proxy Contract: No | Proxy Calls: No
💧 Liquidity: 5000 USD
👥 Total Holders: 1234
