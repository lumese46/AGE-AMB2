from flask import Flask, render_template, redirect, request, url_for, session
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
class_component ={
        "Name_of_agent": "",
        "Name_of_component":"",
        "component_atributes_names": []
    }
class_components =[] #For complex agent can add multiple ones
model_agent = {
                "Name_of_agent": "",
                "number_of_agents": ""
            }
model_agents = []
saved_model_agents =[]
model_system={
                "Name_of_system": "MovementSystem",
                "system_id": "move",
                "system_variables": []
            }
model_systems = []
complete_model =[]
################################################ Home ################################################
#Set up site navigation
@app.route("/", methods=["GET","POST"])
def home():
    if(request.method=="POST"): 
        match request.form['browse']:
            case "Components":
                return render_template("add_component_tab.html",
                                        all_components=helperMethods.get_components_by_name("component"))
            case "Agents":
                return render_template("add_agent_tab.html", 
                                       all_components=helperMethods.get_components_by_name("component"),
                                       all_agents = helperMethods.get_components_by_name("agent"))
            case "Systems":
                return render_template("add_system_tab.html",
                                       all_systems=helperMethods.get_components_by_name("system"),
                                       all_agents = helperMethods.get_components_by_name("agent"))
            case "Models":
                return render_template("setup_model.html", model_type="")
            
            case "Execute":# Example usage

                input_params = helperMethods.get_input_parameters("modelTestReference")
                
                return render_template("execute_model_tab.html",input_params=input_params)
            
            case "Data Collector":
                return render_template("data_collector.html",complex_agents=helperMethods.get_complex_agents_by_name("agent"))
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
                # print(component_to_edit)
                return render_template("edit_component.html", 
                                       compName=request.form["edit_component"], 
                                       all_components=allAttsNames, all_agents = helperMethods.get_components_by_name("agent"))
        return render_template("add_component_tab.html", 
                               compName=component_name, all_components=helperMethods.get_components_by_name("component"), 
                               all_agents = helperMethods.get_components_by_name("agent"))



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
            # print(agent_action)

        case "Complex":
            comp_type = "COMPLEX"
            # print(agent_action)


    agents = helperMethods.read_json("agent")
    return render_template("add_agent_tab.html", 
                           agent_name=name,all_components=helperMethods.get_components_by_name("component"), 
                           all_agents=helperMethods.get_components_by_name("agent"), agent_type=comp_type)

######################################## Data Collector Tab #######################################################################################################################################################


@app.route("/dataCollector", methods=["POST", "GET"])
def data_collector():
    submit_disabled = False
    if request.method == "POST":
        # Get the selected agents from the radio buttons
        selected_agents = request.form.getlist("selected_agents")
        
        # You can add additional logic or processing here
        contents = helperMethods.create_data_collector_dict(selected_agents)
        helperMethods.add_to_json(contents,"dataCollector")
        submit_disabled = True

    

    return render_template("data_collector.html", complex_agents=helperMethods.get_complex_agents_by_name("agent"), submit_disabled=submit_disabled)


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
                # print ("system created")
                dummyCode = ("#dummy code will go here")
            case "Save system":
                #Write system to json
                system["code"]=request.form["editor_code"]
                
                helperMethods.add_to_json(system, "system")
                # print("system saved")
            case "Run":
                #print(dummyCode)
                return render_template("add_system_tab.html",
                           all_systems=helperMethods.get_components_by_name("system"), 
                           sys_name=name, sys_code =dummyCode)

###################################################### execute Route ############################################3
@app.route("/execute", methods=["POST","GET"])
def execute_model():
    input_params = helperMethods.get_input_parameters("modelTestReference")
   
    if request.method=="POST":
        action = request.form["submit_results"]

        #take value of button in templete
        match (action):
            case "Execute":
                print("Hello exec")
            case "Update":
                print("Update")
    return render_template("execute_model_tab.html",input_params=input_params)




###################################################### Model Routes ############################################3
@app.route("/model_type", methods=["GET", "POST"])
def add_model_type():
    if request.method=="POST":
        model_type = request.form["model_type"]
        chosen_model_type = model_type
        session["model_type"] = model_type
        #print (chosen_model_type)
        return render_template("add_model_tab.html", view=1, model_type=chosen_model_type)
    else:
        return render_template("setup_model.html")
    
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


    global model_agents
    global input_parameters
    new_model_name=""
    action = request.form["submit_action"]
    new_param = {
        "Name": "",
        "dataType": ""
    }

    chosen_model_type=session["model_type"]
    all_agents = helperMethods.get_components_by_name("agent")
    all_components = helperMethods.get_components_by_name("component")
    all_current_systems = helperMethods.get_components_by_name("system")
    agent_to_add_to_model=""
    system_to_add_to_model=""
    #create agent and component addition option
    state = (request.form.getlist("state"))
    if ((action in all_agents) and chosen_model_type=="COMPLEX"):
        #print("getting state")
        state = (request.form.getlist("state"))
        #print (state[0])
        if state[0]=="2":
            #print("changing state to 2")
            action="Add class component Name_of_agent"
        elif state[0]=="3":
            #print("initial action "+ action)
            print("Agent chosen to be added to model is "+ action)
            agent_to_add_to_model = action
            action="Add model agent"

    elif ((action in all_components) and session["model_type"]=="COMPLEX"):
        action="Add class component Name_of_component"
    elif (action in all_current_systems):
        system_to_add_to_model = action
        action = "Add system to model"
    #check if action is in the agents lists and change it to add agent
    #check if action is in the components lists and change it to add component
    #check if action is in the systems lists and change it to add system model


    #print(action+" action on "+session["model_type"]+ " model at state "+ state[0])

    #perform action based on action

    match(action):
        case "Add parameter":
            new_param["Name"]=request.form["name"]
            new_param["dataType"] = request.form["data_type"]
            if( new_param not in input_parameters):
                input_parameters.append(new_param)
            new_model_name = request.form["model_name"]
            return render_template("add_model_tab.html",
                                   view=1,
                                   input_params = input_parameters,
                                   model_name=new_model_name,
                                   model_type=session["model_type"])
        
        case "Save input parameters":
            new_param["Name"]=request.form["name"]
            new_param["dataType"] = request.form["data_type"]
            if( new_param not in input_parameters):
                input_parameters.append(new_param)
            new_model_name = request.form["model_name"]
            agents = helperMethods.get_agents_by_type(chosen_model_type)
            components = helperMethods.get_components_by_name("component")
            return render_template("add_model_tab.html",
                                   view=2, 
                                   model_type=session["model_type"],
                                   model_name = new_model_name,
                                   all_class_components = class_components,
                                   all_components=components, 
                                   all_agents = agents,
                                   input_params = input_parameters)
        
        case "Add class component Name_of_agent":
            #print(input_parameters)
            class_component["Name_of_agent"]=request.form["submit_action"]
            new_model_name  = request.form["model_name"]
            return render_template("add_model_tab.html",
                                   view=2, 
                                   model_type=session["model_type"], 
                                   model_name = new_model_name, 
                                   all_class_components = class_components,
                                   all_components=all_components, 
                                   all_agents = helperMethods.get_agents_by_type(chosen_model_type), 
                                   input_params=input_parameters)

        case "Add class component Name_of_component":
            class_component["Name_of_component"]=request.form["submit_action"]
            new_model_name = request.form["model_name"]
            summary = helperMethods.get_components_summary([class_component["Name_of_component"]])
            # len(summary["Names_of_component_atributes"])
            return render_template("add_model_tab.html",
                                   view=2, 
                                   model_type=session["model_type"], 
                                   model_name = new_model_name,
                                   all_class_components = class_components,
                                   all_components=all_components, 
                                   all_agents = helperMethods.get_agents_by_type(chosen_model_type), 
                                   input_params=input_parameters, error_message=f"Select {len(summary[0]['Names_of_component_atributes'])} parameter(s)")

        case "Add class component":
            new_model_name = request.form["model_name"]
            selected_params = request.form.getlist("params_to_add")
            #print("input params")
            #print(selected_params) 
            class_component_summary = helperMethods.get_components_summary([class_component["Name_of_component"]])
            att_summary = class_component_summary[0]["Names_of_component_atributes"]
            params_summary = helperMethods.param_summary(selected_params)

            #print(( f"Params summary {params_summary}"))
            if(len(selected_params)==len(att_summary)):
                class_component["component_atributes_names"] = params_summary
                #print(f"Class component {class_component}")
                class_components.append(class_component)
                #print(class_components)
                return render_template("add_model_tab.html",
                                       view=2, 
                                       model_type=session["model_type"], 
                                       model_name = new_model_name,
                                       all_class_components = class_components,
                                       all_components=all_components, 
                                       all_agents = helperMethods.get_agents_by_type(chosen_model_type), 
                                       input_params=input_parameters)
            else:
                #print("error occured")
                return render_template("add_model_tab.html",view=2, 
                                       mmodel_type=session["model_type"], 
                                       model_name = new_model_name, 
                                       all_components=all_components, 
                                       all_agents = helperMethods.get_agents_by_type(chosen_model_type),
                                       input_params=input_parameters,
                                       error_message=f"Pick {len(att_summary)} parameter(s)")
            
        case "Save class components":
            new_model_name = request.form["model_name"]
            selected_params = request.form.getlist("params_to_add")
            # print("input params")
            # print(selected_params) 
            class_component_summary = helperMethods.get_components_summary([class_component["Name_of_component"]])
            att_summary = class_component_summary[0]["Names_of_component_atributes"]
            params_summary = helperMethods.param_summary(selected_params)

            # print(( f"Params summary {params_summary}"))
            if(len(selected_params)==len(att_summary)):
                class_component["component_atributes_names"] = params_summary
                #print(f"Class component {class_component}")
                class_components.append(class_component)
                #print(class_components)
                return render_template("add_model_tab.html",
                                       view=3, 
                                       model_type=session["model_type"], 
                                       model_name = new_model_name,
                                       all_class_components = class_components,
                                       all_components=all_components, 
                                       all_agents = helperMethods.get_components_by_name("agent"), 
                                       input_params=input_parameters)
            else:
                #print("error occured")
                return render_template("add_model_tab.html",view=2, 
                                       mmodel_type=session["model_type"], 
                                       model_name = new_model_name, 
                                       all_components=all_components, 
                                       all_agents = helperMethods.get_agents_by_type(chosen_model_type),
                                       input_params=input_parameters,
                                       error_message=f"Pick {len(att_summary)} parameter(s)")
            
            
        case "Add model agent":
            new_model_name = request.form["model_name"]
            model_agent["Name_of_agent"] = agent_to_add_to_model
            print("Selected agent to be added to model agents "+ model_agent["Name_of_agent"])
            return render_template("add_model_tab.html",
                                   view=3, 
                                   model_type=chosen_model_type, 
                                   model_name = new_model_name, 
                                   all_components=all_components, 
                                   all_agents = helperMethods.get_components_by_name("agent"),
                                   chosen_agent=agent_to_add_to_model,
                                   current_model_agents = model_agents,
                                   input_params=input_parameters)

        case "Add agent to model":
            # model_agent = {
            #     "Name_of_agent": "",
            #     "number_of_agents": ""
            # }
            
            new_model_name = request.form["model_name"]
            selected_params = request.form.getlist("params_to_add")
            #print(selected_params[0])
            model_agent["number_of_agents"] = selected_params
            # print(f"Agent {model_agent['Name_of_agent']} to be added to model with {model_agent['number_of_agents']} input parameters")
            #print(model_agent)
            model_agents.append(model_agent)
            # print(f"{model_agent} added to {model_agents}")
            
            return render_template("add_model_tab.html",
                                   view=3, 
                                   model_type=session["model_type"], 
                                   model_name = new_model_name, 
                                   all_components=all_components,
                                   current_model_agents = model_agents,
                                   all_agents = helperMethods.get_components_by_name("agent"), 
                                   input_params=input_parameters)
        case "Save agents":
            new_model_name = request.form["model_name"]
            selected_params = request.form.getlist("params_to_add")
            #print(selected_params[0])

            model_agent["number_of_agents"] = selected_params[0]
            model_agents.append(model_agent)
            #print(model_agent)
            return render_template("add_model_tab.html",
                                   view=4, 
                                   model_type=session["model_type"], 
                                   model_name = new_model_name, 
                                   all_systems=helperMethods.get_components_by_name("system"),
                                   agents_added_to_model = model_agents,
                                   input_params=input_parameters)

        case "Add system":
            # model_system={
            #     "Name_of_system": "MovementSystem",
            #     "system_id": "move",
            #     "system_variables": []
            # }
            # model_systems = []
            #print(request.form["system_id"])
            model_system["system_id"]=request.form["system_id"]
            sys_vars = request.form.getlist("param_list")
            #print(sys_vars)
            model_system["system_variables"] = sys_vars
            model_systems.append(model_system)
            return render_template("add_model_tab.html",
                                   view=4, 
                                   model_type=session["model_type"], 
                                   model_name = new_model_name, 
                                   all_systems=all_current_systems, 
                                   input_params=input_parameters)

        case "Add system to model":
            # model_system={
            #     "Name_of_system": "MovementSystem",
            #     "system_id": "move",
            #     "system_variables": []
            # }
            # model_systems = []
            new_model_name = request.form["model_name"]
            #print(f"Adding {system_to_add_to_model} to {new_model_name}")
            model_system["Name_of_system"]=system_to_add_to_model
            return render_template("add_model_tab.html",
                                   view=4, 
                                   model_type=session["model_type"], 
                                   model_name = new_model_name, 
                                   all_systems=all_current_systems, 
                                   input_params=input_parameters)
        
        case "Save systems and execute model":
            new_model_name = request.form["model_name"]
            #print(f"Adding {system_to_add_to_model} to {new_model_name}")
            model_system["Name_of_system"]=system_to_add_to_model
            

            return render_template("add_model_tab.html",
                                   view=5, 
                                   model_type=session["model_type"], 
                                   model_name = new_model_name, 
                                   all_systems=all_current_systems, 
                                   input_params=input_parameters)

    return render_template("add_model_tab.html",
                           view=1,
                           model_type=session["model_type"],
                           input_params=input_parameters)

    
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
    app.secret_key="be gay, do crime"
    app.run(host='0.0.0.0', debug=True)