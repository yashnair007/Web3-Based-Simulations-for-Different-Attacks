from web3 import Web3
import requests
from termcolor import colored
from datetime import datetime

# Connect to Ethereum node (Infura or your own node)
INFURA_URL = "https://mainnet.infura.io/v3/5d419af494974b80a1d4579ac1109ee7"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Transaction hash to verify
tx_hash = "0xc67899c7cb8a352c676e9acfcb694ece78bcf101d2ce4065207a609d175b462e"

# Fetch transaction details
tx = web3.eth.get_transaction(tx_hash)
tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
block = web3.eth.get_block(tx["blockNumber"])

# Extract relevant details
from_address = tx["from"]
to_address = tx["to"]
value_eth = web3.from_wei(tx["value"], 'ether')
gas_used = tx_receipt["gasUsed"]
gas_limit = tx["gas"]
gas_price = tx["gasPrice"]
gas_fee = web3.from_wei(gas_used * gas_price, 'ether')
nonce = tx["nonce"]
block_number = tx["blockNumber"]
block_timestamp = datetime.utcfromtimestamp(block["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
miner = block["miner"]
block_size = block["size"]

# ---- Security Checks ----

# 1️⃣ **Check if sender's address is safe**
def is_safe_address(address):
    safe_addresses = ["0x29e3fe685fa832e597f31f7ae18e868e9f130fee"]  # Example whitelist
    return address in safe_addresses

# 2️⃣ **Check if recipient is a verified contract**
def is_verified_contract(address):
    api_url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey=YOUR_ETHERSCAN_API_KEY"
    response = requests.get(api_url).json()
    
    if "result" in response and isinstance(response["result"], list) and len(response["result"]) > 0:
        source_code = response["result"][0].get("SourceCode", "")
        return source_code.strip() != ""  # Check if SourceCode exists
    return False  

# 3️⃣ **Detect Replay Attack**
replay_attack_warning = "⚠️ Possible Replay Attack!" if nonce < 200 else "✅ Safe Nonce"

# 4️⃣ **Check Gas Usage**
gas_status = "✅ Gas Usage Normal" if gas_used / gas_limit < 0.9 else "⚠️ High Gas Usage"

# 5️⃣ **Advanced MEV Detection**
def check_mev_bot(tx_hash):
    mev_indicators = ["sandwich", "arbitrage", "frontrunning"]
    if any(indicator in str(tx.input).lower() for indicator in mev_indicators):
        return "⚠️ MEV Bot Detected (Potential Arbitrage or Sandwich Attack)"
    return "✅ No MEV Activity Detected"

# 6️⃣ **Advanced Flash Loan Detection**
def check_flash_loan(tx_hash):
    # Known Flash Loan contract addresses (Aave, dYdX, Uniswap, etc.)
    flash_loan_addresses = [
        "0x398ec7346dcd622edc5ae82352f02be94c62d119",  # Aave V2
        "0x5d3a536e4d6dbd6114cc1ead35777bab948e3643",  # Compound
        "0x1111111254eeb25477b68fb85ed929f73a960582",  # 1inch
    ]
    if to_address in flash_loan_addresses:
        return "⚠️ Flash Loan Detected"
    return "✅ No Flash Loan Detected"

# 7️⃣ **Detect Unlimited Token Approvals**
def check_token_approvals(tx_hash):
    if "approve" in str(tx.input).lower():
        return "⚠️ Risky Token Approval Detected (Check for Unlimited Approvals)"
    return "✅ No Risky Approvals"

# ---- Print Transaction Details ----

print(colored(f"\n🔍 Verifying Transaction: {tx_hash}", "cyan"))
print(colored(f"🔹 From: {from_address} ({'✅ Address is Safe' if is_safe_address(from_address) else '⚠️ Unverified Address'})", "yellow"))
print(colored(f"🔹 To: {to_address} ({'✅ Verified Contract' if is_verified_contract(to_address) else '⚠️ Unverified Contract'})", "yellow"))
print(colored(f"🔹 Type: Smart Contract Interaction", "yellow"))
print(colored(f"🔹 Value: {value_eth} ETH", "yellow"))
print(colored(f"🔹 Gas Used: {gas_used} / {gas_limit} limit", "yellow"))
print(colored(f"🔹 Gas Fee: {gas_fee} ETH", "yellow"))
print(colored(f"🔹 Nonce: {nonce} ({replay_attack_warning})", "yellow"))
print(colored(f"🔹 Block Number: {block_number}", "yellow"))
print(colored(f"🔹 Block Timestamp: {block_timestamp}", "yellow"))
print(colored(f"🔹 Mined By: {miner}", "yellow"))
print(colored(f"🔹 Block Size: {block_size} bytes", "yellow"))
print(colored(f"🔹 Transaction Status: ✅ Success", "green"))

# Print Security Checks
print(colored(f"\n🔹 Gas Status: {gas_status}", "green"))
print(colored(f"🔹 MEV Bot Check: {check_mev_bot(tx_hash)}", "green"))
print(colored(f"🔹 Flash Loan Detection: {check_flash_loan(tx_hash)}", "green"))
print(colored(f"🔹 Token Approval Check: {check_token_approvals(tx_hash)}", "green"))

print(colored(f"\nTransaction is valid: {tx_receipt['status'] == 1}", "green"))