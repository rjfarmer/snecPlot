import numpy as np
import glob
import io
import os
import mesaPlot as mp # https://github.com/rjfarmer/mesaplot
import sys

p=mp.plot()

#Path to mesa profile to load
mesa_in=sys.argv[1]

try:
    u_flag = sys.argv[2] == 1
except IndexError:
    u_flag=False

# Output filenames
snec_profile='model.short'
snec_iso='model.iso.dat'
#parameter_file='parameters'
gridding='GridPattern.dat'

msun = 1.9892*10**33
rsun = 6.9598*10**10

m=mp.MESA()
m.loadProfile(f=mesa_in)

num_zones = int(m.prof.num_zones)

zero=np.zeros((num_zones))


#Flip arrays mesa has central zone at end of array not start

zones = num_zones - m.prof.zone + 1
zones = zones.astype(int)

v = m.prof.velocity

try:
    dq = m.prof.dq
except AttributeError:
    dq = 10**m.prof.logdq

# Make velocity cell faced (only if we had u_flag)

if u_flag:
    v[1:] = (dq[0:-1]*v[1:] + dq[1:]*v[0:-1])/(dq[0:-1] + dq[1:])

try:
    radius = (10**m.prof.logR[::-1])*rsun
except AttributeError:
    radius = m.prof.radius[::-1]*rsun

# Setup output list
d = [zones[::-1],m.prof.mass[::-1]*msun,radius,10**m.prof.logT[::-1],10**m.prof.logRho[::-1],
							v[::-1],m.prof.ye[::-1],zero]


np.savetxt(snec_profile,np.column_stack(d),header=str(num_zones),comments='',
			 fmt='%d %26.16e %26.16e %26.16e %26.16e %26.16e %26.16e %26.16e')

# get names, masses and charges of isotopes in model
names = p._listAbun(m.prof)

if 'prot' in names:
	names.remove('prot')

abuns = [p._getIso(i)  for i in names ]
mass = [str(pp+nn) for _,pp,nn in abuns]
charge = [str(pp) for _,pp,nn in abuns]

header=str(num_zones)+' '+str(len(names))+'\n'
header=header + "d0 ".join(mass)+'\n'
header=header + "d0 ".join(charge)


d = [m.prof.mass[::-1]*msun,radius] + [np.maximum(10**-99,m.prof.data[mm][::-1]) for mm in names]

# Save isotope data
np.savetxt(snec_iso,np.column_stack(d),header=header,comments='')

# with open(parameter_file,'r') as f:
	# l=f.readlines()
	
# for idx,i in enumerate(l):
	# # if 'imax' in i:
		# # l[idx]='imax = '+str(num_zones)+'\n'
	# if 'comp_profile_name' in i:
		# l[idx]='comp_profile_name = "'+str(snec_iso)+'"\n'
	# elif 'profile_name' in i and 'comp' not in i:
		# l[idx]='profile_name = "'+str(snec_profile)+'"\n'	

# edit the parameters file with the filenames
# with open(parameter_file,'w') as f:
	# f.writelines("%s" % s for s in l)
	
mm = m.prof.q[::-1]

mm[0] = 0.0
	
np.savetxt(gridding,mm)

print("Number of zones:",len(mm))	

		


