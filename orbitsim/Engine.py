# -*- coding: utf-8 -*-

"""Engine Class"""

__author__ = "Alexander William Minchin"

from scipy import constants as const


class Engine:
    """
    A class to repersent the engine of the spacecraft.

    ...

    Attributes
    ---------
    mass : float
        dry mass of engine (kg)
    mass_p : float
        mass of propellant (kg)
    isp : float
        the specific impulse of the engine (N*s/kg)
    thrust : float
        thrust produced by the enginer (N)
    mass_p_dot : float
        time derivative of proellant mass (kg/s)
    burnout_time : float
        time till all propellant is burnt (s)
    """

    def __init__(
            self,
            mass,
            mass_p=0,
            isp=0,
            thrust=0
    ):
        """
        Parameters
        ----------
        mass : float
            dry mass of engine (kg)
        mass_p : float
            mass of propellant (kg)
        isp : float
            the specific impulse of the engine (N*s/kg)
        thrust : float
            thrust produced by the enginer (N)

        """
        # define the engine attributes in SI units
        self.mass = mass
        self.mass_p = mass_p
        self.isp = isp
        self.thrust = thrust

        # attributes to be calculated
        if self.thrust > 0:
            self.mass_dot = self.calculate_mass_dot()
            self.burnout_time = self.calculate_burnout_time()

    def calculate_mass_dot(self):
        """ calculates and returns the time derivative of proellant mass (kg/s)"""

        #calculate m dot
        self.mass_p_dot = self.thrust / (const.g * self.isp)

        return self.mass_p_dot

    def calculate_burnout_time(self):
        """ calculates the time till all propellant is burnt (s)"""

        #calculate burnout time
        self.burnout_time = self.mass_p / self.mass_p_dot

        return self.burnout_time

    def info(self):
        """ prints information summary of the engine"""

        #print engine information
        print("\nEngine Information")
        print("Engine Mass:", self.mass, "kg")
        print("Engine Isp:", self.isp, "N*s/kg")
        print("Engine Thrust:", self.thrust, "N")
        print("Propellant Mass:", self.mass_p, "kg")
        print("Engine Burnout Time", self.burnout_time, "s")
