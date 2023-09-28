# class MoneySystem(System):
#     def __init__(self, model : Model):
#         super().__init__("MONEY", model)

#     def execute(self):

class createSystems:
    def __init__(self, Name):
        self.Name = Name
    # generate the system code based on attributes
    def generateSystem(self):
        classString = f"#this is {self.Name} System\n"
        classString = classString + f"class {self.Name}(Core.System):\n"
        initString = f"    def __init__(self, id, model):\n"
        superString = f"        super().__init__(id, model)\n"
        executeString = f"    def execute(self):\n        pass\n\n"
        codeString = classString + initString + superString + executeString
        return codeString
#oratile = CreateSystems("ORATILE")
#print(oratile.generateSystem())
    