from createComponents import CreateComponents
from createAgents import CreateAgents
import json
from json_loader import json_load

#### get the data needed to create agent code #####

# get the data from json file 
data = json_load('text.json')

# get the approriate data types for 
for obj in data:
    global name_of_component
    global component_attributes
    name_of_component = obj.get("Name_of_component")
    component_attributes = obj.get("Component_atributes", [])

    component = CreateComponents(Name=name_of_component,POD=component_attributes)
    print(component.generateComponent())


 





# Name1 = "Sheep"
# Tag1 = Name1.upper()
# ClassComponentName1 = "SpeciesComponent"
# Component1 = [
#     {
#         "classname" : "EnergyComponent" ,
#         "POD_names_array" : ["energy"],
#     }        
# ] #list of all the components you want to add
# Type1 = "COMPLEX"




# agent = CreateAgents(Name=Name1,Type=Type1,Tag=Tag1,ClassComponentName=ClassComponentName1,Component=Component1)
# print(agent.generateAgentSimple())
# #component = CreateComponents(Name=Name1,POD=POD1)
# #print(component.generateComponent())