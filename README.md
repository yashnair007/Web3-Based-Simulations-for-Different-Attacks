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



CODE 2  NFT

This Python script connects to the Ethereum mainnet via Infura and performs a comprehensive security analysis of a given transaction hash. It fetches detailed transaction, block, and receipt information using Web3.py and conducts a series of security checks relevant to smart contract interactions. The tool is useful for developers, auditors, and analysts to quickly assess the legitimacy and risk level of Ethereum transactions.

🔍 Features
✅ Transaction & Block Metadata: Extracts sender, receiver, gas details, block timestamp, miner, and more.

✅ Safe Address Verification: Checks whether the sender address is from a known whitelist.

✅ Contract Verification: Uses Etherscan API to validate whether the recipient is a verified smart contract.

✅ Replay Attack Detection: Flags suspiciously low nonce values.

✅ Gas Usage Analysis: Highlights transactions with unusually high gas consumption.

✅ MEV Bot Detection: Identifies potential arbitrage, sandwich, or frontrunning attacks based on input signatures.

✅ Flash Loan Detection: Flags interactions with known flash loan provider contracts like Aave, Compound, or 1inch.

✅ Token Approval Safety: Detects potentially risky unlimited token approvals in transaction data.

✅ Color-coded CLI Output: Presents findings in a structured and readable terminal interface using termcolor.


Requirements
web3

requests

termcolor

📌 Note
Replace YOUR_ETHERSCAN_API_KEY in the code with your valid Etherscan API key.

Make sure Infura endpoint and transaction hash are correctly configured.
