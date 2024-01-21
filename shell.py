import dtilapia

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Specify the path to your file
file_path = 'temp_code.dtil'
file_content = read_file(file_path)

lexer = dtilapia.Lexer(file_path, file_content)
tokens, error = lexer.make_tokens()

if error:
    print(error.as_string())
else:
    for token in tokens:
        print(token)