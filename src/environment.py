# -*- coding: utf-8 -*-

"""Environment Class"""

__author__ = "Alexander William Minchin"

import json

class Environment:
    """
    A class to repersent the environment setup

    ...

    Attributes
    ---------

    """

    def __init__(
            self,
            celestial_body,
            purturbations
    ):

    """
        Parameters
        ----------
        celestial_body : String
        	name of celestrial body that has been defined in
        	celestial_bodies.json
        purturbations : list
        	list of purturbations to be included in the simulation
    """

    self.celestial_body = celestial_body
    self.purturbations = purturbations

