from flask import Flask, request, jsonify
from rule_engine.ast_parser import create_rule
from rule_engine.rule_combiner import combine_rules
from rule_engine.evaluator import evaluate_rule

app = Flask(__name__)

# Global rules storage
rules = []

@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    try:
        rule_string = request.json.get('rule_string')
        if not rule_string:
            return jsonify({"error": "rule_string is required"}), 400

        ast_rule = create_rule(rule_string)
        rules.append(ast_rule)
        return jsonify({"message": "Rule created", "rule_ast": str(ast_rule)}), 201
    except Exception as e:
        # Log the error for debugging
        print(f"Error creating rule: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    try:
        if not rules:
            return jsonify({"error": "No rules to combine"}), 400

        combined_ast = combine_rules(rules)
        return jsonify({"message": "Rules combined", "combined_ast": str(combined_ast)}), 200
    except Exception as e:
        # Log the error for debugging
        print(f"Error combining rules: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    try:
        rule_data = request.json.get('data')
        if not rule_data:
            return jsonify({"error": "Data is required"}), 400

        if not rules:
            return jsonify({"error": "No rules available for evaluation"}), 400

        combined_ast = combine_rules(rules)
        result = evaluate_rule(combined_ast, rule_data)
        return jsonify({"result": result}), 200
    except Exception as e:
        # Log the error for debugging
        print(f"Error evaluating rule: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/somepage')
def somepage():
    return "This is some page!"

if __name__ == '__main__':
    app.run(debug=True)
