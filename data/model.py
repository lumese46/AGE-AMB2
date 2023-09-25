
import numpy
import ECAgent.Core as Core
import ECAgent.Tags as Tags
import ECAgent.Collectors as Collectors
from ECAgent.Environments import GridWorld, PositionComponent, discrete_grid_pos_to_id
import matplotlib.pyplot as plt


class EnergyComponent(Core.Component):
    def __init__(self, agent, model):
        super().__init__(agent, model)

class SpeciesComponent(Core.Component):
    def __init__(self, agent, model):
        super().__init__(agent, model)



#Sheep Agent
class Sheep(Core.Agent):
    def __init__(self, model, energy):
        #Get ClassComponent
        comp = Sheep[EnergyComponent]
        # Create agent id
        agent_id = f'{comp.prefix}{comp.counter}'
        super().__init__(agent_id, model, tag=Tags.SHEEP)
        # Add Energy Component

        self.add_component(
            EnergyComponent(
                self, model, energy
            )
        )
        comp.counter += 1

#Wolf Agent
class Wolf(Core.Agent):
    def __init__(self, model, energy):
        #Get ClassComponent
        comp = Wolf[EnergyComponent]
        # Create agent id
        agent_id = f'{comp.prefix}{comp.counter}'
        super().__init__(agent_id, model, tag=Tags.WOLF)
        # Add Energy Component

        self.add_component(
            EnergyComponent(
                self, model, energy
            )
        )
        comp.counter += 1

class MovementSystem(Core.System):
    def __init__(self, id: str, model):
        super().__init__(id, model)

    def execute(self):
        pass
class ResourceConsumptionSystem(Core.System):
    def __init__(self, id: str, model, regrow_time: int):
        super().__init__(id, model)
        self.regrow_time = regrow_time

    def execute(self):
        pass
class DeathSystem(Core.System):
    def __init__(self, id: str, model):
        super().__init__(id, model)

    def execute(self):
        pass
class BirthSystem(Core.System):
    def __init__(self, id: str, model):
        super().__init__(id, model)

    def execute(self):
        pass
class BirthSystem(Core.System):
    def __init__(self, id: str, model):
        super().__init__(id, model)

    def execute(self):
        pass
class DataCollector(Collectors.Collector):
    def __init__(self, id: str, model):
        super().__init__(id, model)
        self.records = {'Sheep':[], 'WOLF':[], }
     # Count Sheep
        self.records['Sheep'].append(
             len(self.model.environment.get_agents(tag=Tags.SHEEP))
            )

     # Count WOLF
        self.records['WOLF'].append(
             len(self.model.environment.get_agents(tag=Tags.WOLF))
            )


class PredatorPreyModel(Core.Model):
    def __init__(self, size: int, init_sheep: int, init_wolf: int, regrow_rate: int, sheep_gain: float, wolf_gain: float, sheep_reproduce: float, wolf_reproduce: float, seed: int = None):
        super().__init__(seed=seed)

    # Create Grid World
        self.environment = GridWorld(self, size, size)

    # Add Systems
        self.systems.add_system(MovementSystem('move', self))
        self.systems.add_system(ResourceConsumptionSystem('food', self, regrow_rate))
        self.systems.add_system(BirthSystem('birth', self))
        self.systems.add_system(DeathSystem('death', self))
        self.systems.add_system(DataCollector('collector', self))

    # Add Class Components
        Sheep.add_class_component(
            SpeciesComponent(Sheep, self, 'S', sheep_gain, sheep_reproduce)
        )
        Wolf.add_class_component(
            SpeciesComponent(Wolf, self, 'W', wolf_gain, wolf_reproduce)
        )

    # Create Agents at random locations
        for _ in range(init_sheep):
            self.environment.add_agent(
                Sheep(self),
                x_pos = self.random.randint(0, size - 1),
                y_pos = self.random.randint(0, size - 1)
            )
        for _ in range(init_wolf):
            self.environment.add_agent(
                Wolf(self),
                x_pos = self.random.randint(0, size - 1),
                y_pos = self.random.randint(0, size - 1)
            )

    # Method that will execute Model for t timesteps
    def run(self, t: int):
        self.execute(t)

# Input Parameters
size = 50
init_sheep = 100
init_wolf = 50
regrow_rate = 30
sheep_gain = 4
wolf_gain = 25
sheep_reproduce = 0.04
wolf_reproduce = 0.06
seed = 345968
# Change this to change length of simulation
ITERATIONS = 1000
model = PredatorPreyModel(size ,init_sheep ,init_wolf ,regrow_rate ,sheep_gain ,wolf_gain ,sheep_reproduce ,wolf_reproduce ,seed)
# Execute model (May take some time based on input params used)
model.run(ITERATIONS)

# Get population levels from data collector
records = model.systems['collector'].records

# Create Matplotlib Plots
fig, ax = plt.subplots()
ax.set_title('Sheep and Wolf Populations in Simple Predator Prey Model')
ax.set_xlabel('Iterations')
ax.set_ylabel('Population')
iterations = numpy.arange(ITERATIONS)
for species in records:
    ax.plot(iterations, records[species], label=species)

ax.legend(loc='lower right')
ax.set_aspect('auto')
plt.show()
