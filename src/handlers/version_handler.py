import qiskit, json

def json_format(json_str: str):
     return json_str.replace("\'", "\"").replace("None", "null")

def version_handler():
    json_data = json.loads(json_format(str(qiskit.__qiskit_version__)))
    for item in json_data:
        print(item + ": " + str(json_data[item]))
    return
