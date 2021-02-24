"""
Murmur simulation project

Derived from Boids theorem

Joe Milarvie
"""
from Starling import Starling
import random as rd
import pygame
import math
import logging
import os

#Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s')
location = os.path.dirname(os.path.abspath(__file__))
Log_location = f'{location}/Logs/'
if not os.path.isdir(Log_location):
	os.makedirs('Logs')

file_handler = logging.FileHandler('Logs/ Murmur_log.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

#Set up parameters for the pygame
Width = 1200
Height = 800
Display_Colour = (135, 206, 235) #sky blue = 135, 206, 235
Starling_Colour = (0,0,0)

#Tells the program how many starlings to spawn (max approx = 100 depending on single thread performance of cpu) and initializes empty lists for later population
Starling_number = int(50) #<-- Number of Starlings
x = []
y = []
v = [] 
mass = []
theta = []
range_gen = range(Starling_number)

#quick check to stop too few starlings from breaking the simulation
if Starling_number <= 1:
	print("Error: Too few Starlings")
	quit()

#sets up the initial values for the starlings
counter = bool(1) #Choose True(1) or False(0) for centered or distributed respectively
for _ in range_gen:
	if counter:
		x.append(rd.randint(int(Width/3), int(Width/2))) 	#initial x position
		y.append(rd.randint(int(Height/3), int(Height/2)))  #initial y position
	else:
		x.append(rd.randint(0, Width))
		y.append(rd.randint(0, Height))
	v.append(rd.randint(8, 15))							#initial velocity
	theta.append(rd.randint(0,361))						#initial angle
	mass.append(0)										#initial mass
del counter

#Use this function to draw a starling
def Starling_draw(x, y, t):
	counter = bool(0) #For circles set counter to True(1), set to False(0) for arrows
	S_size = 6		  #<-- Starling size
	S_len = 2.5		  #<-- Multiplier for arrow size
	if counter:
		pygame.draw.circle(gameDisplay, Starling_Colour, [int(x), int(y)], S_size)
	else:
		vert_1 = [round(x + S_size*math.cos(t)), round(y - S_size*math.sin(t))]
		vert_2 = [round(x + (S_size*S_len)*math.sin(t)), round(y + (S_size*S_len)*math.cos(t))]
		vert_3 = [round(x - S_size*math.cos(t)), round(y + S_size*math.sin(t))]
		pygame.draw.polygon(gameDisplay, Starling_Colour, [vert_1, vert_2, vert_3])

#This function is used to initialize and differentiate each starling
def Do_Stuff():
	div = Starling_number-1
	for i in range_gen:
		x_temp = 0
		y_temp = 0
		t_temp = 0
		m_temp = 0
		v_temp = 0
		for j in range_gen:
			if j != i:
				Starlings = Starling(x[i], y[i], v[i], theta[i], Width, Height, x[j], y[j], mass[i], mass[j], theta[j], v[j]).position()
				x_temp += Starlings[0][0]
				y_temp += Starlings[0][1]
				t_temp += Starlings[1]
				m_temp += Starlings[2]
				v_temp += Starlings[3]
		x[i] = x_temp/div
		y[i] = y_temp/div
		theta[i] = t_temp/div
		mass[i] = int(m_temp/div)
		v[i] = v_temp/div
		Starling_draw(x[i], y[i], theta[i])

#This function executes the program and sets up the pygame display 
def main():
	while True:
		gameDisplay.fill(Display_Colour)
		#Basic syntax to allow the pygame environment to close:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		Do_Stuff()
		pygame.display.update()
		clock.tick(60)

if __name__ == '__main__':
	#Pygame setup code:
	pygame.init()
	gameDisplay = pygame.display.set_mode((Width, Height))
	pygame.display.set_caption('Murmur')
	clock = pygame.time.Clock()

	try:
		main()
	except Exception as e:
		logger.warning(str(e))
		print("There was an error, check error log")
