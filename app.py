from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Sample data (you can use a database for production)
customers = []

# Define plans
plans = []

# Route for registering a new customer
@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    data = request.get_json()
    if data:
        name = data.get('name')
        dob = data.get('dob')
        email = data.get('email')
        adhar_number = data.get('adhar_number')
        registration_date = data.get('registration_date')
        mobile_number = data.get('mobile_number')
        # Create a new customer record (you would typically save it to a database)
        new_customer = {
            'id': len(customers) + 1,
            'name': name,
            'dob': dob,
            'email': email,
            'adhar_number': adhar_number,
            'registration_date': registration_date,
            'mobile_number': mobile_number,
            'plan_name': None,
            'plan_cost': None,
            'validity': None,
            'plan_status': None
        }
        customers.append(new_customer)
        return jsonify({'message': 'Customer registered successfully!'})
    return jsonify({'error': 'Invalid data format'})

# Route for choosing a new plan
@app.route('/choose_plan/<int:customer_id>', methods=['POST'])
@cross_origin()
def choose_plan(customer_id):
    data = request.get_json()
    if data:
        plan_name = data.get('plan_name')
        # Update customer's plan details (you would typically save it to a database)
        customer = next((c for c in customers if c['id'] == customer_id), None)
        if customer:
            customer['plan_name'] = plan_name
            # Find the selected plan details
            selected_plan = next((p for p in plans if p['name'] == plan_name), None)
            if selected_plan:
                customer['plan_cost'] = selected_plan['cost']
                customer['validity'] = selected_plan['validity']
                customer['plan_status'] = 'Active'
                return jsonify({'message': 'Plan choosen successfully!'})
            else:
                return jsonify({'error': 'Selected plan not found!'})
        else:
            return jsonify({'error': 'Customer not found!'})
    return jsonify({'error': 'Invalid data format'})

# Route for renewing a plan
@app.route('/renew_plan/<int:customer_id>', methods=['POST'])
@cross_origin()
def renew_plan(customer_id):
    data = request.get_json()
    if data:
        renewal_date = data.get('renewal_date')
        plan_status = data.get('plan_status')
        # Update customer's plan details (you would typically save it to a database)
        customer = next((c for c in customers if c['id'] == customer_id), None)
        if customer:
            customer['renewal_date'] = renewal_date
            customer['plan_status'] = plan_status
            return jsonify({'message': 'Plan renewed successfully!'})
        else:
            return jsonify({'error': 'Customer not found!'})
    return jsonify({'error': 'Invalid data format'})

# Route for upgrading/downgrading a plan
@app.route('/upgrade_downgrade_plan/<int:customer_id>', methods=['POST'])
@cross_origin()
def upgrade_downgrade_plan(customer_id):
    data = request.get_json()
    if data:
        existing_plan_name = data.get('existing_plan_name')
        new_plan_name = data.get('new_plan_name')
        plan_cost = data.get('plan_cost')
        validity = data.get('validity')
        plan_status = data.get('plan_status')
        # Update customer's plan details (you would typically save it to a database)
        customer = next((c for c in customers if c['id'] == customer_id), None)
        if customer:
            customer['plan_name'] = new_plan_name
            customer['plan_cost'] = plan_cost
            customer['validity'] = validity
            customer['plan_status'] = plan_status
            return jsonify({'message': 'Plan upgraded/downgraded successfully!'})
        else:
            return jsonify({'error': 'Customer not found!'})
    return jsonify({'error': 'Invalid data format'})

# Route for displaying the customer table
@app.route('/get_all_customers', methods=['GET'])
@cross_origin()
def get_all_customers():
    return jsonify(customers)

if __name__ == '__main__':
    app.run(debug=True)
