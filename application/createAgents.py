from abc import ABC, abstractmethod

# Define an interface for shapes
class createAgents(ABC):
    @abstractmethod
    def generateAgent(self):
        pass



# class CreateAgents:
#     def __init__(self, Name ,Type, Tag, ClassComponentName,Component):
#         self.Name = Name
#         self.ClassComponentName = ClassComponentName
#         self.Tag = Tag
#         self.Component = Component
#         self.Type = Type

#     def generateAgentSimple(self):
#         # for the complex case first
#         classString = f"class {self.Name}(Core.Agent):\n"
#         initString = "    def __init__(self, model"
#         superString = "        super().__init__(id, model)"

#         addString = ""
#         add_componentStrings = []

#         # component data
#         for i in range(len(self.Component)):
#             Component_classname = self.Component[i]["classname"]
#             POD_names_array = self.Component[i]["POD_names_array"]
#             componentString = "        self.add_component(\n" + f"            {Component_classname}(\n" + "                self, model"
#             for l in range(len(POD_names_array)):
#                 componentString = componentString + f", {POD_names_array[l]}"
                
#                 initString = initString + f", {POD_names_array[l]}"
#             add_componentStrings.append( componentString + "\n            )\n" + "        )\n")
#         initString = initString + "):\n"

#         for z in range(len(add_componentStrings)):
#             addString = addString + "\n" + add_componentStrings[z]
#         return classString + initString + superString +  addString
         
            

#     def generateAgent(self):
#             if self.Type == "COMPLEX":
#                 # for the complex case first
#                 classString = f"class {self.Name}(Core.Agent):\n"
#                 initString = "    def __init__(self, model"
#                 compString = f"        comp = {self.Name}[{self.ClassComponentName}]\n"
#                 agent_idString = """        agent_id = f'{comp.prefix}{comp.counter}'\n"""
#                 superString = f"        super().__init__(agent_id, model, tag=Tags.{self.Tag})\n"
#                 counterString = f"        comp.counter += 1"
#                 addString = ""
#                 add_componentStrings = []

#                 # component data
#                 for i in range(len(self.Component)):
#                     Component_classname = self.Component[i]["classname"]
#                     POD_names_array = self.Component[i]["POD_names_array"]
#                     componentString = "        self.add_component(\n" + f"            {Component_classname}(\n" + "                self, model"
#                     for l in range(len(POD_names_array)):
#                         componentString = componentString + f", {POD_names_array[l]}"
                        
#                         initString = initString + f", {POD_names_array[l]}"
#                     add_componentStrings.append( componentString + "\n            )\n" + "        )\n")
#                 initString = initString + "):\n"

#                 for z in range(len(add_componentStrings)):
#                     addString = addString + "\n" + add_componentStrings[z]

#                 # print final string
#                 codeString = classString + initString 
#                 codeString = codeString +  f"        #Get ClassComponent\n" + compString
#                 codeString = codeString + "        # Create agent id\n" + agent_idString + superString
#                 codeString = codeString + "        # Add Energy Component\n" + addString + counterString
#                 return codeString
#             else:
#                 return




