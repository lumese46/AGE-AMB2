class createModel:
    def __init__(self,name_model ,input_parameters,class_components,Agents,environment,systems):
        self.name_model = name_model
        self.input_parameters = input_parameters
        self.class_components = class_components
        self.Agents = Agents
        self.environment = environment
        self.systems = systems
        


    def  addSystems(self):
        codeString = ""
        for i in range(len(self.systems)):
            Name_of_system = self.systems[i]["Name_of_system"]
            system_id = self.systems[i]["system_id"]
            system_variables = self.systems[i]["system_variables"]
            stringSys = f"        self.systems.add_system({Name_of_system}("+ "\'"+f"{system_id}" + "\'" +", self"
            if system_variables != []:
                for x in range(len(system_variables)):
                    system_var = system_variables[x]
                    stringSys = stringSys + ", " + system_var
            stringSys = stringSys + "))\n"
            codeString = codeString +stringSys
        return codeString


    def addEnvironment(self):

        if self.environment == "GRIDWORLD":
            codeString = "        self.environment = GridWorld(self, size, size)\n"
        return codeString


    def addAgents(self):
        codeString = ""
        for i in range(len(self.Agents)): 
            Name_of_agent = self.Agents[i]["Name_of_agent"]
            number_of_agents = self.Agents[i]["number_of_agents"]
            stringFor = f"        for _ in range({number_of_agents}):\n"
            stringSelf = f"            self.environment.add_agent(\n"
            stringAgent = f"                {Name_of_agent}(self),\n"
            stringXpos = f"                x_pos = self.random.randint(0, size - 1),\n"
            stringYpos = f"                y_pos = self.random.randint(0, size - 1)\n"
            stringend = f"            )\n"
            codeString = codeString + stringFor + stringSelf + stringAgent + stringXpos + stringYpos + stringend

        return codeString


    def  addClassComponents(self):
        codeString = ""
        for i in range(len(self.class_components)):
            Name_of_agent = self.class_components[i]["Name_of_agent"]
            Name_of_component = self.class_components[i]["Name_of_component"]
            component_atributes_names = self.class_components[i]["component_atributes_names"]

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


    def inputPrameters(self):
        stringdef = f"    def __init__(self, "
        for i in range(len(self.input_parameters)):
            # fetch  data from dict
            name = self.input_parameters[i]["name"]
            dataType = self.input_parameters[i]["dataType"] 
            stringdef = stringdef +f"{name}: {dataType}, "
        stringdef = stringdef + f"seed: int = None):\n"
        stringinit = "        super().__init__(seed=seed)\n"
        codeString = stringdef + stringinit

        return codeString

    def generateModel(self):
        codeString = ""
        stringclass  = f"class {self.name_model}(Core.Model):\n"
        stringparameters = self.inputPrameters()
        codeString = codeString + stringclass +stringparameters

        stringenv = self.addEnvironment()
        codeString = codeString + "\n    # Create Grid World\n" + stringenv

        stringsys = self.addSystems()
        codeString = codeString + "\n    # Add Systems\n" + stringsys

        stringcomps = self.addClassComponents()
        codeString = codeString + "\n    # Add Class Components\n" + stringcomps

        stringagent = self.addAgents()
        codeString = codeString + "\n    # Create Agents at random locations\n" + stringagent

        
        codeString = codeString + "\n    # Method that will execute Model for t timesteps\n"
        codeString = codeString + "    def run(self, t: int):\n"
        codeString = codeString + "        self.execute(t)\n"


        return codeString
    
    

#print(inputPrameters(input_parameters))
#print(addClassComponents(class_components))
#print(addAgents(Agents))
#print(addEnvironment(environment))
#print(addSystems(systems))

# print(generateModel(name_model ,input_parameters,class_components,Agents,environment,systems))
