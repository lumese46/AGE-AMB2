import numpy
import ECAgent.Core as Core
import ECAgent.Tags as Tags
import ECAgent.Collectors as Collectors
from ECAgent.Environments import GridWorld, PositionComponent, discrete_grid_pos_to_id
import matplotlib.pyplot as plt



class comp_name(Core.Component):
    def __init__(self, agent, model, at_name):
        super().__init__(agent, model)
        self.at_name = at_name #at_desc

class comp_name(Core.Component):
    def __init__(self, agent, model):
        super().__init__(agent, model)
        self.at_name = at_val #at_desc



#This Model code
class predatorpray(Core.Model):
    def __init__(self, new param: int, seed: int = None):
        super().__init__(seed=seed)

    # Create Grid World
        self.environment = GridWorld(self, size, size)

    # Add Systems
        self.systems.add_system(Lumese('ghf', self, new param))

    # Add Class Components
        Sheep.add_class_component(
            comp_name(Sheep, self, 'S', new param)
        )

    # Create Agents at random locations
        for _ in range(new param):
            self.environment.add_agent(
                Sheep(self),
                x_pos = self.random.randint(0, size - 1),
                y_pos = self.random.randint(0, size - 1)
            )

    # Method that will execute Model for t timesteps
    def run(self, t: int):
        self.execute(t)

# Input Parameters
new param = 1
# Change this to change length of simulation
ITERATIONS = 1
model = predatorpray(new param)
# Execute model (May take some time based on input params used)
model.run(ITERATIONS)

# Get population levels from data collector
records = model.systems['collector'].records

# Create Matplotlib Plots
fig, ax = plt.subplots()
ax.set_title('gvhfhg')
ax.set_xlabel('hegdyeud')
ax.set_ylabel('hyfdtuwedf')
iterations = numpy.arange(ITERATIONS)
for species in records:
    ax.plot(iterations, records[species], label=species)

ax.legend(loc='lower right')
ax.set_aspect('auto')
plt.show()

        
        