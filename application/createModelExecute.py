class createModelExecute:
    def __init__(self,name_model ,input_parameters,iterations,visualization):
        self.name_model = name_model
        self.input_parameters = input_parameters
        self.iterations = iterations
        self.visualization = visualization
    
    def inputString(self):
        inputString = "# Input Parameters\n"
        for obj in self.input_parameters:
            Name =obj["name"]
            Input = obj["input"]
            inputString = inputString + f'{Name} = {Input}\n'
        return inputString
    
    def iterationString(self):
        iterationString = f"# Change this to change length of simulation\n"
        iterationString = iterationString + f"ITERATIONS = {self.iterations}\n"
        return iterationString
    
    def modelinnitString(self):
        modelinnitString = f"model = {self.name_model}("
        counter = 0
        for obj in self.input_parameters:
            Name =obj["name"]
            if counter == 0 :
                modelinnitString = modelinnitString + f"{Name}"
                counter = counter + 1
            else:
                modelinnitString = modelinnitString + f" ,{Name}"
        modelinnitString = modelinnitString + ")\n"
        return modelinnitString
    
    def visualString(self):
        visualString = ""
        modelrunString = "# Execute model (May take some time based on input params used)\n"
        modelrunString = modelrunString + "model.run(ITERATIONS)\n"
        
        recordsString = "\n# Get population levels from data collector\n" + f"records = model.systems['collector'].records\n"

        set_title = self.visualization["set_title"]
        set_xlabel = self.visualization["set_xlabel"]
        set_ylabel =  self.visualization["set_ylabel"]

        matplotString = "\n# Create Matplotlib Plots\n" + "fig, ax = plt.subplots()\n" 
        matplotString = matplotString + f"ax.set_title(\'{set_title}\')\n" + f"ax.set_xlabel(\'{set_xlabel}\')\n" + f"ax.set_ylabel(\'{set_ylabel}\')"

        lastString = "\niterations = numpy.arange(ITERATIONS)\n"
        lastString = lastString + "for species in records:\n" + "    ax.plot(iterations, records[species], label=species)\n"
        lastString = lastString + "\nax.legend(loc='lower right')\n" + "ax.set_aspect('auto')\n" + "plt.show()\n"
        







        return modelrunString + recordsString + matplotString + lastString 
    
    def generateModelExecute(self):
        codeString = ""
        inputString = self.inputString()
        iterationString = self.iterationString()
        modelinnitString = self.modelinnitString()
        visualString = self.visualString()
        codeString = inputString + iterationString + modelinnitString + visualString

        return codeString
        

