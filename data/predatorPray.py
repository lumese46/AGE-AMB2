#Source
#https://ecagent.readthedocs.io/en/latest/tutorials/advanced_tutorial.html
import numpy
import ECAgent.Core as Core
import ECAgent.Tags as Tags
import ECAgent.Collectors as Collectors
from ECAgent.Environments import GridWorld, PositionComponent, discrete_grid_pos_to_id
import matplotlib.pyplot as plt




#create components
# Energy Component
class EnergyComponent(Core.Component):
    def __init__(self, agent, model, energy: float):
        super().__init__(agent, model)
        self.energy = energy  # The creatures remaining energy

# Species Class Component
class SpeciesComponent(Core.Component):
    def __init__(self, agent, model, prefix, gain, reproduce_rate):
        super().__init__(agent, model)
        # id prefix
        self.prefix = prefix
        # Energy gain for consuming food item
        self.gain = gain
        # Reproduction rate of Species
        self.reproduce_rate = reproduce_rate
        # Used to ensure agents have unique id per species
        self.counter = 0

# Add Sheep Tag
Tags.add_tag('SHEEP')
# Add Wolf Tag
Tags.add_tag('WOLF')

# Sheep Agent
class Sheep(Core.Agent):
    def __init__(self, model, energy: float = None):
        # Get SpeciesComponent
        sp_comp = Sheep[SpeciesComponent]
        # Create agent id
        agent_id = f'{sp_comp.prefix}{sp_comp.counter}'
        super().__init__(agent_id, model, tag=Tags.SHEEP)
        # Add Energy Component
        self.add_component(
            EnergyComponent(
                self, model, energy if energy is not None
                else model.random.random() * 2 * sp_comp.gain
            )
        )
        sp_comp.counter += 1

# Wolf Agent
class Wolf(Core.Agent):
    def __init__(self, model, energy: float = None):
        # Get SpeciesComponent
        wlf_comp = Wolf[SpeciesComponent]
        # Create agent id
        agent_id = f'{wlf_comp.prefix}{wlf_comp.counter}'
        super().__init__(agent_id, model, tag=Tags.WOLF)
        # Add Energy Component
        self.add_component(
            EnergyComponent(
                self, model, energy if energy is not None
                else model.random.random() * 2 * wlf_comp.gain
            )
        )
        wlf_comp.counter += 1
Tags.itemize()

class MovementSystem(Core.System):
    def __init__(self, id: str, model):
        super().__init__(id, model)

    def execute(self):
        # For each agent in the environment
        for agent in self.model.environment:
            # Move within Moore Neighbourhood [-1, 1]
            x_offset = round(2 * self.model.random.random() - 1)
            y_offset = round(2 * self.model.random.random() - 1)
            self.model.environment.move(agent, x_offset, y_offset)

            # Spend Energy
            agent[EnergyComponent].energy -= 1

class ResourceConsumptionSystem(Core.System):
    def __init__(self, id: str, model, regrow_time: int):
        super().__init__(id, model)
        self.regrow_time = regrow_time

        def resource_generator(pos, cells):
            return 1 if model.random.random() < 0.5 else 0

        # Generate the initial resources
        model.environment.add_cell_component('resources',
                                           resource_generator)

        def countdown_generator(pos, cells):
            return int(model.random.random() * regrow_time)

        # Generate the initial resources
        model.environment.add_cell_component('countdown', countdown_generator)

    def execute(self):
        # Get resources data
        cells = self.model.environment.cells
        resource_cells = cells['resources'].to_numpy()
        countdown_cells = cells['countdown'].to_numpy()
        eaten_sheep = []
        targets_at_pos = {}
        environment = self.model.environment
        # Process Sheep and Wolves first

        for agent in environment:
            posID = discrete_grid_pos_to_id(agent[PositionComponent].x, agent[PositionComponent].y,
                                            self.model.environment.width)

            # Is wolf or is sheep
            if agent.tag == Tags.WOLF:
                # Get all agents at position
                if posID not in targets_at_pos:
                    targets_at_pos[posID] = environment.get_agents_at(
                        agent[PositionComponent].x, agent[PositionComponent].y)

                for target in targets_at_pos[posID]:
                    # If sheep
                    if target.tag == Tags.SHEEP and target.id not in eaten_sheep:
                        # Mark Sheep for death
                        eaten_sheep.append(target.id)
                        # Wolf gets energy for eating Sheep
                        agent[EnergyComponent].energy += Wolf[SpeciesComponent].gain
                        break

            elif agent.id not in eaten_sheep:
                # Check is grass is Alive
                if resource_cells[posID] > 0:
                    # Sheep consumes Grass and gains Energy
                    agent[EnergyComponent].energy += Sheep[SpeciesComponent].gain
                    resource_cells[posID] = 0

        # Remove eaten sheep
        for sheep in eaten_sheep:
            environment.remove_agent(sheep)

        # Regrow Grass
        countdown_cells[resource_cells < 1] -= 1
        mask = countdown_cells < 1
        resource_cells[mask] = 1
        countdown_cells = numpy.where(mask, numpy.asarray(
        [
            int(self.model.random.random() * self.regrow_time)
            for _ in range(len(countdown_cells))
        ]), countdown_cells)

        # Update grass levels and countdowns in environment
        self.model.environment.cells.update({
            'resources': resource_cells,
            'countdown': countdown_cells
        })

class DeathSystem(Core.System):
    def __init__(self, id, model):
        super().__init__(id, model)

    def execute(self):
        toRem = []
        for agent in self.model.environment:
            if agent[EnergyComponent].energy <= 0:
                toRem.append(agent.id)

        for a in toRem:
            self.model.environment.remove_agent(a)

class BirthSystem(Core.System):
    def __init__(self, id, model):
        super().__init__(id, model)

    def execute(self):
        for agent in self.model.environment.get_agents():
            new_agent = None
            if agent.tag == Tags.WOLF and self.model.random.random() < Wolf[SpeciesComponent].reproduce_rate:
            # Birth Wolf
                agent[EnergyComponent].energy /= 2.0
                new_agent = Wolf(self.model,
                         energy=agent[EnergyComponent].energy
                    )

            elif self.model.random.random() < Sheep[SpeciesComponent].reproduce_rate:
            # Birth Sheep
                agent[EnergyComponent].energy /= 2.0
                new_agent = Sheep(self.model,
                        energy=agent[EnergyComponent].energy
                )

            # Add agent to environment (at its parent's location)
            if new_agent is not None:
                self.model.environment.add_agent(
                    new_agent, *agent[PositionComponent].xy()
                )

import ECAgent.Collectors as Collectors

class DataCollector(Collectors.Collector):
    def __init__(self, id: str, model):
        super().__init__(id, model)
        self.records = {'sheep': [], 'wolves': []}

    def collect(self):
    # Count Sheep
        self.records['sheep'].append(
            len(self.model.environment.get_agents(tag=Tags.SHEEP))
        )
    # Count Wolves
        self.records['wolves'].append(
            len(self.model.environment.get_agents(tag=Tags.WOLF))
        )

class PredatorPreyModel(Core.Model):
    def __init__(self, size: int, init_sheep: int, init_wolf: int,
        regrow_rate: int, sheep_gain: float, wolf_gain: float,
        sheep_reproduce: float, wolf_reproduce: float, seed: int = None):
        super().__init__(seed=seed)

    # Create Grid World
        self.environment = GridWorld(self, size, size)

    # Add Systems
        self.systems.add_system(MovementSystem('move', self))
        self.systems.add_system(ResourceConsumptionSystem('food',
            self, regrow_rate))
        self.systems.add_system(BirthSystem('birth', self))
        self.systems.add_system(DeathSystem('death', self))
        self.systems.add_system(DataCollector('collector', self))

    # Add Class Components
        Wolf.add_class_component(
            SpeciesComponent(Wolf, self, 'w', wolf_gain,
                             wolf_reproduce)
        )
        Sheep.add_class_component(
            SpeciesComponent(Sheep, self, 's', sheep_gain,
                             sheep_reproduce)
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


