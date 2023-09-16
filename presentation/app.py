from flask import Flask, render_template, redirect, request, url_for
import helperMethods


app = Flask(__name__)
components = []
component ={"Name_of_component":"",
            "Component_attributes":[]
            }
attributes = []
agent = {
        "Name_of_agent": "",
        "Class_component_name":"",
        "Components":[],
        "Type_of_agent": "",
        }

comp_type = "SIMPLE"
input_parameters = []

################################################ Home ################################################
#Set up site navigation
@app.route("/", methods=["GET","POST"])
def home():
    if(request.method=="POST"): 
        match request.form['browse']:
            case "Components":
                return render_template("add_component_tab.html", all_components=helperMethods.get_components_by_name("component"))
            case "Agents":
                return render_template("add_agent_tab.html", all_components=helperMethods.get_components_by_name("component"),all_agents = helperMethods.get_components_by_name("agent"))
            case "Systems":
                return render_template("add_system_tab.html",all_systems=helperMethods.get_components_by_name("system"),all_agents = helperMethods.get_components_by_name("agent"))
            case "Models":
                return render_template("add_model_tab.html", all_components=helperMethods.get_components_by_name("component"),all_agents = helperMethods.get_components_by_name("agent"), all_systems=helperMethods.get_components_by_name("system"))
    else:
        return(render_template("add_component_tab.html"))
    

################################################ Components ################################################

#control components though the components window
@app.route("/component_tab", methods=["POST", "GET"])
def add_components():
        #get input from user
        component_name = request.form["Name_of_component"]
        component["Name_of_component"]=request.form["Name_of_component"]
        button_clicked = request.form["submit_results"]
        match (button_clicked):
            #if user wants to add attributes to a component
            case "Add attribute":
                attributes.append(helperMethods.add_attributes(
                request.form["att_name"],
                request.form["att_description"],
                request.form["att_default_value"]
                )
                )

            #if user wants to save/add component to component's list
            case "Add component":
                #add last attribute
                attributes.append(helperMethods.add_attributes(
                request.form["att_name"],
                request.form["att_description"],
                request.form["att_default_value"]
                )
                )
                all_atts = attributes
                component["Component_attributes"]=all_atts #assign attributes to components
                helperMethods.add_to_json(component, "component") #add component to json
                attributes.clear()
                component_name=""
                #call create components method here
                
            case _:
                component_to_edit = helperMethods.get_component(request.form["edit_component"])
                allAttsNames = []
                for att in component_to_edit[0]["Component_attributes"]:
                    allAttsNames.append(att["name"])
                print(component_to_edit)
                return render_template("edit_component.html", compName=request.form["edit_component"], all_components=allAttsNames, all_agents = helperMethods.get_components_by_name("agent"))
        return render_template("add_component_tab.html", compName=component_name, all_components=helperMethods.get_components_by_name("component"), all_agents = helperMethods.get_components_by_name("agent"))



############################################### Edit Component ###################################
# @app.route("/edit_component", methods=["POST"])
# def edit_component():
#     #get component to be edited
#     action = request.form["edit_component"]
#     match(action):
#         case("edit_component"):
#             component_to_edit = helperMethods.get_component(request.form["edit_component"])
#             allAttsNames = []
#             for att in component_to_edit[0]["Component_attributes"]:
#                 allAttsNames.append(att["name"])
#             print(component_to_edit)
#             return render_template("edit_component.html", compName=request.form["edit_component"], all_components=allAttsNames, all_agents = helperMethods.get_components_by_name("agent"))
#     return render_template("add_component_tab.html", compName=request.form["edit_component"], all_components=allAttsNames, all_agents = helperMethods.get_components_by_name("agent"))



############################################################AGENT ROUTES#############################################################

#control agents through the agents tab
@app.route("/agents", methods=["POST", "GET"])
def add_agent():
    agent_action = request.form["add_to_agent"]
    global comp_type
    name=request.form["agent_name"]
    match agent_action:
        case "Add Agent":
            agent["Name_of_agent"] = name
            agent["Type_of_agent"] = comp_type
            agent["Class_component_name"] = request.form["agent_class_componet_name"]
            components_to_add_by_name = (request.form.getlist("component_to_add")) #get  list of component the user wants to add to their agent
            components_summary = helperMethods.get_components_summary(components_to_add_by_name)#get component summary list
            agent["Components"].append(components_summary)
            helperMethods.add_to_json(agent,"agent")
            agent["Components"].clear()
            name=""
            #clear screen

        case "Simple":
            comp_type = "SIMPLE"
            print(agent_action)

        case "Complex":
            comp_type = "COMPLEX"
            print(agent_action)


    agents = helperMethods.read_json("agent")
    return render_template("add_agent_tab.html", agent_name=name,all_components=helperMethods.get_components_by_name("component"), all_agents=helperMethods.get_components_by_name("agent"), agent_type=comp_type)


######################################## Systems Tab #######################################################################################################################################################
@app.route("/systems", methods=["POST","GET"])
def add_system():
    system = {
        "Name_of_system":"",
        "code": ""
    }
    dummyCode = ""
    if request.method=="POST":
        name=request.form["sys_name"]
        action=request.form["submit_code"]
        match(action):
            case "Create system":
                system["Name_of_system"] = request.form["sys_name"]
                print ("system created")
                dummyCode = ("#dummy code will go here")
            case "Save system":
                #Write system to json
                system["code"]=request.form["editor_code"]
                
                helperMethods.add_to_json(system, "system")
                print("system saved")
            case "Run":
                print(dummyCode)
    return render_template("add_system_tab.html",all_systems=helperMethods.get_components_by_name("system"), sys_name=name, sys_code =dummyCode)


###################################################### Model Routes ############################################3

@app.route("/model", methods=["GET", "POST"])
def add_model():
    print("in model")
    action = request.form["submit_action"]
    new_param = {
        "Name": "",
        "dataType": ""
    }
    print(action)
    match(action):
        case ("Save input parameters"):
            new_param["Name"]=request.form["name"]
            new_param["dataType"] = request.form["data_type"]
            input_parameters.append(new_param)
    
    print(input_parameters)
    return render_template("add_model_tab.html", all_components=helperMethods.get_components_by_name("component"),all_agents = helperMethods.get_components_by_name("agent"), all_systems=helperMethods.get_components_by_name("system"))


# def run_me():
#         app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)