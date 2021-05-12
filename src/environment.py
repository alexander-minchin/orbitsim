# -*- coding: utf-8 -*-

"""Environment Class"""

__author__ = "Alexander William Minchin"

import json
from scipy import constants as const

CONFIG_FILE = '../simulator_values/celestial_bodies.json'

class Environment:
    """
    A class to repersent the environment setup

    ...

    Attributes
    ---------
	celestial_body : String
    	name of celestrial body that has been defined in
    	celestial_bodies.json
    perturbations : list
    	list of perturbations to be included in the simulation
    	['thrust', 'aero', 'J2']
    """

    def __init__(
            self,
            celestial_body,
            perturbations=[]
    ):

	    """
	        Parameters
	        ----------
	        celestial_body : String
	        	name of celestrial body that has been defined in
	        	celestial_bodies.json
	        perturbations : list
	        	list of perturbations to be included in the simulation
	        	['thrust', 'aero', 'J2']
	    """

	    self.celestial_body = celestial_body
	    self.perturbations = perturbations

	    self.get_celestial_body()

    def get_celestial_body(self):
    	"""read in data about celestial body and unpack"""

    	#read in json file
    	with open(CONFIG_FILE) as f:
    		data = json.load(f)

    	celestial_body_dict = data[self.celestial_body]

    	# unpack json file
    	self.cb_mass = celestial_body_dict['mass_kg']
    	self.cb_radius = celestial_body_dict['radius_m']
    	self.cb_J2 = celestial_body_dict['J2']
    	self.cb_atm_rot = celestial_body_dict['atm_rot_vec_rad_p_s']

    	# calculate parameters
    	self.cb_mu = const.G * self.cb_mass # m^3 kg^-1 s^-2
