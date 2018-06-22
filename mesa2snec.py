import numpy as np
import glob
import io
import os
import mesaPlot as mp

p=mp.plot()

mesa_in='mesa.prof'

snec_profile='model.short'
snec_iso='model.iso.dat'
parameter_file='parameters'
gridding='GridPattern.dat'

msun = 1.9892*10**33
rsun = 6.9598*10**10

m=mp.MESA()
m.loadProfile(f=mesa_in)

num_zones = int(m.prof.num_zones)

zero=np.zeros((num_zones))


#Flip arrays

zones = num_zones - m.prof.zone + 1
zones =zones.astype(int)

v = m.prof.velocity

v[1:] = (m.prof.dq[0:-1]*v[1:] + m.prof.dq[1:]*v[0:-1])/(m.prof.dq[0:-1] + m.prof.dq[1:])



d = [zones[::-1],m.prof.mass[::-1]*msun,10**m.prof.logT[::-1],10**m.prof.logRho[::-1],
							v[::-1],m.prof.ye[::-1],zero]




#Todo need cell faced velcoity not cell centered
np.savetxt(snec_profile,np.column_stack(d),header=str(num_zones),comments='',
			 fmt='%d %26.16e %26.16e %26.16e %26.16e %26.16e %26.16e')


names = p._listAbun(m.prof)

abuns = [p._getIso(i)  for i in names ]
mass = [str(pp+nn) for _,pp,nn in abuns]
charge = [str(pp) for _,pp,nn in abuns]

header=str(num_zones)+' '+str(len(names))+'\n'
header=header + " ".join(mass)+'\n'
header=header + " ".join(charge)


d = [m.prof.mass[::-1],(10**m.prof.logR[::-1])*rsun] + [m.prof.data[mm][::-1] for mm in names]

np.savetxt(snec_iso,np.column_stack(d),header=header,comments='')

with open(parameter_file,'r') as f:
	l=f.readlines()
	
for idx,i in enumerate(l):
	if 'imax' in i:
		l[idx]='imax = '+str(num_zones)+'\n'
	elif 'comp_profile_name' in i:
		l[idx]='comp_profile_name = "'+str(snec_iso)+'"\n'
	elif 'profile_name' in i and 'comp' not in i:
		l[idx]='profile_name = "'+str(snec_profile)+'"\n'	

with open(parameter_file,'w') as f:
	f.writelines("%s" % s for s in l)
	
mm = m.prof.q[::-1]
	
np.savetxt(gridding,mm)
	

		


