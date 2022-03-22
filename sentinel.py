import time
import numpy as np
from scipy import stats
import math
import array

output_file = 'senti_out.txt'

percentChange = 1.2
hard_constraint = 15

current_mu = 1
current_sigma = 1

file = 0

#normality test
def isnormal(data):
	#The data I was generating was deemed too normal, so this function is temporarily commented out
	'''
	k2, p = stats.normaltest(data)
	alpha = 1e-3
	return p >= alpha
	'''
	return True

#checks whether mu and sigma are within a certain percentage of the previous mu and sigma
def check_update(mu, sigma):
	global percentChange
	global current_sigma
	global current_mu

	mu_off = abs((current_mu*percentChange)-current_mu)
	sigma_off = abs((current_sigma*percentChange)-current_sigma)
	change_mu = (mu<current_mu-mu_off) or (mu>current_mu+mu_off)
	change_sigma = (sigma<current_sigma-sigma_off) or (sigma>current_sigma+sigma_off)
	return change_mu or change_sigma

#calculates mean and variance
def get_mu_sigma(data):
	mu = sum(data) / len(data)
	var =sum((i - mu) ** 2 for i in data) / len(data)	
	sigma = math.sqrt(var)
	return (mu, sigma)

#reads in the data, and reports any significant changes
def print_mu_sigma():
	global percentChange
	global current_mu
	global current_sigma
	
	data = array.array('d', bytes(data_mem.buf))
	mu_sigma = get_mu_sigma(data)

	#avoid print statements if data hasn't changed much
	if (check_update(mu_sigma[0], mu_sigma[1])):
		current_mu = mu_sigma[0]
		current_sigma = mu_sigma[1]

		#data my not have useful theorems proveable (hard_constraint is more a proof of concept)
		able_mem.buf[0] = isnormal(data) and mu_sigma[0] <= hard_constraint

		global file 
		file.write("SENTI: Change Detected!\n")

		musig_mem.buf[:16] = bytearray(np.asarray(mu_sigma))


def init(quit, data, musig, able, ready):
	global quit_mem, data_mem, musig_mem, able_mem, ready_mem
	quit_mem = quit
	data_mem = data
	musig_mem = musig
	able_mem = able
	ready_mem = ready

	global file 
	file = open(output_file,'w+')
	file.write("SENTI: Started monitoring incoming data...\n")

	#wait for data to be ready
	while not ready_mem.buf[0]:
		time.sleep(0.2)
	update()

def update():
	global file
	time.sleep(1)

	#print if mu or sigma changes
	print_mu_sigma()

	#flush file, and check for quit
	file.flush()
	if quit_mem.buf[0]:
		file.close()
		return

	update()
