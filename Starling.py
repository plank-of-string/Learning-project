"""
Starling for use in Murmur sim
"""
import math

class Starling:
	#Initialises the class:
	def __init__(self, x_pos, y_pos, speed, direction, x_bound, y_bound, Other_x, Other_y, mass, other_mass, other_direction, other_velocity):
		self.speed = speed
		self.direc = direction
		self.x_bound = x_bound
		self.y_bound = y_bound
		self.x = x_pos
		self.y = y_pos
		self.O_x = Other_x
		self.O_y = Other_y
		self.mass = mass
		self.O_mass = other_mass
		self.O_direc = other_direction
		self.O_V = other_velocity

	#Preforms the movment of the starling
	def movement(self):
		self.direc = int(round(self.direc))
		move_weight = [math.sin(self.direc), math.cos(self.direc)]
		self.x += (self.speed*move_weight[0])
		self.y += (self.speed*move_weight[1])
		self.check_bounds()
		return self.x, self.y

	#Stops the starlings from exceeding the bounds
	def check_bounds(self):
	    if self.x <= 0:
	    	self.x = 10
	    	self.direc += 0.5
	    elif self.x >= self.x_bound:
	        self.x = self.x_bound-10
	        self.direc += 0.5
	    if self.y <= 0:
	        self.y = 10
	        self.direc += 0.5
	    elif self.y >= self.y_bound:
	        self.y = self.y_bound-10
	        self.direc += 0.5

	#Calculates the distance to the currently passed other starling
	def Dist(self):
		Hyp_dist = math.sqrt((self.x - self.O_x)**2 + (self.y - self.O_y)**2)+0.00001 #'0.00001' is here to prevent divison by zero in the event of starling overlap
		Opp_dist = math.sqrt((self.O_x - self.x)**2)
		Direc_to_other = (180 - (math.asin(Opp_dist/Hyp_dist)))
		return Hyp_dist, Direc_to_other

	#Calculates if the currently passed other starling is in sight
	def in_sight(self):
		radius = 2000 # <--- Sight radius
		fov = 360    # <--- Feild of view
		fovL = self.direc - fov/2
		fovR = self.direc + fov/2
		if fovL < 0:
			fovL += 360
		if fovR > 360:
			fovR -= 360
		In_fov = self.Dist()[1]
		if self.Dist()[0] < radius:
			if self.direc >= In_fov >= fovL or self.direc <= In_fov <= fovR:
				return True

	#Acts to condense the murmur
	def cohesion(self):
		New_direct_1 = self.Dist()[1]
		#New_direct_1 -= New_direct_1/1.15 #Adds movement weight
		return New_direct_1

	#Changes the direction of the starling to align with the direction of the other starling that is in sight
	def alignment(self):
		New_direct_2 = self.O_direc 	
		#New_direct_2 -= New_direct_2/1.15
		return New_direct_2

	#Makes the starlings move away from each other if they get too close
	def avoidance(self):
		if self.direc < self.Dist()[1]:
			New_direct_3 = self.direc-self.Dist()[1]
		else:
			New_direct_3 = self.direc+self.Dist()[1]
		#New_direct_3 -= New_direct_3/1
		return New_direct_3

	#Preforms multiple logic arguments depending on if the other starling is in sight, etc...
	def attractor(self):
		Min_dist = 10 		#<-- Minimum distance between starlings
		Align_dist = 500	#<-- Maximum alignment distance between starlings
		if self.in_sight():
			if self.speed < self.O_V:
				if self.speed < 10:
					self.speed += 1 	#Makes the starlings match their speed with their nearest starling
			elif self.speed > self.O_V:
				if self.speed > 10:
					self.speed -= 1
			if self.O_mass > self.mass:
				if Align_dist > self.Dist()[0] > Min_dist:
					New_direct = (self.cohesion() + self.alignment())/2
					return New_direct, self.mass, self.speed
				elif self.Dist()[0] > Min_dist:
					return self.cohesion(), self.mass, self.speed
				else:	
					return self.avoidance(), self.mass, self.speed
			elif self.Dist()[0] <= Min_dist:
				self.mass += 10			#Mass still increases to generate a murmur
				return self.avoidance(), self.mass, self.speed
			else:
				self.mass += 10
				return self.direc, self.mass, self.speed
		else: 	
			self.mass -= 20
			return self.direc, self.mass, self.speed #Retruns inital values if no other starlings are about

	#Outputs the new postion of the starling
	def position(self):
		pos = [self.movement()[0], self.movement()[1]]
		New_direc = self.attractor()[0]
		New_mass = self.attractor()[1]
		New_speed = self.attractor()[2]
		return pos, New_direc, New_mass, New_speed