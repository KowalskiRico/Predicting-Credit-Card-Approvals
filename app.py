from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# static_url_path='' lets /assets/... and /images/... work as written in index.html
app = Flask(__name__, static_folder='static', static_url_path='')

model  = joblib.load(os.path.join(BASE, 'credit_model.pkl'))
scaler = joblib.load(os.path.join(BASE, 'scaler.pkl'))

# Same encoding LabelEncoder used in your notebook (alphabetical order)
YES_NO = {'N': 0, 'Y': 1}
EDUCATION = {
    'Higher education': 1,
    'Incomplete higher': 2,
    'Secondary / secondary special': 4,
}

# Same columns, same order as training
COLUMNS = ['Car_Owner', 'Propert_Owner', 'Annual_income', 'EDUCATION']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        d = request.get_json(force=True)
        row = pd.DataFrame([[
            YES_NO[d['car_owner']],
            YES_NO[d['property_owner']],
            float(d['income']),
            EDUCATION[d['education']],
        ]], columns=COLUMNS)

        pred = int(model.predict(scaler.transform(row))[0])
        # 0 = Approved, 1 = Rejected (as in your presentation)
        label = 'Approved' if pred == 0 else 'Rejected'
        return jsonify(status='success', prediction=label)
    except Exception as e:
        return jsonify(status='error', message=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True)