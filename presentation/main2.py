from flask import Flask, render_template, redirect, request, url_for
import json
app = Flask(__name__)
components = []
attributes = []

@app.route("/",)
def home():
    return render_template("add_component_tab.html")

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
        create_json(components)       
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


def create_json(contents):
     jsonObj = json.dumps(contents , indent=4)
     with open("components.json", "w") as outfile:
        outfile.write(jsonObj)

@app.route("/agent_tab", methods=["POST", "GET"])
def add_agent():
    return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)