from flask import Flask, render_template, redirect, request, url_for
import json
import helperMethods
app = Flask(__name__)
components = []
component ={"Name_of_component":"",
            "Component_attributes":[]
            }
attributes = []
agent ={}


################################################ Home ################################################

@app.route("/", methods=["GET","POST"])
def home():
    if(request.method=="POST"): 
        match request.form['browse']:
            case "Components":
                return render_template("add_component_tab.html", savedComp={})
            case "Agents":
                return render_template("add_agent_tab.html")
            case "Systems":
                return render_template("add_system_tab.html")
            case "Models":
                return render_template("add_component_tab.html")
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
                helperMethods.add_to_json(component, "components") #add component to json
                attributes.clear()
                component_name=""
                
        return render_template("add_component_tab.html", compName=component_name, all_components=helperMethods.get_components())





############################################################AGENT ROUTES#############################################################

@app.route("/agents", methods=["POST", "GET"])
def add_agent():
    agent = {
        "Name_of_agent": "",
        "Class_component_name":"",
        "Components":[],
        "Type": "",
        }
    agents = helperMethods.read_json("agents")
    return (render_template("add_agent_tab.html"))

def read_json():
    result = []
    with open("./data/agents.json") as jfile:
        result = json.load(jfile)

    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)