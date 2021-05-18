# -*- coding: utf-8 -*-

"""Orbit Class"""

import numpy as np
from scipy.integrate import ode
import pyatmos as atm
import mayavi as mya

from . import util as ut

class Orbit:
    """
    A class to repersent the orbit of the spacecraft.

    ...

    Attributes
    ---------
    spacecraft : Spacecraft
        the spacecraft that will have its orbit calculated
    environment : Environment
        the environment settings for the simulation
    tspan : int
        span of time that the simulation runs for
    dt : int
        time step for the simulation
    """

    def __init__(
            self,
            spacecraft,
            environment,
            tspan,
            dt
    ):
        self.spacecraft = spacecraft
        self.environment = environment
        self.tspan = tspan
        self.dt = dt

        # convert keplerian orbital elements to orbital state vector if necessary
        if self.spacecraft.state_format == 'koe':
            self.spacecraft.set_state0(ut.koe_to_osv(
                self.spacecraft.state0,self.environment.cb_mu))

        # calculate number of steps required
        self.n_steps = int(np.ceil(self.tspan/self.dt))

        # allocate memory for time and state arrays
        self.ts = np.zeros((self.n_steps,1))
        self.ys = np.zeros((self.n_steps,6))

        # initial conditions
        self.ys[0] = self.spacecraft.state0
        self.step = 1

        # set up solver
        self.solver = ode(self.diff_y)
        self.solver.set_integrator('lsoda')
        self.solver.set_initial_value(self.ys[0],self.ts[0])

        self.solve_orbit()


    def solve_orbit(self):
        # propagate the orbit
        while self.solver.successful() and self.step < self.n_steps:
            self.solver.integrate(self.solver.t+self.dt)
            self.ts[self.step] = self.solver.t
            self.ys[self.step] = self.solver.y
            self.step+=1

        self.rs = self.ys[:,:3]
        self.vs = self.ys[:,3:]


    def diff_y(self,t,y):

        r = y[:3]
        v = y[3:]
        r_norm = np.linalg.norm(r)

        # two body acceleration
        a = -r*self.environment.cb_mu / r_norm**3

        # constant thrust
        if "thrust" in self.environment.perturbations:
            v_dir = v/np.linalg.norm(v)
            a_thrust = v_dir * self.spacecraft.engine.thrust/self.spacecraft.mass_total

            a+= a_thrust

        # aerodynamic drag
        if 'aero' in self.environment.perturbations:
            #calculate air density
            z = r_norm - self.environment.cb_radius  # km

            rho = atm.coesa76(z)[0][0]*1e9  # kg / km^3

            #calculate motion of s/c wrt a rotating atmosphere
            v_rel = v - np.cross(self.environment.cb_atm_rot,r)

            drag = 0.5 * rho * v_rel*np.linalg.norm(v_rel) * self.spacecraft.drag_coeff\
            * self.spacecraft.area / self.spacecraft.mass_total

            a += drag

        # J2 perturbation
        if 'J2' in self.environment.perturbations:

            z2 = r[2]**2
            r2 = r_norm**2
            tx = r[0] / r_norm*(5*z2/r2 -1)
            ty = r[1] / r_norm*(5*z2/r2 -1)
            tz = r[2] / r_norm*(5*z2/r2 -3)

            a_j2 = 1.5*self.environment.cb_J2*self.environment.cb_mu\
            * self.environment.cb_radius**2 / r_norm**4 * np.array([tx, ty, tz])

            a += a_j2

        return np.concatenate([v,a])

        def plot_orbits(self,orbits):
            ut.plot_n_orbits(orbits,self.environment)

