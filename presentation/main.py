from flask import Flask, render_template, redirect, request, url_for
import json
import agentMethods as AgentHelper
app = Flask(__name__)
components = []
attributes = []
agent ={}
@app.route("/", methods=["GET","POST"])
def home():
    if(request.method=="POST"): 
        match request.form['browse']:
            case "Components":
                return render_template("add_component_tab.html")
            case "Agents":
                return render_template("add_agent_tab.html")
            case "Systems":
                return render_template("add_system_tab.html")
            case "Models":
                return render_template("add_component_tab.html")
    else:
        return(render_template("base.html"))
    

@app.route("/component_tab", methods=["POST", "GET"])
def add_components():
        component ={"Name_of_component":"",
                     "Component_attributes":[]
                     }
        component_atts = []
        #get input from user
        name_of_component = request.form["Name_of_component"]
        component["Name_of_component"]=name_of_component

        #add later
        # get_user_input(request.form)
        att_desc = request.form["att_description"]
        att_name =request.form["att_name"]
        att_val = request.form["att_default_value"]

        #adding attributes
        add_attributes(component, att_name,  att_desc, att_val)
        add_attributes(component, att_name,  att_desc, att_val)
        print(component)
        add_component(component, components)
        add_component(component, components) 

        #adding json file
        AgentHelper.create_json(components, "components")       
        return render_template("add_component_tab.html")



    #     if (name_of_component!=""):
    #         component["Name_of_component"] = name_of_component
    #         component["Attributes"] = component_atts
    #     if (request.form["submit_results"]=="Add Component"):
    #         if(component["Name_of_component"]):
    #             print (f'name_of_component {component["Name_of_component"]} \nWith attributes {component["Attributes"]} \nto be added in components {components}')
    #             return redirect(url_for("home"))
    #             print("Can't append a component of empty name")
    #     elif (request.form["submit_results"]=="Add Attribute"):
    #         attribute = {}
    #         att_name =request.form["att_name"]
    #         if(att_name!=""):
    #             attribute["name"]=att_name
    #             att_desc = request.form["att_description"]
    #             attribute["description"]=att_desc
    #             att_val = request.form["att_default_value"]
    #             if(att_val==""):
    #                 att_val = "NONE"
    #             attribute["default_value"] = att_val
    #             attributes.append(attribute)
    #             component_atts.append(attribute)
    #             print(f"{attribute}")
    #         else:
    #             print("Attribute name empty attribute not added to component")
    # else:


# @app.route("/add_attributes", methods= ["POST", "GET"])
def add_attributes(component, att_name,  att_desc, att_val):
    attribute = {}
    attribute["name"]=att_name
    attribute["description"]=att_desc
    attribute["default_value"]=att_val
    component["Component_attributes"].append(attribute)

def add_component(component, components):
     components.append(component)


def create_json(contents,name):
     jsonObj = json.dumps(contents , indent=4)
     with open(f"{name}.json", "w") as outfile:
        outfile.write(jsonObj)

@app.route("/agents", methods=["POST", "GET"])
def add_agent():
    agent = {
        "Name_of_agent": "",
        "Class_component_name":"",
        "Components":[],
        "Type": "",
        }
    if(request.method=="POST"):
        agent["Name_of_agent"] = request.form["agent_name"]
        agent["Type"] = request.form["agent_type"]
        agent["Components"].append("Energy")
        agent["Class_component_name"] = request.form["agent_class_name"]

        match(request.form["add_to_agent"]):
            case("Add Components"):
                AgentHelper.add_component_to_agent(agent,"Energy")
            case("Add agent"):
                AgentHelper.add_agent(agent)

        
        print(agent)
    return (render_template("add_agent_tab.html"))



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)