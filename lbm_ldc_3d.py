#!/usr/bin/python

import numpy
import lbm
import geo

import optparse
from optparse import OptionGroup, OptionParser, OptionValueError

import sym

sym.use_grid(sym.D3Q13)

class LBMGeoLDC(geo.LBMGeo3D):
	"""Lid-driven cavity geometry."""

	max_v = 0.1

	def _define_nodes(self):
		"""Initialize the simulation for the lid-driven cavity geometry."""
		self.map = numpy.zeros((self.lat_d, self.lat_h, self.lat_w), numpy.int32)

		# bottom/top
		for x in range(0, self.lat_w):
			for y in range(0, self.lat_h):
				self.set_geo((x, y, self.lat_d-1), self.NODE_VELOCITY, (self.max_v, 0.0, 0.0))
				self.set_geo((x, y, 0), self.NODE_WALL)

		# walls
		for z in range(1, self.lat_d):
			for x in range(0, self.lat_w):
				self.set_geo((x, 0, z), self.NODE_WALL)
				self.set_geo((x, self.lat_h-1, z), self.NODE_WALL)
			for y in range(0, self.lat_h):
				self.set_geo((0, y, z), self.NODE_WALL)
				self.set_geo((self.lat_w-1, y, z), self.NODE_WALL)

	def init_dist(self, dist):
		self.velocity_to_dist((0, 0, 0), (0.0, 0.0, 0.0), dist)

		for i in range(0, len(sym.GRID.basis)):
			dist[i,:,:,:] = dist[i,0,0,0]

		for x in range(0, self.lat_w):
			for y in range(0, self.lat_h):
				self.velocity_to_dist((x, y, self.lat_d-1), (self.max_v, 0.0, 0.0), dist)

	# FIXME
	def get_reynolds(self, viscosity):
		return int((self.lat_w-1) * self.max_v/viscosity)

class LDCSim(lbm.LBMSim):

	filename = 'ldc'

	def __init__(self, geo_class):
		opts = []
		lbm.LBMSim.__init__(self, geo_class, misc_options=opts)

sim = LDCSim(LBMGeoLDC)
sim.run()