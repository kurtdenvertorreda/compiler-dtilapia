import dtilapia

while True:
    code = ""
    text = input('DTilapia > ')
    if not text:
            break

        # Concatenate the input line to the existing code
    code += text + '\n'

    if not code.strip():
          break
    
    result, error = dtilapia.run('<stdin>', text)
    if error: print(error.as_string())
    else: print(result)