import numpy as np;
import scipy as sp;
import math;
import random as rand;
from sklearn.linear_model import LogisticRegression as LR;
import pandas as pd;

##
##Performs the attack if no covariates
##OR is odds ratio
##n0 number controls, n1 number of cases
##err is allowed error in odds ratio
##returns num_match, the number of inputs giving the correct OR
##
def attack_no_covar(n0,n1,OR,err=.001):
	n=n0+n1;
	y=[1 for i in range(0,n)]
	for i in range(0,n0):
		y[i]=0;
	num_match=0;
	ret=[];
	##iterate through all possibilities and test
	for i0 in range(0,n0+1):##number in controls with 2 minor alleles
		for i1 in range(0,(n0-i0+1)):##number in controls with 1 minor alleles
			for j0 in range(0,n1+1):##number in cases with 2 minor alleles
				for j1 in range(0,(n1-j0+1)):##number in cases with 1 minor alleles
					lr=LR(C = 1e9);
					i2=n0-i0-i1;
					j2=n1-j0-j1;
					x=[0 for i in range(0,n)];

					x[:i0]=[2 for i in range(0,i0)];
					cur=i0;
					x[cur:cur+i1]=[1 for i in  range(0,i1)];
					cur=cur+i1;
					cur=cur+i2
					x[cur:cur+j0]=[2 for i in  range(0,j0)];
					cur=cur+j0;
					x[cur:cur+j1]=[1 for i in  range(0,j1)];
					lr.fit(np.asarray([x]).T,y)
					OR_cur=math.exp(float(lr.coef_));
					if abs(OR_cur-OR)<err:
						num_match=num_match+1;
						ret.append([i0,i1,i2,j0,j1,j2]);
						print "match!\n";
	return ret;

##
##generates fake data
##
def test_attack_nocovar(n0,n1,err=.001):
	lr=LR(C = 1e9);
	n=n0+n1;
	x=[rand.randint(0,2) for i in range(0,n)]
	y=[1 for i in range(0,n)]
	for i in range(0,n0):
		y[i]=0;
	lr.fit(np.asarray([x]).T,y)
	OR=math.exp(float(lr.coef_));
	ret=attack_no_covar(n0,n1,OR,err)
	print "The number of matches is: "+str(len(ret));
	print OR;
	for r in ret:
		print r;





##
##Performs the attack if one covariates
##OR is odds ratio
##y pheno vector, covar covariance vector
##err is allowed error in odds ratio
##returns num_match, the number of inputs giving the correct OR
##ret=set of possible i0,etc.
##
def attack_one_covar(y,covar,n0,n1,OR,ret=[],err=.001):
	n=n0+n1;
	y=[1 for i in range(0,n)]
	for i in range(0,n0):
		y[i]=0;
	num_match=0;
	#ret=[];
	k0=min([i for i in range(0,len(y)) if covar[i]==0])##number with y=0,covar=1
	k1=min([i for i in range(0,len(y)) if covar[i]==0 and y[i]==1])
	num_match=0;
	ret2=[];
	##iterate through all possibilities and test
	for r in ret:
		nextIt=False;
		for i0 in range(0,r[0]+1):
			for i1 in range(0,r[1]+1):
				if i0+i1>k0:
					continue;
				if r[0]+r[1]-i0-i1>n0-k0:
					continue;
				for j0 in range(0,r[0]+1):
					for j1 in range(0,r[1]+1):
						if nextIt:
							continue;
						if j0+j1>k1-n0:
							continue;
						if r[3]+r[4]-j0-j1>n1-(n0-k1):
							continue;
						x=[0 for i in range(0,n)]
						x[:i0]=[2 for i in range(0,i0)];
						x[k0:k0+r[0]-i0]=[2 for i in range(0,r[0]-i0)];
						x[i0:i1+i0]=[1 for i in range(0,i1)];
						x[k0+r[0]-i0:k0+r[0]+r[1]-i0-i1]=[1 for i in range(0,r[1]-i1)];

						x[n0:n0+j0]=[2 for i in range(0,j0)];
						x[k1:k1+r[3]-j0]=[2 for i in range(0,r[3]-j0)];
						x[n0+j0:n0+j1+j0]=[1 for i in range(0,j1)];
						x[k1+r[3]-j0:k1+r[4]+r[3]-j0-j1]=[1 for i in range(0,r[4]-j1)];
						if len(x)!=len(covar):
							continue;
						lr=LR(C = 1e9);
						#print x;
						#print covar;
						lr.fit(np.asarray([x,covar]).T,y)
						OR_cur=math.exp(float(lr.coef_[0,0]));
						if abs(OR_cur-OR)<err:
							num_match=num_match+1;
							ret2.append(x);
							nextIt=True;

	return ret2;



##
##generates fake data
##
def test_attack_onecovar(n0,n1,err=.001):
	lr=LR(C = 1e9);
	n=n0+n1;
	x1=[rand.randint(0,2) for i in range(0,n)]
	covar=[rand.randint(0,1) for i in range(0,n)]
	covar[:n0]=sorted(covar[:n0],reverse=True)
	covar[n0:]=sorted(covar[n0:],reverse=True)

	
	y=[1 for i in range(0,n)]
	for i in range(0,n0):
		y[i]=0;
	lr.fit(np.asarray([x1]).T,y)
	OR=math.exp(float(lr.coef_));
	ret=attack_no_covar(n0,n1,OR,err)
	print "The number of matches is: "+str(len(ret));
	print OR;
	for r in ret:
		print r;
		print sum([((2-i)%3)*r[i] for i in range(0,len(r))])

	#print covar;
	#	print x1;
	lr.fit(np.asarray([x1,covar]).T,y)
	OR_cov=math.exp(float(lr.coef_[0,0]));

	ret2=attack_one_covar(y,covar,n0,n1,OR_cov,ret,err)
	print "results"
	print len(ret);
	for r in ret2:
			print r;



if __name__=="__main__":
	n0=20;
	n1=19;
	err=.01;
	test_attack_onecovar(n0,n1,err);





