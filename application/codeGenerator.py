from createAgentsFactory import createAgentsFactory
from createComponents import CreateComponents
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
            print(component.generateComponent())
     
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
                print(agent.generateAgent())
     def generateSystem():
            # get the data from json file 
            data = json_load('systems.json')
            # get the approriate data types for 
            for obj in data:
                Name_of_system = obj.get("Name_of_system")
                code = obj.get("code")
                print(code)


code = codeGenerator
print(code.generateAgent())


