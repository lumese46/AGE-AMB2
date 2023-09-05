from simpleAgents import simpleAgents
from complexAgents import complexAgents

Name1 = "Sheep"
Tag1 = Name1.upper()
ClassComponentName1 = "SpeciesComponent"
Component1 = [
    {
        "classname" : "EnergyComponent" ,
        "POD_names_array" : ["energy"],
    }        
] #list of all the components you want to add
Type1 = "COMPLEX"




agent = complexAgents(Name=Name1,Type=Type1,Tag=Tag1,ClassComponentName=ClassComponentName1,Component=Component1)
print(agent.generateAgent())
#print(agent.generateAgentComplex())
#component = CreateComponents(Name=Name1,POD=POD1)
#print(component.generateComponent())