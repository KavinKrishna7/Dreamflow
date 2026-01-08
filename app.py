from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
history = []

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_eligibility():
    try:
        data = request.get_json(force=True)

        # Safe extraction with defaults
        age = int(data.get("age", 0))
        income = float(data.get("income", 0))
        loan_type = data.get("loan_type")
        emi = float(data.get("emi", 0))
        loan = float(data.get("loan", 0))
        tenure = float(data.get("tenure", 0))

        # Validation: negative / zero values
        if age <= 0 or income <= 0 or loan <= 0 or tenure <= 0:
            return jsonify({
                "result": "Invalid Input Values",
                "score": 10,
                "suggestion": "All values must be greater than zero",
                "isEligible": False
            })

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
                "suggestion": f"Allowed age: {min_age}-{max_age}",
                "isEligible": False
            })

        if tenure > (max_age - age):
            return jsonify({
                "result": "Tenure Too Long",
                "score": 30,
                "suggestion": f"Max tenure: {max_age - age} years",
                "isEligible": False
            })

        monthly_income = (income * 100000) / 12

        if monthly_income <= 0:
            return jsonify({
                "result": "Invalid Income",
                "score": 15,
                "suggestion": "Income must be positive",
                "isEligible": False
            })

        max_emi = 0.5 * monthly_income - emi
        loan_emi = loan / (tenure * 12)

        if loan_emi <= max_emi:
            result = {
                "result": "Approved! You Are Eligible",
                "score": 90,
                "suggestion": "Proceed with application",
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

    except Exception as e:
        return jsonify({
            "result": "Server Error",
            "score": 0,
            "suggestion": "Please check input values",
            "isEligible": False
        })

@app.route("/history")
def get_history():
    return jsonify(history)

if __name__ == "__main__":
    app.run(debug=True)
