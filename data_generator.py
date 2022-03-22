import numpy as np
from pythonping import ping

server = '127.0.0.1'
data_arr = []

#writes data array to shared memory file
def send_data():
	data_mem.buf[:(1000*8)] = bytearray(np.asarray(data_arr))

def init(quit, data, ready):
	global quit_mem, data_mem, ready_mem
	global data_arr
	quit_mem = quit
	data_mem = data
	ready_mem = ready
	print("GENER: Generating data...")

	#generate initial data
	for i in range(1000):
		response_list = ping(server, count=1)
		#print("Ping: " + str(response_list.rtt_min_ms))
		data_arr.append(response_list.rtt_min_ms)
	send_data()
	print("GENER: Full array of data generated; generating more...")
	ready_mem.buf[0] = True

	update(0)

def update(pos):
	#generate next 250 datum
	global data_arr
	my_pos = pos
	for i in range(250):
		response_list = ping(server, count=1)
		data_arr[my_pos%1000] = response_list.rtt_min_ms
		send_data()
		my_pos +=1

	#check for quit
	if quit_mem.buf[0]:
		return

	update(my_pos+1)
