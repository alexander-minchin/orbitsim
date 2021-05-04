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
        mass of spacecraft without fuel loaded (kg)
    engine : Engine
        the engine that is used by the spacecraft
    drag_coeff : float
        the coefficient of drag for the spacecraft
    area : float (m^2)
        the cross sectional area of the spacecraft
    state0 : array (m/s)
        state vector containing the initial 3D position and velocities
        [x,y,z,u,v,w]
    """

    def __init__(
        self,
        mass,
        engine,
        drag_coeff,
        area,
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
        [x,y,z,u,v,w]    [(m),(m),(m),(m/s),(m/s),(m/s)]
    environment : Environment
    """
    # define the spacecraft attributes in SI units
    self.mass = mass
    self.engine = engine
    self.drag_coeff = drag_coeff
    self.area = area
    self.state0 = state0