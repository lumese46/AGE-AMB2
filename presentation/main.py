from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)
components = []
attributes = {}

@app.route("/",)
def home():
    return render_template("add_component_tab.html")


@app.route("/component_tab", methods=["POST", "GET"])
def add_components():
    if request.method=="POST":
        component ={}
        component_atts = []
        name_of_component = request.form["Name_of_component"]
        if (name_of_component!=""):
            component["Name_of_component"] = name_of_component
            component["Attributes"] = component_atts
        if (request.form["submit_results"]=="Add Component"):
            if(component["Name_of_component"]):
                print (f'name_of_component {component["Name_of_component"]} \nWith attributes {component["Attributes"]} \nto be added in components {components}')
                return redirect(url_for("home"))
                print("Can't append a component of empty name")
        elif (request.form["submit_results"]=="Add Attribute"):
            attribute = {}
            att_name =request.form["att_name"]
            if(att_name!=""):
                attribute["name"]=att_name
                att_desc = request.form["att_description"]
                attribute["description"]=att_desc
                att_val = request.form["att_default_value"]
                if(att_val==""):
                    att_val = "NONE"
                attribute["default_value"] = att_val
                attributes.append(attribute)
                component_atts.append(attribute)
                print(f"New attribute{component_atts} to be added to component{components[0]}")
            else:
                print("Attribute name empty attribute not added to component")
    else:
        return render_template("add_component_tab.html")


# @app.route("/add_attributes", methods= ["POST", "GET"])
def add_attributes(form):

    return "Attributes"


@app.route("/agent_tab", methods=["POST", "GET"])
def add_agent():
    return ""

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)