class CreateComponents:
    def __init__(self, Name, POD):
        self.Name = Name
        self.POD = POD
    
    # gets the name of component
    def getName(self):
        return self.Name
    # gets the POD of component
    def getPOD(self):
        return self.POD
    
    # generate the component code based on attributes
    def generateComponent(self):
        classString = f"class {self.Name}(Core.Component):\n"
        initString = "    def __init__(self, agent, model"
        superString = "        super().__init__(agent, model)\n"
        POD_String = [] # responsible for POD line
        for i in range(len(self.POD)):
            # fetch POD data from dict
            POD_name = self.POD[i]["name"] 
            POD_DefaultValue = self.POD[i]["DefaultValue"]
            POD_Comment = self.POD[i]["Comment"]

            # fomulate code
            if (POD_DefaultValue == "NONE"):
                initString = initString + " ," +  POD_name
                POD_String.append(f"        self.{POD_name} = {POD_name}  # {POD_Comment}\n")
            else:
                POD_String.append(f"        self.{POD_name} = {POD_DefaultValue}  # {POD_Comment}\n")

        initString = initString + "):\n"

        codeString = classString + initString + superString

        for l in range(len(POD_String)):
            codeString = codeString + POD_String[l]

        return codeString






