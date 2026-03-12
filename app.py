from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-quote', methods=['POST'])
def submit_quote():
    name = request.form['name']
    phone = request.form['phone']
    message = request.form['message']
    print(f"New quote request from {name} - {phone}")
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
