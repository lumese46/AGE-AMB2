
from .createDataCollector import createDataCollector
from .createAgentsFactory import createAgentsFactory
from .createComponents import CreateComponents
from .createModelExecute import createModelExecute
from .createModel import createModel
import json
from .json_loader import json_load

#### get the data needed to create agent code #####
class codeGenerator:
     def __init__(self):
         pass
     def generateComponent(self):
        # get the data from json file 
        data = json_load('component')
        componentString = ""
        # get the approriate data types for 
        for obj in data:
            name = obj['Name_of_component']
            attributes = obj['Component_attributes']
            component = CreateComponents(name, attributes)
            componentString = componentString + "\n" + component.generateComponent()
        return componentString
     
     def generateAgent(self):

            # get the data from json file 
            data = json_load('agent')
            # get the approriate data types for
            agentCode = "" 
            for obj in data:
                Name_of_agent = obj.get("Name_of_agent")
                Class_component_name = obj.get("Class_component_name")
                Tag_of_agent = Name_of_agent.upper()
                Type_of_agent = obj.get("Type_of_agent")
                Components = obj.get("Components")[0]
                # use the factory
                agentFactory = createAgentsFactory(Name=Name_of_agent,Type=Type_of_agent,Tag=Tag_of_agent,ClassComponentName=Class_component_name,Component=Components)
                # create agent using the factory
                agent = agentFactory.createAgentS(Type_of_agent)
                # generate agent code
                agentCode = agentCode + f"\n\n#{Name_of_agent} Agent\n" + agent.generateAgent()
            return agentCode + "\nTags.itemize()\n"
     def generateSystem(self):
            # get the data from json file 
            data = json_load('system')
            finalCode = ""
            # get the approriate data types for 
            for obj in data:
                Name_of_system = obj.get("Name_of_system")
                code = obj.get("code")
                finalCode = finalCode +  code
            return finalCode
     def generateModel(self):
            # get the data from json file 
            data = json_load('model')
            for obj in data[0]:
                if "input_parameters" in obj:
                    input_parameters = obj["input_parameters"]
                elif "name_model" in obj:
                    name_model = obj["name_model"]
                elif "class_components" in obj:
                    class_components = obj["class_components"]
                elif "Agents" in obj:
                    Agents = obj["Agents"]
                elif "environment" in obj:
                    environment = obj["environment"]
                elif "systems" in obj:
                    systems = obj["systems"]

            
            model = createModel(name_model = name_model  ,input_parameters = input_parameters,class_components = class_components,Agents=Agents,environment=environment,systems=systems)
            return model.generateModel()
     def generateDataCollector(self):
            
            # get the data from json file  
            data = json_load('dataCollector')  
            name_of_agents = data[0]["Name_of_agents"]
            dataCollector = createDataCollector(name_of_agents)
            return dataCollector.generateDataCollector()
    
     def generateModelExecute(self):
            # get the data from json file 
            data = json_load('executeTemplete')
            for obj in data:
                if "input_parameters" in obj:
                    input_parameters = obj["input_parameters"]
                elif "name_model" in obj:
                    name_model = obj["name_model"]
                elif "iterations" in obj:
                    iterations = obj["iterations"]
                elif "visualization" in obj:
                    visualization = obj["visualization"]
            modelExecute = createModelExecute(name_model = name_model  ,input_parameters = input_parameters,iterations=iterations,visualization=visualization)
            return modelExecute.generateModelExecute()
     def generateStandAloneModelCode(self):
          importString = '''
import numpy
import ECAgent.Core as Core
import ECAgent.Tags as Tags
import ECAgent.Collectors as Collectors
from ECAgent.Environments import GridWorld, PositionComponent, discrete_grid_pos_to_id
import matplotlib.pyplot as plt
'''       
          generateComponent = self.generateComponent()
          generateAgent = self.generateAgent()
          generateSystem = self.generateSystem()
          generateDataCollector = self.generateDataCollector()
          generateModel = self.generateModel()
          generateModelExecute = self.generateModelExecute()
          return importString + "\n" + generateComponent + "\n" + generateAgent + "\n" + generateSystem + "\n" + generateDataCollector + "\n" + generateModel + "\n" + generateModelExecute
                
# Create an instance of CodeGenerator
code = codeGenerator()

# Call the method on the instance
# print(code.generateAgent())

     





