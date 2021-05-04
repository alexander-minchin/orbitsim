# -*- coding: utf-8 -*-

"""Spacecraft Class"""

__author__ = "Alexander William Minchin"


class Spacecraft:
    """
    A class to repersent the spacecraft in orbit.

    ...

    Attributes
    ---------
    mass : float
        structural mass of spacecraft (kg)
    engine : Engine
        the engine that is used by the spacecraft
    drag_coeff : float
        the coefficient of drag for the spacecraft
    area : float
        the cross sectional area of the spacecraft (m^2)
    state0 : array
        state vector containing the initial 3D position and velocities
        [x,y,z,u,v,w]       [(m),(m),(m),(m/s),(m/s),(m/s)]
    mass_total : float
        total mass of the spacecraft including engine and propellant (kg)
    """

    def __init__(
            self,
            mass=3000.0,
            engine,
            drag_coeff=2.2,
            area=6.0,
            state0
    ):
        """
        Parameters
        ----------
        mass : float
            mass of spacecraft without fuel loaded (kg)
        engine : Engine
            the engine that is used by the spacecraft
        drag_coeff : float
            the coefficient of drag for the spacecraft (-)
        area : float
            the cross sectional area of the spacecraft (m^2)
        state0 : array
            state vector containing the initial 3D position and velocities
            [x,y,z,u,v,w]       [(m),(m),(m),(m/s),(m/s),(m/s)]
        environment : Environment
        """
        # define the spacecraft attributes in SI units
        self.mass = mass
        self.engine = engine
        self.drag_coeff = drag_coeff
        self.area = area
        self.state0 = state0

        #attributed to be calculated
        self.mass_total = self.calculate_total_mass()

    def calculate_total_mass(self):
        """ calculates and returns the total mass of the spacecraft
        including engine mass and propellant mass"""

        #calcualte mass by summing spacecraft, engine and propellant masses
        self.mass_total = self.mass + self.engine.mass + self.engine.mass_p

        return self.mass_total

    def info(self):
        """ prints information summary of the engine"""

        #print engine information
        print("\nSpacecraft Information")
        print("Spacecraft Mass:", self.mass, "kg")
        print("Spacecraft Cd:", self.drag_coeff, "N*s/kg")
        print("Spacecraft Cross-sectional Area:", self.area, "N")
        print("Spacecraft Total Mass:", self.mass_total, "kg")
        print("Spacecraft Orbital State Vector", self.state0, "s")
