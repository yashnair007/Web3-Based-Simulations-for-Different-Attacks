import requests
import json

def check_honeypot(token_address):
    api_url = f"https://api.honeypot.is/v2/IsHoneypot?address={token_address}&chain=eth"

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Debugging: Log the raw API response
        print(f"\n[DEBUG] Raw API Response for {token_address}:\n", json.dumps(data, indent=4))

        # Extract key fields safely
        is_honeypot = data.get("honeypotResult", {}).get("isHoneypot", None)
        honeypot_reason = data.get("honeypotResult", {}).get("honeypotReason", "Unknown")
        simulation_success = data.get("simulationSuccess", None)
        risk_level = data.get("summary", {}).get("risk", "Unknown")
        risk_score = data.get("summary", {}).get("riskLevel", "N/A")
        buy_tax = data.get("simulationResult", {}).get("buyTax", "N/A")
        sell_tax = data.get("simulationResult", {}).get("sellTax", "N/A")
        transfer_tax = data.get("simulationResult", {}).get("transferTax", "N/A")
        buy_gas = data.get("simulationResult", {}).get("buyGas", "N/A")
        sell_gas = data.get("simulationResult", {}).get("sellGas", "N/A")
        open_source = data.get("contractCode", {}).get("openSource", False)
        is_proxy = data.get("contractCode", {}).get("isProxy", False)
        has_proxy_calls = data.get("contractCode", {}).get("hasProxyCalls", False)
        liquidity = data.get("pair", {}).get("liquidity", "N/A")
        total_holders = data.get("token", {}).get("totalHolders", "N/A")
        token_name = data.get("token", {}).get("name", "Unknown")
        token_symbol = data.get("token", {}).get("symbol", "Unknown")

        # Risk classification
        if is_honeypot:
            status = "🚨 WARNING: This is a Honeypot!"
            risk_status = "High Risk"
            risk_color = "🔴"
        elif risk_score > 50:
            status = "⚠️ Caution: Medium Risk Token"
            risk_status = "Medium Risk"
            risk_color = "🟠"
        else:
            status = "✅ Safe: Low Risk Token"
            risk_status = "Low Risk"
            risk_color = "🟢"

        # Construct response message
        result = f"\n🔍 Token Address: {token_address}\n"
        result += f"📛 Name: {token_name} ({token_symbol})\n"
        result += f"{status}\n"
        result += f"{risk_color} Risk Level: {risk_status} ({risk_level} - {risk_score}/100)\n"
        result += f"📌 Honeypot Reason: {honeypot_reason}\n"
        result += f"💰 Buy Tax: {buy_tax}% | Sell Tax: {sell_tax}% | Transfer Tax: {transfer_tax}%\n"
        result += f"⛽ Gas Fees - Buy: {buy_gas} | Sell: {sell_gas}\n"
        result += f"📜 Open Source Contract: {'Yes' if open_source else 'No'}\n"
        result += f"🔄 Proxy Contract: {'Yes' if is_proxy else 'No'} | Proxy Calls: {'Yes' if has_proxy_calls else 'No'}\n"
        result += f"💧 Liquidity: {liquidity}\n"
        result += f"👥 Total Holders: {total_holders}\n"
        
        return result

    except requests.exceptions.RequestException as e:
        return f"❌ API Error: {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected Error: {str(e)}"

# List of token contracts to check
tokens_to_check = [
    "0x8b9773e03e987BeD942d1F9695fE6895395ca386",
    "0x34C6211621f2763c60Eb007dC2aE91090A2d22f6",
    "0x45dAc6C8776E5Eb1548d3CdcF0C5f6959e410c3A",
    "0x2C27CF135980cD8f05008f1443e1E4A14d33329F",
]

# Run the honeypot check for each token
for token in tokens_to_check:
    print(check_honeypot(token))
    print("-" * 60)
