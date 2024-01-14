# app.py
from flask import Flask, render_template, request, jsonify
import dtilapia

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/runcode', methods=['POST'])
def run_code():
    code = request.json['code']
    result, error = dtilapia.run('<stdin>', code)
    if error:
        return jsonify({'result': None, 'error': error.as_string()})
    else:
        return jsonify({'result': result, 'error': None})

if __name__ == '__main__':
    app.run(debug=True)
    

#while True:
#    text = input('DTilapia > ')
#    result, error = dtilapia.run('<stdin>', text)

#    if error: print(error.as_string())
#    else: print(result)