from createComponents import CreateComponents
from createAgents import CreateAgents

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




agent = CreateAgents(Name=Name1,Type=Type1,Tag=Tag1,ClassComponentName=ClassComponentName1,Component=Component1)
print(agent.generateAgentSimple())
#component = CreateComponents(Name=Name1,POD=POD1)
#print(component.generateComponent())