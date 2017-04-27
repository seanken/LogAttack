import numpy as np;
import scipy as sp;
import math;
import random as rand;
from sklearn.linear_model import LogisticRegression as LR;
import pandas as pd;
import Attack as at;








def attack_subset(n0,n1,ORwith,ORwo,err=.001):
	n=n0+n1;
	poss=at.attack_no_covar(n0,n1,ORwo,err);
	ret=[];
	for gen in poss:
		y=[1 for i in range(0,n+1)]
		for i in range(0,n0):
			y[i]=0;
			lr=LR(C = 1e9);
			i0=gen[0];
			i1=gen[1];
			i2=gen[2];
			j0=gen[3];
			j1=gen[4];
			j2=gen[5];
			x=[0 for i in range(0,n+1)];
					
			x[:i0]=[2 for i in range(0,i0)];
			cur=i0;
			x[cur:cur+i1]=[1 for i in  range(0,i1)];
			cur=cur+i1;
			cur=cur+i2
			x[cur:cur+j0]=[2 for i in  range(0,j0)];
			cur=cur+j0;
			x[cur:cur+j1]=[1 for i in  range(0,j1)];
			for i in range(0,3):
				x[-1]=i;
				lr.fit(np.asarray([x]).T,y)
				OR_cur=math.exp(float(lr.coef_));
				if abs(OR_cur-ORwith)<err:
					ret.append(i);
					print "match!\n";
	print len(ret);
	print len(poss);
	print ret;


def test_sub(n0,n1,err=.001):
	lr=LR(C = 1e9);
	n=n0+n1;
	x=[rand.randint(0,2) for i in range(0,n)]
	y=[1 for i in range(0,n)]
	for i in range(0,n0):
		y[i]=0;
	lr.fit(np.asarray([x]).T,y)
	ORwo=math.exp(float(lr.coef_));
	x.append(rand.randint(0,2));
	y.append(1);
	lr=LR(C = 1e9);
	lr.fit(np.asarray([x]).T,y)
	ORwith=math.exp(float(lr.coef_));
	attack_subset(n0,n1,ORwith,ORwo,err=err);



if __name__=="__main__":
	n0=50;
	n1=50;
	err=.001;
	test_sub(n0,n1,err);





