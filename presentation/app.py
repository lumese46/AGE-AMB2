from flask import Flask, render_template, redirect, request, url_for
import helperMethods, modelhelperMethods


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
class_components =[] #For complex agent can add multiple ones

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
                return render_template("add_model_tab.html", view=1, step=1)
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

    # Logic
    # select type of model you are dealing with
    # enable input parameters button
    ##Input parameters
    # select add input parameters button
    # enter input parameters details
    # get input parameters and save them in input_parameters list
    # select save input parameters
    # save input_parameters list
    # enable class components button
    ##Class components
    # select class components button
    # add class components details (according to SIMPLE or COMPLEX agent and input parameters)
    # select add class component datails
    # add class components details
    # select save class components
    # enable add agents button
    ##Add agents
    # select agents from all agents list
    # get agents selected
    # save selected agents to agents list
    # select number of agents from input parameters
    # select save agent
    # add agent to agents list
    # save environment as GRIDWORLD if  model is COMPLEX, save it as DEFAULT if model is SIMPLE
    # enable add systems button
    ##Add systems
    # select system name from all systems list
    # add system ID
    # select system variables from input parameters list
    # select add system
    # select system name from all systems list
    # add system ID
    # select system variables from input parameters list
    # select save systems
    # save systems to all systems
    # save input parameters, class components, agents and systems to the models json file
    


    new_model_name=""
    action = request.form["submit_action"]
    new_param = {
        "Name": "",
        "dataType": ""
    }
    # Logic implementation
    # select type of model you are dealing with
    chosen_model_type = "COMPLEX"
    #change view according to model type
    # match chosen_model_type:
    #     case "COMPLEX":
    #         return redirect(url_for("model_setup", step=1, model_type=chosen_model_type))
    #     case "SIMPLE":
    #         pass
    # enable input parameters button
    ##Input parameters
    # select add input parameters button
    # enter input parameters details
    # get input parameters and save them in input_parameters list
    # select save input parameters
    print(action)
    #check if action is in the agents lists and change it to add agent
    #check if action is in the components lists and change it to add component

    # if(action in  )
    match(action):
        
        case "Add parameter":
            new_param["Name"]=request.form["name"]
            new_param["dataType"] = request.form["data_type"]
            input_parameters.append(new_param)
            new_model_name = request.form["model_name"]
            return render_template("add_model_tab.html", view=1,model_name=new_model_name, model_type=chosen_model_type)
        
        case "Save input parameters":
            new_param["Name"]=request.form["name"]
            new_param["dataType"] = request.form["data_type"]
            input_parameters.append(new_param)
            new_model_name = request.form["model_name"]
            agents = helperMethods.get_agents_by_type(chosen_model_type)
            components = helperMethods.get_components_by_name("component")
            new_input_parameters =input_parameters
            return render_template("add_model_tab.html",view=2, model_type=chosen_model_type, step=2, model_name = new_model_name, all_components=components, all_agents = agents, input_params = new_input_parameters)
        
        case "Add class component":
            # class_component = {
            #     "Name_of_agent": "",
            #     "Name_of_component": "",
            #     "component_atributes_names": []
            # }
            # class_component["Name_of_agent"]=
            print("In Add component") 

        
    # save input_parameters list
    # enable class components button
    ##Class components
    # select class components button
    # add class components details (according to SIMPLE or COMPLEX agent and input parameters)
    # select add class component datails
    # add class components details
    # select save class components
    # enable add agents button
    ##Add agents
    # select agents from all agents list
    # get agents selected
    # save selected agents to agents list
    # select number of agents from input parameters
    # select save agent
    # add agent to agents list
    # save environment as GRIDWORLD if  model is COMPLEX, save it as DEFAULT if model is SIMPLE
    # enable add systems button
    ##Add systems
    # select system name from all systems list
    # add system ID
    # select system variables from input parameters list
    # select add system
    # select system name from all systems list
    # add system ID
    # select system variables from input parameters list
    # select save systems
    # save systems to all systems
    # save input parameters, class components, agents and systems to the models json file
    return render_template("add_model_tab.html",view=1, model_type=chosen_model_type, step=1)

    
    # print(action)
    # match(action):
    #     #if user wants to add a parameter
    #     case ("Add input parameters"):
    #         view_section = "input parameters"     #change view to show only input parameter fields
        
    #     case ("Add class components"):
    #         view_section = "class components"

    #     case ("Add parameter"):
    #         new_param["Name"]=request.form["name"]
    #         new_param["dataType"] = request.form["data_type"]
    #         print(new_param)
    #         input_parameters.append(new_param)
    #         new_model_name = request.form["model_name"]
    #         return render_template("add_model_tab.html", model_name=new_model_name, view=view_section)
        
    #     case ("Save input parameters"):
    #         new_param["Name"]=request.form["name"]
    #         new_param["dataType"] = request.form["data_type"]
    #         print(new_param)
    #         input_parameters.append(new_param)
    #         model_input_parameters = modelhelperMethods.add_input_parameters(input_parameters)
    #         helperMethods.add_to_json(model_input_parameters, "model")
    #         input_parameters.clear()
    #         new_model_name=""
    #         return render_template("add_model_tab.html", model_name=new_model_name, view=view_section)




# @app.route("/model_setup", methods=["GET", "POST"])
# def model_setup():
#         print("in model setup")
#         if request.form["submit_action"]: #if user wants to move into the first step and add input parameters
#             print ("got into the model type")     
#             return render_template("add_model_tab.html", step=1, view=1)
#         else:
#             return render_template("add_model_tab.html", step=1, view=1)


# def run_me():
#         app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)