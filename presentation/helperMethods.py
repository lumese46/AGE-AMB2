import json
def read_json(fname):
    result = []
    try:
        with open(f"./data/{fname}s.json") as jfile: #read old file if it exists
            result = json.load(jfile)
    except:
        with open(f"./data/{fname}s.json", "w") as jfile:    #create new file
            pass
    return result

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
# gets you the name of the complex agents by name 
def get_complex_agents_by_name(fname):
    data= read_json(fname)
    complex_agents = [agent["Name_of_agent"] for agent in data if agent.get("Type_of_agent") == "COMPLEX"]
    return complex_agents
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
    # print("Summary created")
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



