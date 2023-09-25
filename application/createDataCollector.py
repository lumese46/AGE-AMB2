class createDataCollector:
    def __init__(self, Name_of_agents):
        self.Name_of_agents = Name_of_agents

    def generateDataCollector(self):
        codeString = ""
        self_records_string = f"{{"
        countStrings = []
        for l in range(len(self.Name_of_agents)):
            countString = ""
            name = self.Name_of_agents[l]
            self_records_string = self_records_string + "\'"+f"{name}" + "\':[], "
            name = str(name)
            Tag = name.upper()
            # create a count code 
            countString = countString + f"     # Count {name}\n"
            countString = countString + f"        self.records[" + "\'"+f"{name}" + "\'" +f"].append(\n"
            countString = countString + f"             len(self.model.environment.get_agents(tag=Tags.{Tag}))\n"
            countString = countString + f"            )\n"
            countStrings.append(countString)

            
        self_records_string = self_records_string + f"}}"
        # create final code string
        codeString = codeString + f"class DataCollector(Collectors.Collector):\n"
        codeString = codeString + f"    def __init__(self, id: str, model):\n"
        codeString = codeString + f"        super().__init__(id, model)\n"
        codeString = codeString + f"        self.records = " + self_records_string + "\n"
        for x in range(len(countStrings)):
            codeString = codeString + countStrings[x] + "\n"
        return codeString




