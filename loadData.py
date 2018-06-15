

import numpy as np
import glob
import io

MSUN=1.9892*10**33 #grams
RSUN=6.9598*10**10 #cm
LSUN=3.8418*10**33 #ergs


def get_num_zones():
	with open('parameters','r') as f:
		for i in f:
			if 'imax' in i:
				return int(i.split('=')[1])
				

def read_init(filename):
	return np.genfromtxt(filename,names=['zone','data'])
		
		
def read_all_inits():
	res={}
	for i in glob.glob("*_init_*.dat"):
		name=i.split('_')[0]
		res[name]=read_init(i)
	
	for i in glob.glob("*_initial.dat"):
		name=i.split('_')[0]
		res[name]=read_init(i)
		
	n=[]
	for i in res:
		n.append((i,np.float64))
	
	n = [('zone','i4')] + n
	
	arr = np.empty(len(res[i]['zone']),dtype=np.dtype(n))
	
	arr['zone'] = res[i]['zone']
	
	for i in res:
		arr[i] = res[i]['data']
	
	
	return arr
	
x=read_all_inits()


def read_output(filename,num_zones):
	time=[]
	data=[]
	cols=np.dtype([('mass',np.float64),('data',np.float64)])
	with open(filename,'r') as f:
		while True:
			l=f.readline()
			if len(l):
				time.append(float(l.split('=')[1]))
				z=[]
				for i in range(num_zones):
					z.append(bytes(f.readline().encode()))
				s=io.BytesIO(b"".join(z))
				data.append(np.genfromtxt(s,dtype=cols))
				# Blank at end of section
				l=f.readline()
				l=f.readline()
			else:
				break

	return time,data
	
def read_all_outputs():
	num_zones=get_num_zones()
	
	res={}
	for i in glob.glob("*.xg"):
		name=i.replace('.xg','')
		res[name]=read_output(i,num_zones)
				
	return res
		

z=read_all_outputs()



