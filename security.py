import requests
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# API Keys
INFURA_API_KEY = "5d419af494974b80a1d4579ac1109ee7"
ETHERSCAN_API_KEY = "E8VZXYAHZDM21WC5FX14UB75NUINQ98QJT"
TELEGRAM_TOKEN = "7680351723:AAGPtDTrYweEVhafH8wyCHJpFyMYnHaIYZc"

# Configure logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Function to check if a token is a honeypot
def check_honeypot(token_address):
    honeypot_api_url = f"https://api.honeypot.is/v2/IsHoneypot?address={token_address}&chain=eth"
    etherscan_api_url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={token_address}&apikey={ETHERSCAN_API_KEY}"
    
    try:
        response = requests.get(honeypot_api_url, timeout=10)
        response.raise_for_status()
        honeypot_data = response.json()

        response = requests.get(etherscan_api_url, timeout=10)
        response.raise_for_status()
        etherscan_data = response.json()

        is_honeypot = honeypot_data.get("honeypotResult", {}).get("isHoneypot", None)
        honeypot_reason = honeypot_data.get("honeypotResult", {}).get("honeypotReason", "Unknown")
        risk_level = honeypot_data.get("summary", {}).get("risk", "Unknown")
        buy_tax = honeypot_data.get("simulationResult", {}).get("buyTax", "N/A")
        sell_tax = honeypot_data.get("simulationResult", {}).get("sellTax", "N/A")
        total_holders = honeypot_data.get("token", {}).get("totalHolders", "N/A")
        token_name = honeypot_data.get("token", {}).get("name", "Unknown")
        token_symbol = honeypot_data.get("token", {}).get("symbol", "Unknown")
        contract_verified = bool(etherscan_data["result"]) and bool(etherscan_data["result"][0]["SourceCode"])
        
        locked_liquidity = "No evidence of liquidity lock. High risk!" if not honeypot_data.get("liquidity", {}).get("locked", False) else "Liquidity is locked."
        large_tx_detected = "Large transactions detected! Possible rug pull." if honeypot_data.get("summary", {}).get("largeTx", False) else "No unusual large transactions detected."
        dev_wallet_holding = honeypot_data.get("developer", {}).get("walletBalance", "N/A")
        mint_function_detected = "Yes" if honeypot_data.get("contract", {}).get("hasMintFunction", False) else "No"
        blacklist_function_detected = "Yes" if honeypot_data.get("contract", {}).get("hasBlacklistFunction", False) else "No"
        transfer_pause_detected = "Yes" if honeypot_data.get("contract", {}).get("canPauseTransfers", False) else "No"
        
        top_holders = honeypot_data.get("holders", [])[:5]
        holder_details = "\n".join([f"- {h['address']}: {h['balance']} tokens" for h in top_holders]) if top_holders else "No holder data available."
        
        # Normalize risk level values
        risk_mapping = {"low": "Low Risk 🟢", "medium": "Medium Risk 🟠", "high": "High Risk 🔴"}
        risk_status = risk_mapping.get(str(risk_level).lower(), "Unknown Risk")
        
        result = f"""
🔍 **Token Address:** `{token_address}`
📛 **Name:** {token_name} ({token_symbol})
📌 **Risk Level:** {risk_status}
📌 **Honeypot Reason:** {honeypot_reason}
💰 **Buy Tax:** {buy_tax}% | **Sell Tax:** {sell_tax}%
👥 **Total Holders:** {total_holders}
✅ **Contract Verified on Etherscan:** {'Yes' if contract_verified else 'No'}
🔒 **Liquidity Lock:** {locked_liquidity}
🚨 **Rug Pull Risk:** {large_tx_detected}
💼 **Developer Wallet Holding:** {dev_wallet_holding} ETH
⚠️ **Mint Function Present:** {mint_function_detected}
⚠️ **Blacklist Function Present:** {blacklist_function_detected}
⚠️ **Transfer Pause Ability:** {transfer_pause_detected}
🏦 **Top 5 Holders:**
{holder_details}
"""
        return result
    except requests.exceptions.RequestException as e:
        return f"❌ API Error: {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected Error: {str(e)}"

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("👋 Welcome! Send me a token address, and I'll check if it's a honeypot.")

async def check_token(update: Update, context: CallbackContext) -> None:
    token_address = update.message.text.strip()
    if len(token_address) != 42 or not token_address.startswith("0x"):
        await update.message.reply_text("⚠️ Invalid token address. Please send a valid Ethereum contract address.")
        return
    
    await update.message.reply_text("🔍 Checking token, please wait...")
    result = check_honeypot(token_address)
    await update.message.reply_text(result, parse_mode="Markdown")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_token))
    
    logging.info("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
