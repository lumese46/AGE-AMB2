from createDataCollector import createDataCollector
from createAgentsFactory import createAgentsFactory
from createComponents import CreateComponents
from createModelExecute import createModelExecute
from createModel import createModel
import json
from json_loader import json_load

#### get the data needed to create agent code #####
class codeGenerator:
     def __init__(self):
         pass
     def generateComponent():
        # get the data from json file 
        data = json_load('components.json')
        # get the approriate data types for 
        for obj in data:
            global name_of_component
            global component_attributes
            name_of_component = obj.get("Name_of_component")
            component_attributes = obj.get("Component_atributes", [])

            component = CreateComponents(Name=name_of_component,POD=component_attributes)
            return component.generateComponent()
     
     def generateAgent():

            # get the data from json file 
            data = json_load('agents.json')
            # get the approriate data types for 
            for obj in data:
                Name_of_agent = obj.get("Name_of_agent")
                Class_component_name = obj.get("Class_component_name")
                Tag_of_agent = Name_of_agent.upper()
                Type_of_agent = obj.get("Type_of_agent")
                Components = obj.get("Components")
                # use the factory
                agentFactory = createAgentsFactory(Name=Name_of_agent,Type=Type_of_agent,Tag=Tag_of_agent,ClassComponentName=Class_component_name,Component=Components)
                # create agent using the factory
                agent = agentFactory.createAgentS(Type_of_agent)
                # generate agent code
                return agent.generateAgent()
     def generateSystem():
            # get the data from json file 
            data = json_load('systems.json')
            finalCode = ""
            # get the approriate data types for 
            for obj in data:
                Name_of_system = obj.get("Name_of_system")
                code = obj.get("code")
                finalCode = finalCode + "/n" +  code
            return finalCode
     def generateModel():
            # get the data from json file 
            data = json_load('modelTestReferences.json')
            for obj in data:
                if "input_parameters" in obj:
                    input_parameters = obj["input_parameters"]
                elif "name_model" in obj:
                    name_model = obj["name_model"]
                elif "class_components" in obj:
                    class_components = obj["class_components"]
                elif "Agents" in obj:
                    Agents = obj["Agents"]
                elif "environment" in obj:
                    environment = obj["environment"]
                elif "systems" in obj:
                    systems = obj["systems"]

            
            model = createModel(name_model = name_model  ,input_parameters = input_parameters,class_components = class_components,Agents=Agents,environment=environment,systems=systems)
            return model.generateModel()
     def generateDataCollector():
            
            # get the data from json file 
            data = json_load('dataCollectors.json')
            name_of_agents = data[0]["Name_of_agents"]
            dataCollector = createDataCollector(name_of_agents)
            return dataCollector.generateDataCollector()
    
     def generateModelExecute():
            # get the data from json file 
            data = json_load('executeTemplete.json')
            for obj in data:
                if "input_parameters" in obj:
                    input_parameters = obj["input_parameters"]
                elif "name_model" in obj:
                    name_model = obj["name_model"]
                elif "iterations" in obj:
                    iterations = obj["iterations"]
                elif "visualization" in obj:
                    visualization = obj["visualization"]
            modelExecute = createModelExecute(name_model = name_model  ,input_parameters = input_parameters,iterations=iterations,visualization=visualization)
            return modelExecute.generateModelExecute()
                


     





