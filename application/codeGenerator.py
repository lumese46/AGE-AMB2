from createComponents import CreateComponents
from createAgents import createAgents
from simpleAgents import simpleAgents
from complexAgents import complexAgents
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

# get the data from json file 
data = json_load('agents.json')
# get the approriate data types for 
for obj in data:
    Name_of_agent = obj.get("Name_of_agent")
    Class_component_name = obj.get("Class_component_name")
    Tag_of_agent = Name_of_agent.upper()
    Type_of_agent = obj.get("Type_of_agent")
    Components = obj.get("Components")
    agent = simpleAgents(Name=Name_of_agent,Type=Type_of_agent,Tag=Tag_of_agent,ClassComponentName=Class_component_name,Component=Components)
    print(agent.generateAgent())
print(Name_of_agent,Class_component_name,Type_of_agent,Components)


