

import environment, engine, spacecraft, orbit 

if __name__ == '__main__':
	
	#initialise objects
	environment = environment.Environment("Earth")
	engine = engine.Engine(100)
	spacecraft = spacecraft.Spacecraft(engine)
	spacecraft.set_state0([50e6,0.1,0,0,0,0], 'koe')

	tspan = 24*60*60 #1 day in seconds
	dt = 60 # 1 minute
	orbit = orbit.Orbit(spacecraft,environment,tspan,dt)