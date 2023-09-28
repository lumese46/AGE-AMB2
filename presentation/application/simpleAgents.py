from .createAgents import createAgents

class simpleAgents(createAgents):
    def __init__(self, Name ,Type, Tag, ClassComponentName,Component):
        self.Name = Name
        self.ClassComponentName = ClassComponentName
        self.Tag = Tag
        self.Component = Component
        self.Type = Type

    def generateAgent(self):
        # for the complex case first
        classString = f"class {self.Name}(Core.Agent):\n"
        initString = "    def __init__(self, model"
        superString = "        super().__init__(id, model)"

        addString = ""
        add_componentStrings = []

        # component data
        for i in range(len(self.Component)):
            Name_of_component = self.Component[i]["Name_of_component"]
            Names_of_component_atributes = self.Component[i]["Names_of_component_atributes"]
            componentString = "        self.add_component(\n" + f"            {Name_of_component}(\n" + "                self, model"
            for l in range(len(Names_of_component_atributes)):
                componentString = componentString + f", {Names_of_component_atributes[l]}"
                
                initString = initString + f", {Names_of_component_atributes[l]}"
            add_componentStrings.append( componentString + "\n            )\n" + "        )\n")
        initString = initString + "):\n"

        for z in range(len(add_componentStrings)):
            addString = addString + "\n" + add_componentStrings[z]
        return classString + initString + superString +  addString
