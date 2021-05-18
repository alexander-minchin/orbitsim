

from .Environment import Environment
from .Engine import Engine
from .Spacecraft import Spacecraft
from .Orbit import Orbit

import util as t
import numpy as np

if __name__ == '__main__':
	
	#initialise environment object
	env = environment.Environment("Earth")

	# initialise spacecraft
	eng1 = engine.Engine(100)
	sc1 = spacecraft.Spacecraft(eng1)
	sc1.set_state0([50e6,0.1,0,0,0,0], 'koe')

	eng2 = engine.Engine(200)
	sc2 = spacecraft.Spacecraft(eng2)
	sc2.set_state0([40e6,0.3,np.radians(25),0,0,0], 'koe')

	# define simulation parameters
	tspan = 3*24*60*60 # 1 day in seconds
	dt = 600 # 10 minutes

	# calcualte orbits
	orb1= orbit.Orbit(sc1,env,tspan,dt)
	orb2 = orbit.Orbit(sc2,env,tspan,dt)

	# plot orbits
	t.plot_n_orbits([orb1,orb2],env)