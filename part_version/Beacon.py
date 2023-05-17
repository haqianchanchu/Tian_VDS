import sign
import parameters
import random
import time,os
import structure
n = parameters.USER_NUMBER
P = sign.init()
seed = 1234
rand_list = [0, 0]
u_list = []
corrupt = {}
SLOT = parameters.SLOT
Epislon = 0.5
global START_TIME
def init_U(epislon):
	start()
	global Epislon
	global u_list
	global corrupt
	Epislon = epislon
	random.seed(seed)
	i = 0
	while i < n:
		sk, pk = sign.keygen(P)
		u_list.append({'pk':pk,'sk':sk})
		i += 1
	sk, pk = sign.keygen(P)
	corrupt = {'pk':pk,'sk':sk}
	return u_list

def select(sl):
	while sl >= len(rand_list):
		max_rand = len(u_list)+len(u_list)/(0.5+Epislon)*(0.5-Epislon)-1
		rand_list.append(random.randint(0, int(max_rand)))
	print(rand_list)
	if rand_list[sl] >= len(u_list):
		return corrupt
	else:
		return u_list[rand_list[sl]]
def judge():
	tem_l = []
	for user in rand_list:
		if user >= len(u_list):
			tem_l.append(1)
		else:
			tem_l.append(0)
def start():
	global START_TIME
	START_TIME = time.time()
def slot_num():
	global START_TIME
	return int((time.time()-START_TIME)/ SLOT)
def random_Tx():
	i = random.randint(0,len(u_list)-1)
	j = random.randint(0,len(u_list)-1)
	u1 = u_list[i]
	u2 = u_list[j]
	tx1 =  structure.Tx(u1['pk'], u2['pk'], 10, "haha")
	# print(u1['sk'])
	tx1.sign(u1['sk'])
	return tx1
def random_dirt_Tx():
	i = random.randint(0,len(u_list)-1)
	j = random.randint(0,len(u_list)-1)
	u1 = u_list[i]
	u2 = u_list[j]
	tx1 =  structure.Tx(u1['pk'], u2['pk'], 10, "dirt"+str(random.randint(0,10000)))
	# print(u1['sk'])
	tx1.sign(u1['sk'])
	return tx1
def Valid(block):
	block = structure.Block.get(block)
	body = block.body
	for tx in body:
		tx1 =  structure.Tx,get(tx)
		if tx1.data == "dirt":
			return 0
	return 1

def main():
	init_U()
	start()
	print(slot_num())
	i = 0


if __name__ == '__main__':
	main()