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
	celestial_body : String
    	name of celestrial body that has been defined in
    	celestial_bodies.json
    purturbations : list
    	list of purturbations to be included in the simulation
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
        	['thrust', 'aero', 'J2']
    """

    self.celestial_body = celestial_body
    self.purturbations = purturbations

    self.get_celestial_body()

    def get_celestial_body(self):
    	"""read in data about celestial body and unpack"""

    	#read in json file
    	with open('../simulator_values/celestial_bodies.json') as f:
    		data = json.load(f)

    	celestial_body_dict = data[celestial_body]

    	#unpack json file
    	self.cb_mass = celestial_body_dict['mass_kg']
    	self.cb_radius = celestial_body_dict['radius_m']
    	self.cb_J2 = celestial_body_dict['J2']
    	self.cb_atm_rot = celestial_body_dict['atm_rot_vec_rad_p_s']
    	