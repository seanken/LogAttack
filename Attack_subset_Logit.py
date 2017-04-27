import numpy as np;
import scipy as sp;
import math;
import random as rand;
from sklearn.linear_model import LogisticRegression as LR;
import pandas as pd;
import Attack_Logit as at;
import sys;
from scipy.stats import mode;
from math import floor;
from math import log10;



def round_sig(val,num_dig=3):
	if num_dig==-1:
		return val;
	return round(val, -int(floor(log10(abs(val))))+num_dig-1)


def attack_subset(n0,n1,ORwith,ORwo,err=.001):
	n=n0+n1;
	poss=at.attack_no_covar(n0,n1,ORwo,err);
	#print poss;
	ret=[];
	for gen in poss:
		y=[1 for i in range(0,n+1)]
		for i in range(0,n0):
			y[i]=0;
			#lr=LR(C = 1e9);
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
			try:
				OR_cur=at.Log_Calc(y,x);
			except:
				continue;
			#lr.fit(np.asarray([x]).T,y)
			#OR_cur=math.exp(float(lr.coef_));
			if round_sig(OR_cur,err)==round_sig(ORwith,err):##abs(OR_cur-ORwith)<err:
				ret.append(i);
	#print "match!\n";
	#print len(ret);
	#print len(poss);
	return ret;


def test_sub(n0,n1,err=.001,x=[],y=[],getOR=False):
	n=n0+n1;
	if len(x)==0:
		x=[rand.randint(0,2) for i in range(0,n)]
	if len(y)==0:
		y=[1 for i in range(0,n)];
	maf=sum(x)/float(2*n)
	for i in range(0,n0):
		y[i]=0;

	ORwo=at.Log_Calc(y,x);
	x.append(rand.randint(0,2));
	y.append(1);
	#lr=LR(C = 1e9);
	#lr.fit(np.asarray([x]).T,y)
	ORwith=at.Log_Calc(y,x);
	ret=attack_subset(n0,n1,ORwith,ORwo,err=err);
	guess=int(mode(ret)[0])
	#print x[-1];
	if getOR:
		return [maf,ORwith,ORwo,guess,x[-1],int(guess==x[-1])];
	return guess==x[-1];




if __name__=="__main__":
	argv=sys.argv;
	n0=10;
	reps=10;
	n1=9;
	err=.001;
	if len(argv)>2:
		n0=int(argv[1]);
		n1=int(argv[2])
	if len(argv)>3:
		err=float(argv[3]);
	print "n0 equals "+str(n0);
	print "n1 equals "+str(n1);
	print "err equals "+str(err);
	correct=0;
	for i in range(0,reps):
		print i;
		correct=correct+int(test_sub(n0,n1,err));
	print correct/float(reps);





