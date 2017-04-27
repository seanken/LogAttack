import numpy as np;
import scipy as sp;
import math;
import Attack_Logit as AL;
import random as rand;
from statsmodels.discrete.discrete_model import Logit as LR;
import pandas as pd;
import sys;
sys.path.insert(1,"/usr/local/lib/python2.7/dist-packages")
from statsmodels.tools.tools import add_constant as AC
from IterTable import *;
from numpy.linalg import matrix_rank as MatR;
from sympy.matrices import Matrix;
from sympy.solvers.solveset import linsolve;

##
##Performs the attack if no covariates
##OR is odds ratio
##n0 number controls, n1 number of cases
##err is allowed error in odds ratio
##returns num_match, the number of inputs giving the correct OR
##
def attack(y,cov,OR,err=.001,bnd=.5,numStep=10):
	n=n0+n1;
	num_match=0;
	ret=[];
	COV=[y];
	COV.extend(cov);
	COV=np.asarray(COV).T
	iter=IterTable(COV);
	cur=0;
	iter.next();
	[yCur,covCur]=iter.get();
	while not iter.isDone():
		#print cur;
		cur=cur+1;
		[yCur,covCur]=iter.get();
	
		lr=LR(yCur,AC(covCur,False))
		try:
			res_lr=lr.fit(disp=0)
		except:
			iter.next();
			continue;

		OR_cur=1.0;

		try:
			OR_cur=math.exp(float(res_lr.params[0]));
		except:
			iter.next();
			continue;
		if abs(OR_cur-OR)<err:
			print "match"
			num_match=num_match+1;
			ret.append(iter.getTable());
		#if abs(OR-OR_cur)/OR_cur>bnd:
		#for i in range(0,numStep):
		#iter.next();
		iter.next();
	return ret;
	


##
##generates fake data
##
def test_attack(n0,n1,numCov,err=.001):
	n=n0+n1;
	x=[rand.randint(0,2) for i in range(0,n)]
	y=[1 for i in range(0,n)]
	for i in range(0,n0):
		y[i]=0;
	covs=[[rand.randint(0,1) for i in range(0,n)] for j in range(0,numCov)]
	ORs=[];
	for i in range(0,numCov):
		print i;
		ret=[x];
		ret.append(covs[i]);
		X=np.asarray(ret).T
		X=AC(X,False);
		lr=LR(y,X);
		res_lr=lr.fit(disp=0)
		OR=math.exp(float(res_lr.params[0]));
		ret.append(attack(y,covs,OR,err));
		ORs.append(OR)
	print "The number of matches is: "
	for r in ret:
		str(len(r));
	print ORs;
	for r in ret:
		print r;
	print len(ret);

##
##Helper function
##
def listToDict(r):
	dct={}
	dct[(0)]=[r[0],r[1],r[2]];
	dct[(1)]=[r[3],r[4],r[5]];
	return dct;

##
##combines top i covariates with the i+1st
##
def combineDct(dctt1,dct2,cnt):
	if len(dct1)==0 or len(dct2)==0:
		return [];
	ret=[];
	b=[0 for i in range(0,8*len(dct1))];
	A=[[0 for i in range(0,6*len(dct1))] for j in range(0,8*len(dct1))]

	cnt_keys=[c for c in cnt]

	cnt_dct={}
	for i in range(0,len(cnt)):
		cnt_dct[cnt_keys[i]]=i


	num=0;
	for j in range(0,3):
		for d in dct1:
			val1=d+(1);
			val2=d+(0);
			b[num]=dct1[d][j];
			A[num][3*cnt_dct[val1]+j]=1;
			A[num][3*cnt_dct[val2]+j]=1;
			num=num+1;
			val1=(1)+d;
			val2=(0)+d;
			b[num]=dct2[d][j];
			A[num][3*cnt_dct[val1]+j]=1;
			A[num][3*cnt_dct[val2]+j]=1;
			num=num+1;
	for d in dct:
		val1=d+(1);
		val2=d+(0);
		b[num]=cnt[val1];
		for j in range(0,3):
			A[num][3*cnt_dct[val1]+j]=1;
		num=num+1;
		b[num]=cnt[val2];
		for j in range(0,3):
			A[num][3*cnt_dct[val2]+j]=1;
		num=num+1;
	#A=np.asarray();
	poss=[];
	A=Matrix(A);
	b=Matrix(b);

	linsolve()




def makeMat(m):
	dct=[(0),(1)]
	for i in range(1,m):
		dctnew=[];
		for d in dct:
			dctnew.append((d+(0)))
			dctnew.append((d+(1)))
	print dct;

	A=[[0 for i in range(0,6*len(dct))] for j in range(0,8*len(dct))]
	
	cnt_keys=[c for c in dct]
	
	cnt_dct={}
	for i in range(0,len(dct)):
		cnt_dct[cnt_keys[i]]=i
	
	
	num=0;
	for j in range(0,3):
		for d in dct:
			val1=d+(1);
			val2=d+(0);

			A[num][3*cnt_dct[val1]+j]=1;
			A[num][3*cnt_dct[val2]+j]=1;
			num=num+1;
			val1=(1)+d;
			val2=(0)+d;

			A[num][3*cnt_dct[val1]+j]=1;
			A[num][3*cnt_dct[val2]+j]=1;
			num=num+1;

	for d in dct:
		val1=d+(1);
		val2=d+(0);
		b[num]=cnt[val1];
		for j in range(0,3):
			A[num][3*cnt_dct[val1]+j]=1;
		num=num+1;
		b[num]=cnt[val2];
		for j in range(0,3):
			A[num][3*cnt_dct[val2]+j]=1;
		num=num+1;
	A=np.asarray(A);
	print num;
	print MatR(A)
	print 6*len(dct)



##
##combines top i covariates with the i+1st
##
def combineRes(lst1,lst2,cnt):
	ret=[];
	for dct1 in lst1:
		for dct2 in lst2:
			dcts=combineDct(dct1,dct2,cnt);
			ret.extend(dcts);
	return ret;

##chosen list of marginals to be combined
##numchose is the number of marginals chosen so far
##poss is all possible marginals
##dctCov maps from possible combs of covariates to index
##cnt maps from possible combs of covariates to counts
def testAll(chosen,numchose,poss,dctCov,cnt):
	ret=[];
	if numchose<len(poss):
		for i in range(0,len(poss[numchose])):
			next=[c for c in chosen];
			next.append(poss[numchose][i]);
			ret.extend(testAll(next,numchose+1,poss,dctCov))
		return ret;


	numEq=len(dctCov)+sum([len(c) for c in chosen]);
	b=[0 for i in range(0,numEq)];
	A=[[0 for i in range(0,3*len(dctCov))] for j in range(0,numEq)]
	num=0;
	##add eqations from histogram
	for d in dctCov:
		b[num]=cnt[d]
		for j in range(0,3):
			A[num][3*dctCov[d]+j]=1
		num=num+1;
	for i in range(0,len(chosen)):
		for k in range(0,6):
			b[num+k]=chosen[i][k]
		for d in dctCov:
			for k in range(0,2):
				for j in range(0,3):
					if d[i]==k:
						A[num+3*k+j][3*dctCov[d]+j]=1
		num=num+6;
	##want all nice solutions to Ax=b!!
	A=Matrix(A);
	b=Matrix(b);

	##
	##FINISH!!
	##
	solution=linsolve((A,b));

##
##generates fake data
##
def test_attack_pheno(n,numCov,err=.001):
	#n=n0+n1;
	x=[rand.randint(0,2) for i in range(0,n)]
	#y=[1 for i in range(0,n)]
	#for i in range(0,n0):
	#	y[i]=0;
	covs=[[rand.randint(0,1) for i in range(0,n)] for j in range(0,numCov)]
	ORs=[];
	ret=[];
	for i in range(0,numCov):
		print i;
		y=covs[i]
		#ret=[x];
		#ret.append(covs[i]);
		#X=np.asarray(ret).T
		X=AC(x,False);
		lr=LR(y,X);
		res_lr=lr.fit(disp=0)
		OR=math.exp(float(res_lr.params[0]));
		n1=sum(y);
		#n=len(y);
		n0=n-n1;
		ret.append(AL.attack_no_covar(n0,n1,OR,err=.001));
		ORs.append(OR)
	print "The number of matches is: "
	for r in ret:
		str(len(r));
	print ORs;
	marg=[]
	pos=0;
	for r in ret:
		marg.append([]);
		for i in r:
			marg[pos].append((i[0]+i[3],i[1]+i[4],i[2]+i[5]))
		pos=pos+1;
		print "\n"
	for mar in marg:
		print mar;
	#marg=[list(set(mar)) for mar in marg];
	inAll=[];
	notIn=False;
	for m in marg[0]:
		for mar in marg:
			if not m in mar:
				notIn=True;
		if not notIn:
			inAll.append(m);
		notIn=False;

	poss=[[ret[j][i] for i in range(0,len(ret[j])) if marg[j][i] in inAll] for j in range(0,len(ret))];
	poss=[[tuple(i) for i in p] for p in poss]


	posCov=[(0),(1)]
	for i in range(1,m):
		dctnew=[];
		for d in PosCov:
			dctnew.append((d+(0)))
			dctnew.append((d+(1)))
		posCov=dctnew
	dctCov={};
	for i in range(0,len(posCov)):
		dctCov[posCov[i]]=i;

	cnt={}
	for c in posCov:
		cnt[c]=0;
	for i in range(0,len(covs[0])):
		cnt[tuple([c[i] for c in covs])]=cnt[tuple([c[i] for c in covs])]+1;

	chosen=[];
	numchose=0;
	testAll(chosen,numchose,poss,dctCov,cnt)







def Log_Calc(y,x):
	x1=AC(x,False);
	lr=LR(y,x1);
	try:
		res_lr=lr.fit(disp=0)
	except:
		return -1;
	return math.exp(res_lr.params[0]);


if __name__=="__main__":
	argv=sys.argv;
	n0=10;
	n1=9;
	numCov=4;
	err=.001;
	if len(argv)>2:
		n0=int(argv[1]);
		n1=int(argv[2])
	if len(argv)>3:
		err=float(argv[3]);
	n=n0+n1;
	print "n0 equals "+str(n0);
	print "n1 equals "+str(n1);
	print "err equals "+str(err);
	#test_attack(n0,n1,numCov,err);
	test_attack_pheno(n,numCov,err=.001);





