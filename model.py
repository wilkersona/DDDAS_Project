import time
import array

choose_chance = 0.8
cur_model = 0
cur_prob = 0

#prevents spamming the "unable" message
written_unable = False

#file containing all the current theorems you want to check
theorems_file = "theorems.txt"

def write_model(which, probability):
	file = open(theorems_file, "r")
	theorems = file.readlines()
	result = ""

	#print out the correct formatting for whichever theorem is chosen
	#add new types of theorems here as well
	if theorems[which][:1] == "<":
		result = ("Model: P(Transmission delay <= " + str(float(theorems[which][2:])) + ") = " + str(probability))

	file.close()
	return result

def init(quit, probs, able):
	global quit_mem, probs_mem, able_mem
	quit_mem = quit
	probs_mem = probs
	able_mem = able

	#as with proof.py, I am not sure we need to write the initial garbage proof
	global file 
	file = open('model_out.txt','w+')
	file.write("MODEL: Initial " + write_model(0, 0) + "\n")
	update()

def update():
	global cur_model, cur_prob, written_unable
	global file 
	time.sleep(1)

	#read the current probabilities
	probabilities = array.array('d', bytes(probs_mem.buf))
	model_picked = False
	for i in range(len(probabilities)):
		probabilities[i] = float(probabilities[i])
		#pick the first model with probability above choose_chance
		#assumes teorems are sorted s.t. probabilities do not decrease
		if probabilities[i] > choose_chance and not model_picked:
			model_picked = True
			#print statements; I included the live output here so as to not write redundant code
			if cur_model != i:
				print("LIVE: New " + write_model(i, probabilities[i]))
				file.write("MODEL: New " + write_model(i, probabilities[i]) + "\n")
			elif cur_prob != probabilities[i]: 
				print("LIVE: Updated " + write_model(i, probabilities[i]))
				file.write("MODEL: Updated " + write_model(i, probabilities[i]) + "\n")
			cur_model = i
			cur_prob = probabilities[i]
			written_unable = False

	#if no theorems possible, say so
	if (not able_mem.buf[0] or not model_picked):
		if (not written_unable):
			file.write("MODEL: No Proofs Available!\n")
			written_unable = True

	#flush file and check for quit
	file.flush()
	if quit_mem.buf[0]:
		#quit_mem.close()
		file.close()
		return
	update()
