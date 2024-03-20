from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
import json

app = Flask(__name__)
model = pickle.load(open('Kidney.pkl', 'rb'))

@app.route('/home',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('auth.html')

@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Check if username and password match
    for user in users:
        if user['username'] == username and user['password'] == password:
            return jsonify({"status": "success"})
        
    return jsonify({"status": "failed"})


# Load users from JSON file
with open('data/users.json', 'r') as f:
    users_data = json.load(f)
    users = users_data['users']

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        sg = float(request.form['sg'])
        htn = float(request.form['htn'])
        hemo = float(request.form['hemo'])
        dm = float(request.form['dm'])
        al = float(request.form['al'])
        appet = float(request.form['appet'])
        rc = float(request.form['rc'])
        pc = float(request.form['pc'])

        values = np.array([[sg, htn, hemo, dm, al, appet, rc, pc]])
        prediction = model.predict(values)

        return render_template('result.html', prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)

