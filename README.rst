orbitsim is a tool for visualising the orbits of satellites and spacecraft.

below is an example for plotting the orbits of 2 spacecraft

import orbitsim as orb

#initialise environment object
env = environment.Environment("Earth")

# initialise spacecraft
eng1 = orb.Engine(100)
sc1 = orb.Spacecraft(eng1)
sc1.set_state0([50e6,0.1,0,0,0,0], 'koe')

eng2 = orb.Engine(200)
sc2 = orb.Spacecraft(eng2)
sc2.set_state0([40e6,0.3,np.radians(25),0,0,0], 'koe')

# define simulation parameters
tspan = 3*24*60*60 # 1 day in seconds
dt = 600 # 10 minutes

# calcualte orbits
orb1= orb.Orbit(sc1,env,tspan,dt)
orb2 = orb.Orbit(sc2,env,tspan,dt)

# plot orbits
orb.util.plot_n_orbits([orb1,orb2],env)
