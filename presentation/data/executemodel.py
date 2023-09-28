import matplotlib.pyplot as plt
import numpy
import predatorPray

from functools import partial


# Input Parameters
ENV_SIZE = 20
INIT_SHEEP = 200
INIT_WOLF = 10
REGROW_RATE = 60
SHEEP_GAIN = 8
WOLF_GAIN = 55
SHEEP_REPRODUCTION = 0.08
WOLF_REPRODUCTION = 0.06

# Change this to change length of simulation
ITERATIONS = 5
SEED = 345968  # For pseudo-random number generator

model = predatorPray.PredatorPreyModel(
ENV_SIZE,
INIT_SHEEP,
INIT_WOLF,
REGROW_RATE,
SHEEP_GAIN,
WOLF_GAIN,
SHEEP_REPRODUCTION,
WOLF_REPRODUCTION,
SEED)

# Execute model (May take some time based on input params used)
model.run(ITERATIONS)

# Get population levels from data collector
records = model.systems['collector'].records

# Create Matplotlib Plots
fig, ax = plt.subplots()
ax.set_title('Sheep and Wolf Populations in \nSimple Predator Prey Model')
ax.set_xlabel('Iterations')
ax.set_ylabel('Population')

iterations = numpy.arange(ITERATIONS)

print(records)



