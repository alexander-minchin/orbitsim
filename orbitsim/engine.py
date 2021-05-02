# -*- coding: utf-8 -*-

__author__ = "Alexander William Minchin"

from scipy import constants as const


class Engine:

	"""Defines information surrounding the spaceship in orbit."""

	def __init__(
		self,
		mass,
		mass_p,
		Isp,
		thrust
	):

		"""
		Inputs:
			mass : float
				mass of engine (kg)
			mass_p : float
				mass of propellant (kg)
			Isp : float
				the specific impulse of the engine (N*s/kg)
			thrust : float
				thrust produced by the enginer (N)

		Outputs:
			None
		"""
		# define the spacecraft attributes in SI units
		self.mass = mass
		self.mass_p = mass_p
		self.Isp = Isp
		self.thrust = thrust

		# attributes to be calculated
		self.mass_dot = None
		self.burnout_time = None

	def calculate_mass_dot(self):
		""" calculates and returns the time derivative of proellant mass (kg/s)"""
		#calculate m dot
		self.mass_dot = self.thrust / (const.g * self.Isp)

		return self.mass_dot

	def calculate_burnout_time(self):
		""" calculates the time till all propellant is burnt (s)"""
		#calculate mass dot if not already done
		if self.mass_dot is None:
			self.calculate_mass_dot()

		#calculate burnout time
		self.burnout_time = self.mass_p / self.mass_dot

		return self.burnout_time

	def info(self):
		""" prints information summary of the engine"""

		#print engine information
		print("\nEngine Information")
		print("Engine Mass:", self.mass, "kg")
		print("Engine Isp:", self.Isp, "N*s/kg")
		print("Engine Thrust:", self.thrust, "N")
		print("Propellant Mass:", self.mass_p, "kg")
		print("Engine Burnout Time", self.burnout_time, "s")

