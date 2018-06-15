#!/usr/bin/python3

#Make a new run directory for SNEC

import sys
import os
import shutil

SNEC_DIR=os.environ["SNEC_DIR"]
folders=sys.argv[1:]


for i in folders:
	os.mkdir(i)
	os.mkdir(os.path.join(SNEC_DIR,'Data'))
	shutil.copyfile(os.path.join(SNEC_DIR,'parameters'),os.path.join(i,parameters))
	shutil.copyfile(os.path.join(SNEC_DIR,'snec'),os.path.join(i,snec))
	os.symlink(os.path.join(SNEC_DIR,'tables'),os.path.join(i,'tables'))
	print("Made folder "+i)


