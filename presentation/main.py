from flask import Flask, render_template, redirect, request, url_for
import json
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
        "Type": "",
        }


################################################ Home ################################################

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


@app.route("/component_tab", methods=["POST", "GET"])
def add_components():
        #get input from user
        component_name = request.form["Name_of_component"]
        component["Name_of_component"]=request.form["Name_of_component"]
        button_clicked = request.form["submit_results"]
        match (button_clicked):
            case "Add attribute":
                attributes.append(helperMethods.add_attributes(
                request.form["att_name"],
                request.form["att_description"],
                request.form["att_default_value"]
                )
                )
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
                
        return render_template("add_component_tab.html", compName=component_name, all_components=helperMethods.get_components_by_name("component"), all_agents = helperMethods.get_components_by_name("agent"))





############################################################AGENT ROUTES#############################################################

@app.route("/agents", methods=["POST", "GET"])
def add_agent():
    agent_action = request.form["add_to_agent"]
    comp_type = "simple"
    match agent_action:
        case "Add Agent":
            agent["Name_of_agent"] = request.form["agent_name"]
            agent["Type"] = comp_type
            agent["Class_component_name"] = request.form["agent_class_componet_name"]
            agent["Components"] = helperMethods.get_all_components(request.form.getlist("component_to_add")) #get detailed components using their names 
            helperMethods.add_to_json(agent,"agent")
            #clear screen
            comp_type = "simple"

        case "Simple":
            comp_type = "simple"
            print(agent_action)
        case "Complex":
            comp_type = "complex"
            print(agent_action)


    agents = helperMethods.read_json("agent")
    return render_template("add_agent_tab.html",all_components=helperMethods.get_components_by_name("component"), all_agents=helperMethods.get_components_by_name("agent"), agent_type=comp_type)


######################################## Systems Tab #######################################################################################################################################################
@app.route("/systems", methods=["POST","GET"])
def add_system():
    system = {
        "Name_of_system":"",
        "code": ""

    }
    if request.method=="POST":
        system["Name_of_system"] = request.form["sys_name"]
        system["code"]=request.form["editor"]
        helperMethods.add_to_json(system, "system")
    return render_template("add_system_tab.html",all_systems=helperMethods.get_components_by_name("system"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)