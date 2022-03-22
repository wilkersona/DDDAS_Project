import time
import statistics
from statistics import NormalDist
import numpy as np
import math
import array

current_mu = 1
current_sigma = 1

#file containing all the current theorems you want to check
theorems_file = "theorems.txt"

#so that it does not spam that you cannot prove anything useful
written_unable = False

#Here is where to list new types of theorems
#	at the moment, we only have [< N]

#create new less-than theorem
def create_theorem_lessthan(max_delay, MU, SIGMA):
	probability = NormalDist(mu=MU, sigma=SIGMA).cdf(max_delay)
	#just edit the probability to ensure it is never exactly 1
	probability = probability - 0.0000000000001
	thm_strng = "P(Transmission delay <= " + str(max_delay) + ") = " + str(probability) 
	return (probability, thm_strng)

#print theorems from file
def print_theorems(MU, SIGMA):
	file = open(theorems_file, "r")
	theorems = file.readlines()
	probabilities = []
	strings = []

	#loop through, parsing the theorems as you go
	#add new types of theorems here, along with a flag (e.g. "<")
	for theorem in theorems:
		if theorem[:1] == "<":
			data = create_theorem_lessthan(float(theorem[2:]), MU, SIGMA)
			probabilities.append(data[0])
			strings.append(data[1])

	#print the probability that each theorem holds
	file.close()
	probs_mem.buf[:(len(probabilities)*8)] = bytearray(np.asarray(probabilities))
	return strings

def init(quit, musig, probs, able):
	global quit_mem, musig_mem, probs_mem, able_mem
	quit_mem = quit
	musig_mem = musig
	probs_mem = probs
	able_mem = able

	#prints out initial proofs (mu and sigma are both 1); is the initial proof really necessary?
	global file 
	file = open('proof_out.txt','w+')
	file.write("PROOF: Initial Proofs:\n")
	file.write("PROOF: "+str(print_theorems(1, 1))+"\n")
	update()

def update():
	global current_mu
	global current_sigma
	global written_unable
	global file

	#read in the new mu and sigma
	cur_musig = [current_mu, current_sigma]
	new_musig = array.array('d', bytes(musig_mem.buf))
	new_musig = [float(new_musig[0]), float(new_musig[1])]

	#print out the corresponding message
	if (not able_mem.buf[0]):
		if (not written_unable):
			file.write("PROOF: No Proofs Possible!\n")
			written_unable = True
	#mu or sigma changed
	elif (cur_musig != new_musig):
		written_unable = False
		file.write("PROOF: New Mu and Sigma: " + str(new_musig) + "\n")
		file.write("PROOF: New Theorems: "+str(print_theorems(new_musig[0], new_musig[1])) + "\n")
		current_mu = new_musig[0]
		current_sigma = new_musig[1]

	#flush file, check for quit
	time.sleep(1)
	file.flush()
	if quit_mem.buf[0]:
		file.close()
		return
	update()
