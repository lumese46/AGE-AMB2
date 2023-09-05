
from simpleAgents import simpleAgents
from complexAgents import complexAgents
# Create a agentcodeFactory that creates different shapes
class createAgentsFactory:
    def __init__(self, Name,Type,Tag,ClassComponentName,Component):
        self.Name = Name
        self.Type = Type
        self.Tag = Tag
        self.ClassComponentName = ClassComponentName
        self.Component = Component

    def createAgentS(self,agent_type):
        if agent_type == "COMPLEX":
            return complexAgents(Name=self.Name,Type=self.Type,Tag=self.Tag,ClassComponentName=self.ClassComponentName,Component=self.Component)
        elif agent_type == "SIMPLE":
            return simpleAgents(Name=self.Name,Type=self.Type,Tag=self.Tag,ClassComponentName=self.ClassComponentName,Component=self.Component)
        else:
            raise ValueError("Invalid shape type")
