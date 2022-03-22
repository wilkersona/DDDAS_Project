'''
March 22, 2022
Andrew Wilkerson & Paul Saswata

Distributed program to read in ping times, determine the probability
that certain given theorems hold, and choose the 'best' option
'''

import logging
import threading
import time
from multiprocessing import shared_memory
from multiprocessing.managers import SharedMemoryManager
import proof
import sentinel
import data_generator
import model

num_theorems = 4

with SharedMemoryManager() as smm:
	#shared memory for the following:
	#quit message for processes to terminate
	quit = smm.SharedMemory(1)
	quit.buf[0] = False
	#message saying whether a theorem is possible at all
	able = smm.SharedMemory(1)
	able.buf[0] = False
	#data stream
	data = smm.SharedMemory(8000)
	#message containing current mu and sigma
	musig = smm.SharedMemory(16)
	#contains the probability that each theorem holds
	probs = smm.SharedMemory(8*num_theorems)
	#whether the data stream is full yet
	ready = smm.SharedMemory(1)
	ready.buf[0] = False

	print("Type \"quit\" to exit")

	#start each thread with the relevant shared memory
	proof = threading.Thread(target=proof.init, args=(quit,musig,probs,able))
	proof.start()

	gener = threading.Thread(target=data_generator.init, args=(quit,data,ready))
	gener.start()

	senti = threading.Thread(target=sentinel.init, args=(quit,data,musig,able,ready))
	senti.start()

	model = threading.Thread(target=model.init, args=(quit,probs,able))
	model.start()

	#break out of the loop
	while 1:
		if input() == "quit":
			quit.buf[0] = True
			break

	#rejoin all threads and deallocate all memory
	proof.join()
	gener.join()
	senti.join()
	model.join()

	quit.close()
	quit.unlink()
	able.close()
	able.unlink()
	data.close()
	data.unlink()
	musig.close()
	musig.unlink()
	probs.close()
	probs.unlink()
	ready.close()
	ready.unlink()