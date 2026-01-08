from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_eligibility():
    data = request.json

    age = int(data["age"])
    income = float(data["income"])
    loan_type = data["loan_type"]
    emi = float(data["emi"])
    loan = float(data["loan"])
    tenure = float(data["tenure"])

    limits = {
        "p": (21, 65),
        "h": (21, 70),
        "c": (21, 65),
        "e": (18, 40)
    }

    if loan_type not in limits:
        return jsonify({
            "result": "Invalid Loan Type",
            "score": 10,
            "suggestion": "Select a valid loan type",
            "isEligible": False
        })

    min_age, max_age = limits[loan_type]

    if not (min_age <= age <= max_age):
        return jsonify({
            "result": "Age Criteria Not Met",
            "score": 20,
            "suggestion": f"Age must be between {min_age}-{max_age}",
            "isEligible": False
        })

    if tenure > (max_age - age):
        return jsonify({
            "result": "Tenure Too Long",
            "score": 30,
            "suggestion": f"Max tenure allowed: {max_age - age} years",
            "isEligible": False
        })

    monthly_income = (income * 100000) / 12
    max_emi = (0.5 * monthly_income) - emi
    loan_emi = loan / (tenure * 12)

    if loan_emi <= max_emi:
        result = {
            "result": "Approved! You are eligible",
            "score": 90,
            "suggestion": "You can proceed with the loan",
            "isEligible": True
        }
    else:
        result = {
            "result": "EMI Capacity Exceeded",
            "score": 45,
            "suggestion": f"Max EMI allowed: ₹{int(max_emi)}",
            "isEligible": False
        }

    history.append({**data, **result})
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
