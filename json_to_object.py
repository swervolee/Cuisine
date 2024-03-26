with open("file.json", "r") as f:
    data = f.read()
    data = data.replace("false", "False")
    data = eval(data)
    print(type(data))