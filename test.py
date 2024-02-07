import dtilapia

while True:
    text = input('DTilapia > ')
    result, error = dtilapia.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)