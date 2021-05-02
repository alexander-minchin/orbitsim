# -*- coding: utf-8 -*-

__author__ = "Alexander William Minchin"




class Spaceship:

	"""Defines information surrounding the spaceship in orbit."""

	def __init__(
		self,
		mass,
		engine,
		Cd,
		area,
		state0
	):

	"""
	Inputs:
		mass : float
			mass of spacecraft without fuel loaded (kg)
		engine : Engine
			the engine that is used by the spacecraft
		Cd : float
			the coefficient of drag for the spacecraft
		area : float (m^2)
			the cross sectional area of the spacecraft
		state0 : array (m/s)
			state vector containing the initial 3D position and velocities
			[x,y,z,u,v,w]

	Outputs:
		None
	"""
	# define the spacecraft attributes in SI units
	self.mass = mass
	self.engine = engine
	self.Cd = Cd
	self.area = area
	self.state0 = state0

