#!/usr/bin/env python

import numpy as np
import kepler as kp
import datetime
from mayavi import mlab
import random

from .Environment import Environment

def plot_n_orbits(orbits,environment,show_plot=True,save_plot=False,title='No Title'
				 ,show_body=True):
	'''
	creates a 3D plot from the input rs list, containing x, y, and z positions
	'''
	mlab.figure(1, bgcolor=(0, 0, 0), fgcolor=(0.8, 0.8, 0.8),size=(800, 400))
	mlab.clf()

	r_plot = environment.cb_radius

	rs = []
	for orbit in orbits:
		rs.append(orbit.rs)

	if show_body:
	# Plot central body
		plot_body(environment)


	# plot the x,y,z vectors
	l = r_plot*2.0
	x, y, z = [[0,0,0],[0,0,0],[0,0,0]]
	u, v, w = [[l,0,0],[0,l,0],[0,0,l]]
	mlab.quiver3d(x,y,z,u,v,w,color=(1,0,0))

	# Check for custom axes limits
	max_val = np.max(np.abs(rs))

	# Plot trajectory and starting point
	for r in rs:
		# print(r)
		mlab.plot3d(r[:,0],r[:,1],r[:,2],color = (random.uniform(0.2, 1),
					random.uniform(0.2, 1),random.uniform(0.2, 1)),
										tube_radius=None)
	
	# Check for custom axes limits
	max_x = np.max([r[:,0] for r in rs])
	min_x = np.min([r[:,0] for r in rs])
	max_y = np.max([r[:,1] for r in rs])
	min_y = np.min([r[:,1] for r in rs])
	max_z = np.max([r[:,2] for r in rs])
	min_z = np.min([r[:,2] for r in rs])

	if np.abs(min_z) < r_plot:
		min_z = -r_plot
	if max_z < r_plot:
		max_z = r_plot

	extent=[min_x,max_x,min_y,max_y,min_z,max_z]
	axes = mlab.axes(extent=[min_x,max_x,min_y,max_y,min_z,max_z]
	 				,xlabel = 'X (km)', ylabel = 'Y (km)', zlabel='Z (km)'
	 				,nb_labels=5)

	axes.label_text_property.font_family = 'courier'
	axes.label_text_property.font_size = 6
	axes.title_text_property.font_family = 'courier'
	axes.title_text_property.font_size = 8

	if show_plot:
		mlab.show()
	if save_plot:
		mlab.savefig(title+'.png',dpi=300)

def osv_to_koe(osv, mu):
	'''
	input an orbital state vector
	returns a corresponding vector of keplerian orbital elements
	'''
	r_vec = osv[:3]
	v_vec = osv[3:]
	h_bar = np.cross(r_vec, v_vec)
	h = np.linalg.norm(h_bar)
	r = np.linalg.norm(r_vec)
	v = np.linalg.norm(v_vec)
	E=0.5 * v**2 - mu/r
	a = -mu/(2*E)
	e = np.sqrt(1 - h**2 / (a*mu))
	i = np.arccos(h_bar[2]/h)
	if i == 0:
		lan = 0
		lat = 0
	else:
		lan = np.arctan2(h_bar[0], -h_bar[1])
		lat = np.arctan2(np.divide(r_vec[2],(np.sin(i))),(r_vec[0]*np.cos(lan) + r_vec[1]*np.sin(lan)))

	p = a*(1 - e**2)
	ta = np.arctan2(np.sqrt(p/mu) * np.dot(r_vec,v_vec), p-r)
	ap = lat - ta
	koe = a, e, i, lan, ap, ta
	return koe

def koe_to_osv(koe, mu, deg=True):
	'''
	input a vector of keplerian orbital elements
	returns the corresponding orbital state vector
	'''
	a, e, i, lan, ap, ta = koe

	if deg:
		np.radians(i)
		np.radians(lan)
		np.radians(ap)
		np.radians(ta)
	EA = 2*np.arctan(np.tan(ta/2) / np.sqrt(np.divide((1+e),(1-e))))
	r = a*(1 - e*np.cos(EA))
	h = np.sqrt(mu*a * (1 - e**2))


	x = r*(np.cos(lan)*np.cos(ap+ta) - np.sin(lan)*np.sin(ap+ta)*np.cos(i))
	y = r*(np.sin(lan)*np.cos(ap+ta) + np.cos(lan)*np.sin(ap+ta)*np.cos(i))
	z = r*(np.sin(i)*np.sin(ap+ta))

	p = a*(1-e**2)

	u = (x*h*e/(r*p))*np.sin(ta) - (h/r)*(np.cos(lan)*np.sin(ap+ta) + \
	np.sin(lan)*np.cos(ap+ta)*np.cos(i))
	v = (y*h*e/(r*p))*np.sin(ta) - (h/r)*(np.sin(lan)*np.sin(ap+ta) - \
	np.cos(lan)*np.cos(ap+ta)*np.cos(i))
	w = (z*h*e/(r*p))*np.sin(ta) + (h/r)*(np.cos(ap+ta)*np.sin(i))


	osv = x, y, z, u, v, w
	return osv

def tle_to_koe(tle_filename,mu):
	'''
	input a file containing a single set wo-line elements
	returns a the keplerian orbital elements
	'''

	# read in TLE file
	with open(tle_filename, 'r') as f:
		lines = f.readlines()

	# separate into three lines
	line0 = lines[0].strip() # satellite name
	line1 = lines[1].strip().split()
	line2 = lines[2].strip().split()

	# epoch (year and day)
	epoch = line1[3]
	year, month, day, hour = calc_epoch(epoch)

	# process koe

	i = float(line2[2])
	lan = float(line2[3])
	e_string = line2[4]
	e = float('0.' + e_string)
	ap = float(line2[5])
	Me = float(line2[6]) 
	mean_motion = float(line2[7])
	T = 1/mean_motion * 24*3600
	a = (T**2*mu/4.0/np.pi**2)**(1/3.0)

	E = kp.solve(Me,e)
	ta = 2*np.arctan(np.sqrt(np.divide(1+e, 1-e) * np.tan(E/2)))

	return a, e, i, lan, ap, ta, [year, month, day, hour]

def tle_to_osv(tle_filname):
	'''
	input a file containing a single set of two-line elements
	returns an orbital state vector
	'''
	return koe_to_osv(tle2koe(tle_filename), deg=True)

def calc_epoch(epoch):
	year = int('20' + epoch[:2])
	epoch = epoch[2:].split('.')
	day_of_year = int(epoch[0])-1
	hour = float('0.' + epoch[1]) * 24.0
	date = datetime.date(year,1,1) + datetime.timedelta(day_of_year)

	month = float(date.month)
	day = float(date.day)
	
	return year, month, day, hour

def tles_to_koes(tle_filename,mu):
	'''
	input a file containing sets of two-line elements
	returns a list of sets of keplerian orbital elements
	'''
	tles_lst = get_tles(tle_filename)

	koes = []
	for tle_str in tles_lst:
		lines = tle_str

		# separate into three lines
		line0 = lines[0].strip() # satellite name
		line1 = lines[1].strip().split()
		line2 = lines[2].strip().split()

		# epoch (year and day)
		epoch = line1[3]
		year, month, day, hour = calc_epoch(epoch)

		# Process koe

		i = float(line2[2])
		lan = float(line2[3])
		e_string = line2[4]
		e = float('0.' + e_string)
		ap = float(line2[5])
		Me = float(line2[6]) 
		mean_motion = float(line2[7])
		T = 1/mean_motion * 24*3600
		a = (T**2*mu/4.0/np.pi**2)**(1/3.0)

		E = np.degrees(kp.solve(np.radians(Me),e))
		ta = 2*np.degrees(np.arctan(np.sqrt(np.divide(1+e, 1-e)) * np.tan(E/2)))

		koes.append([a, e, i, lan, ap, ta])
	return koes		
		
def get_tles(tle_filename):
	# read in TLE file
	with open(tle_filename, 'r') as f:
		lines = f.readlines()
	tles_lst = chunks(lines,3)
	return tles_lst

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def plot_body(environment):
	# Display continents outline, using the VTK Builtin surface 'Earth'
	from mayavi.sources.builtin_surface import BuiltinSurface
	continents_src = BuiltinSurface(source='earth', name='Continents')
	# The on_ratio of the Earth source controls the level of detail of the
	# continents outline.
	continents_src.data_source.on_ratio = 2
	continents_src.data_source.radius = environment.cb_radius
	continents = mlab.pipeline.surface(continents_src, color=(0, 0, 0))

	# Display a sphere, for the surface of the Earth

	sphere = mlab.points3d(0, 0, 0, environment.cb_radius, 
									scale_mode='scalar',
	                                scale_factor=2,
	                                color=(0.67, 0.77, 0.93),
	                                resolution=50,
	                                opacity=1,
	                                name='Earth')

	sphere.actor.property.specular = 0.45
	sphere.actor.property.specular_power = 5

	# Plot the equator and the tropiques
	theta = np.linspace(0, 2 * np.pi, 100)
	for angle in (- np.pi / 6, 0, np.pi / 6):
	    x = environment.cb_radius*np.cos(theta) * np.cos(angle)
	    y = environment.cb_radius*np.sin(theta) * np.cos(angle)
	    z = environment.cb_radius*np.ones_like(theta) * np.sin(angle)

	    mlab.plot3d(x, y, z, color=(0,0,0),
	                        opacity=1, tube_radius=None)
