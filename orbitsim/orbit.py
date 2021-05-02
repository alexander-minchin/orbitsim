import numpy as np
from scipy.integrate import ode
from . import tools as t
import pyatmos as atm
import mayavi as mya

class OrbitSolver:

	def __init__(self,y0,tspan,dt,koe=True,deg=True,cb=cb.earth):

		self.tspan = tspan
		self.dt = dt
		self.cb = cb
		self.deg = deg

		# convert keplerian orbital elements to orbital state vector if necessary
		if koe:
			y0 = t.koe_to_osv(y0, deg=deg, mu=cb['mu'])

		# calculate number of steps required
		n_steps = int(np.ceil(tspan/dt))

		# allocate memory for time and state arrays
		ts = np.zeros(n_steps,1)
		ys = np.zeros(n_steps,6)

		# initial conditions
		ys[0] = y0
		step = 1

		# set up solver
		solver = ode(diff_y).set_integrator('lsoda')
		solver.set_initial_value(y0,ts[0])

		solve.orbit()

	def diff_y(self,t,y):

		r = y[:3]
		v = y[3:]
		r_norm = np.linalg.norm(r)

		# two body acceleration
		a = -r*self.cb['mu'] / r_norm**3

		# constant thrust
			if self.perts['constant_thrust']:
				v_dir = v/np.linalg.norm(v)
				a_thrust = 6e-5*v_dir

				a+= a_thrust

		# aerodynamic drag
		if self.perts['aero']:
			#calculate air density
			z = r_norm - self.cb['radius']	# km

			rho = atm.coesa76(z)[0][0]*1e9	# kg / km^3

			#calculate motion of s/c wrt a rotating atmosphere
			v_rel = v - np.cross(self.cb['atm_rot_vec'],r)

			drag = 0.5 * rho * v_rel*np.linalg.norm(v_rel) * spacecraft.Cd
				 * spacecraft.A / self.mass

			a += drag

		# J2 perturbation
		if self.perts['J2']:

			z2 = r[2]**2
			r2 = r_norm**2
			tx = r[0] / r_norm*(5*z2/r2 -1)
			ty = r[1] / r_norm*(5*z2/r2 -1)
			tz = r[2] / r_norm*(5*z2/r2 -3)

			a_j2 = 1.5*self.cb['J2']*self.cb['mu'] * self.cb['radius']**2
				 / r_norm**4 * np.array([tx, ty, tz])

			a += a_j2

		return v + a