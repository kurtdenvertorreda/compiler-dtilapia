from flask import Flask, render_template, request, jsonify
import os
import dtilapia

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_code():
    try:
        data = request.json
        code = data['code']

        # Write code to a temporary file
        with open('temp_code.dtil', 'w') as file:
            file.write(code)

        def read_file(file_path):
            with open(file_path, 'r') as file:
                return file.read()

        # Specify the path to your file
        file_path = 'temp_code.dtil'
        file_content = read_file(file_path)

        lexer = dtilapia.Lexer(file_path, file_content)
        tokens, error = lexer.make_tokens()

        #test checkpoint
        #print(file_content)
        #if error:
        #    print(error.as_string())
        #    return jsonify({'error': error.as_string()})
        #else:
        #    for token in tokens:
        #        print(token)

        # Remove the temporary file
        os.remove('temp_code.dtil')

        if error:
            return jsonify({'error': error.as_string()})
        else:
            # Return the tokens as JSON
            return jsonify({'tokens': [str(token) for token in tokens]})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)