import json

class CreateComponents:
    def __init__(self, name, component_attributes):
        self.name = name
        self.component_attributes = component_attributes
    
    def generateComponent(self):
        class_string = f"class {self.name}(Core.Component):\n"
        init_string = f"    def __init__(self, agent, model{self.generate_init_params()}):\n"
        super_string = "        super().__init__(agent, model)\n"
        attributes_string = self.generate_attributes()
        return class_string + init_string + super_string + attributes_string

    def generate_init_params(self):
        params = ""
        for attribute in self.component_attributes:
            default_value = attribute['default_value']
            if default_value == "NONE":
                params += f", {attribute['name']}"
        return params

    def generate_attributes(self):
        attributes_string = ""
        for attribute in self.component_attributes:
            default_value = attribute['default_value']
            if default_value == "NONE":
                attributes_string += f"        self.{attribute['name']} = {attribute['name']} #{attribute['description']}\n"
            else:
                attributes_string += f"        self.{attribute['name']} = {default_value} #{attribute['description']}\n"
        return attributes_string









