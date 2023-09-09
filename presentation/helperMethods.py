import json

def read_json(fname):
    result = []
    try:
        with open(f"./data/{fname}.json") as jfile:
            print("read old file")
            result = json.load(jfile)
    except:
        with open(f"./data/{fname}.json", "w") as jfile:
            print("cerated a new file")
    return result

def add_to_json(contents,outfile):
    print(f"Adding {contents} attri to ./data/{outfile}.json")
    saved_components = read_json(outfile)
    saved_components.append(contents)
    jsonObj = json.dumps(saved_components , indent=4)

    with open(f"./data/{outfile}.json", "w") as iof:
        iof.writelines(jsonObj)

def add_attributes(att_name,  att_desc, att_val):
    attribute = {}
    attribute["name"]=att_name
    attribute["description"]=att_desc
    attribute["default_value"]=att_val
    return attribute

def get_components():
    saved_comps= read_json("components")
    results =[]
    for comp in saved_comps:
        results.append(comp["Name_of_component"])
    return results