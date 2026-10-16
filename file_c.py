from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# TinyFish Agent Wrapper Function
def run_tinyfish_agent(target_url):
    """
    TinyFish autonomous web agent jo background headless browser launch
    karke target site ke links, checkout modals aur Terms & Conditions
    ko traverse karta hai.
    """
    print(f"[TinyFish Agent] Launching autonomous browser for: {target_url}")
    time.sleep(1.5)  # Simulate browser navigation & DOM extraction
    
    # Mock extracted legal clauses by TinyFish Agent
    extracted_data = {
        "url": target_url,
        "scanned_pages": ["/checkout", "/terms-and-conditions", "/cancellation-policy"],
        "extracted_clauses": [
            "User agrees to auto-renewal subscription of Rs 499/month unless cancelled 48h prior.",
            "Items bought during promotional offers carry strict zero refund or exchange liability.",
            "Personal contact data may be shared with trusted marketing affiliates."
        ]
    }
    return extracted_data

# AI Dark Pattern & Risk Analyzer
def analyze_clauses_with_ai(clauses):
    """
    Extracted clauses ko AI/NLP engine se scan karke Dark Patterns
    aur Risk Score calculate karta hai.
    """
    red_flags = []
    risk_score = 30  # Base safe score

    for text in clauses:
        lower_text = text.lower()
        if "auto-renewal" in lower_text or "recurring" in lower_text:
            risk_score += 35
            red_flags.append("Predatory Auto-Debit: Hidden monthly recurring charge detected.")
        if "zero refund" in lower_text or "no return" in lower_text:
            risk_score += 25
            red_flags.append("Forced Sale: Non-refundable clause hidden in fine print.")
        if "shared with" in lower_text and "marketing" in lower_text:
            risk_score += 15
            red_flags.append("Data Resale: Personal info can be distributed to 3rd-party advertisers.")

    risk_score = min(risk_score, 95)
    return risk_score, red_flags

@app.route('/api/scan', methods=['POST'])
def scan_website():
    data = request.json or {}
    url = data.get('url', '').strip()

    if not url:
        return jsonify({"error": "Please provide a valid website URL"}), 400

    # 1. TinyFish agent executes autonomous web traversal
    tinyfish_result = run_tinyfish_agent(url)

    # 2. AI analyzes extracted contracts & dark patterns
    score, flags = analyze_clauses_with_ai(tinyfish_result["extracted_clauses"])

    response = {
        "status": "success",
        "url": url,
        "risk_score": score,
        "risk_level": "High Risk" if score > 70 else ("Moderate" if score > 40 else "Safe"),
        "pages_scanned": tinyfish_result["scanned_pages"],
        "red_flags": flags,
        "summary": "Website contains deceptive terms with hidden subscription billing and strict non-refundable terms."
    }
    return jsonify(response)

if __name__ == '_main_':
    print("SentinelShield Backend running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)