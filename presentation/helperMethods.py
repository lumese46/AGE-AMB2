import json
import subprocess
import os
def read_json(fname):
    result = []
    try:
        with open(f"./data/{fname}s.json") as jfile: #read old file if it exists
            result = json.load(jfile)
    except:
        with open(f"./data/{fname}s.json", "w") as jfile:    #create new file
            pass
    return result
def clear_json_file(fname):
    with open(f"./data/{fname}s.json", 'w') as file:
        # Truncate the file (remove all content)
        file.truncate()

# Example usage: Clear a JSON file named 'example.json'
clear_json_file('example.json')


def add_to_json(contents,outfile):
    saved_components = read_json(outfile) #read saved outfile.json
    saved_components.append(contents) #add newcontetes to file
    jsonObj = json.dumps(saved_components , indent=4)

    with open(f"./data/{outfile}s.json", "w") as iof:
        iof.writelines(jsonObj) #write to file

#enter an array of json params and add the names to an array. Returns an array of names
def param_summary(json_str_arr):
    result=[]
    print(json_str_arr[0]+" to be converted to string")
    # print(json.dumps(json_str_arr[0]))
    for js in json_str_arr:
        js = js.replace("\'", "\"")
        js_json = json.loads(js)
        result.append(js_json["Name"])
    return result

def add_attributes(att_name,  att_desc, att_val):
    attribute = {}
    attribute["name"]=att_name
    attribute["description"]=att_desc
    attribute["default_value"]=att_val
    return attribute

#get all components by name (ie all components, agents, systems and model)
def get_components_by_name(fname):
    saved_comps= read_json(fname)
    results =[]
    for comp in saved_comps:
        results.append(comp[f"Name_of_{fname}"])
    return results
#####################################################oratile########################
# gets you the name of the complex agents by name 
def get_complex_agents_by_name(fname):
    data= read_json(fname)
    complex_agents = [agent["Name_of_agent"] for agent in data if agent.get("Type_of_agent") == "COMPLEX"]
    return complex_agents
# this create a data collector dict 
def create_data_collector_dict(agents_array):
    data_collector_dict = {
        "Name_of_agents": agents_array
    }
    return data_collector_dict


# returns input parameters
def get_input_parameters(fname):
    data= read_json(fname)
    input_parameters = []
    for item in data:
        if 'input_parameters' in item:
            input_parameters = item['input_parameters']
            break
    return input_parameters

# for execute 
def transform_to_input_parameters(input_params_from_user):
    input_parameters = []

    for param_name, param_value in input_params_from_user.items():
        parameter = {"name": param_name, "input": param_value}
        input_parameters.append(parameter)

    return input_parameters
def get_model_name():
    # Load the JSON data
    components = read_json("model")

    # Fetch the first component
    model_name = components[0]
    return model_name

def run_model(fname):
    # Assuming model.py is in the 'models' directory
    script_path = f"./data/{fname}.py"
    # Run the script using subprocess
    subprocess.run(["python", script_path])


#####################################################oratile########################


#give component name, get component with it's attributes
def get_component(component_name):
    results = []
    components_from_file =read_json("component")   #read components json file
    for comp in components_from_file:
        if comp["Name_of_component"] == component_name:
            results.append(comp)
            break
    return results

#give a list of components you want a summary of (that being the name and all the names of the attributes) and get the summary of them in an array
def get_components_summary(compList):
    results = []
    components_from_file =read_json("component")   #read components json file
    for comp in components_from_file:
        comp_summary = {
            "Name_of_component":comp["Name_of_component"],
            "Names_of_component_atributes": []
        }
        if comp["Name_of_component"] in compList:
            for comp_att in comp["Component_attributes"]:
                comp_summary["Names_of_component_atributes"].append(comp_att["name"])
            results.append(comp_summary)
        else:
            pass
    print("Summary created")
    return results

#get all agents
def get_all_agents():
    result = []
    all_agents = read_json("agent")
    for agent in all_agents:
        result.append(agent)
    return result

#supply the type of agents you want to add, get all agents of that type in that list in an array of their names
def get_agents_by_type(agent_type):
    result = []
    all_agents = get_all_agents()
    for agent in all_agents:
        if agent["Type_of_agent"]==agent_type:
            result.append(agent["Name_of_agent"])
    return (result)



