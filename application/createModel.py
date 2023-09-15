input_parameters = [
        {
            "name": "init_wolf",
            "dataType": "int"
        },
        {
            "name": "init_sheep",
            "dataType": "int"
        }
    ]
class_components = [
        {
            "Name_of_agent": "Sheep",
            "Name_of_component": "SpeciesComponent",
            "component_atributes_names": [
                "sheep_gain",
                "sheep_reproduce"
            ]
        },
        {
            "Name_of_agent": "Wolf",
            "Name_of_component": "SpeciesComponent",
            "component_atributes_names": [
                "wolf_gain",
                "wolf_reproduce"
            ]
        }
    ]
Agents =  [
        {
            "Name_of_agent": "Sheep",
            "number_of_agents": "init_sheep"
        },
        {
            "Name_of_agent": "Wolf",
            "number_of_agents": "init_wolf"
        }
    ]
environment =  "GRIDWORLD"
systems =  [
        {
            "Name_of_system": "MovementSystem",
            "system_variables": []
        },
        {
            "Name_of_system": "ResourceConsumptionSystem",
            "system_variables": [
                "regrow_rate"
            ]
        },
        {
            "Name_of_system": "BirthSystem",
            "system_variables": []
        },
        {
            "Name_of_system": "DeathSystem",
            "system_variables": []
        }
    ]



def  addSystems(systems):
    pass


def addEnvironment(environment):

    if environment == "GRIDWORLD":
        codeString = "      self.environment = GridWorld(self, size, size)"
    return codeString


def addAgents(Agents):
    codeString = ""
    for i in range(len(Agents)):
        Name_of_agent = Agents[i]["Name_of_agent"]
        number_of_agents = Agents[i]["number_of_agents"]
        stringFor = f"        for _ in range({number_of_agents}):\n"
        stringSelf = f"            self.environment.add_agent(\n"
        stringAgent = f"                {Name_of_agent}(self),\n"
        stringXpos = f"                x_pos = self.random.randint(0, size - 1),\n"
        stringYpos = f"                y_pos = self.random.randint(0, size - 1)\n"
        stringend = f"            )\n"
        codeString = codeString + stringFor + stringSelf + stringAgent + stringXpos + stringYpos + stringend

    return codeString


def  addClassComponents(class_components):
    codeString = ""
    for i in range(len(class_components)):
        Name_of_agent = class_components[i]["Name_of_agent"]
        Name_of_component = class_components[i]["Name_of_component"]
        component_atributes_names = class_components[i]["component_atributes_names"]

        stringAdd = f"        {Name_of_agent}.add_class_component(\n"
        stringComp = f"            {Name_of_component}({Name_of_agent}, self, " + "\'"+f"{Name_of_agent[0]}" + "\'" +", "
        stringClose = f"        )\n"
        for x in range(len(component_atributes_names)):
            attribute = component_atributes_names[x]
            if x == len(component_atributes_names)-1:

                stringComp = stringComp  + attribute + ")\n"
            else:
                stringComp = stringComp  + attribute  + ", "
        codeString = codeString + stringAdd + stringComp + stringClose
    return codeString


def inputPrameters(input_parameters):
    stringdef = f"    def __init__(self, "
    for i in range(len(input_parameters)):
        # fetch  data from dict
        name = input_parameters[i]["name"]
        dataType = input_parameters[i]["dataType"] 
        stringdef = stringdef +f"{name}: {dataType}, "
    stringdef = stringdef + f"seed: int = None):\n"
    stringinit = "       super().__init__(seed=seed)\n"
    codeString = stringdef + stringinit

    return codeString
#print(inputPrameters(input_parameters))
#print(addClassComponents(class_components))
#print(addAgents(Agents))
#print(addEnvironment(environment))
