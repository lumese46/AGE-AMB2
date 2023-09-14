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
    global comp_type
    name=request.form["agent_name"]
    match agent_action:
        case "Add Agent":
            agent["Name_of_agent"] = name
            agent["Type_of_agent"] = comp_type
            agent["Class_component_name"] = request.form["agent_class_componet_name"]
            components_to_add_by_name = (request.form.getlist("component_to_add")) #get detailed components using their names 
            components_summary = helperMethods.get_components_summary(components_to_add_by_name)    #get component summary list
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


# def run_me():
#         app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)