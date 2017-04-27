import numpy as np;
import scipy as sp;
import Attack_subset_Logit as asl;
import sys;
import pandas;
import Attack_Logit as at;
from loadData import loadData;
from scipy.stats import mode;
import random as rand;

def test_sub(x2,y,err=.001,withConf=False,num=0):
	print num;
	n=len(y);
	n1=int(sum(y));
	n0=n-n1;
	x=[i for i in x2]
	try:
		maf=sum(x)/float(2*n)
	except:
		return [-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,0.0]

	
	ORwo=at.Log_Calc(y[1:],x[1:]);

	ORwith=at.Log_Calc(y,x);
	if ORwo==-1 or ORwith==-1:
		return [maf,ORwith,ORwo,-1.0,-1.0,-1.0,0.0]
	ret=[maf,ORwith,ORwo,-1.0,-1.0,-1.0,0.0]
	try:
		ret=asl.attack_subset(n0,(n1-1),ORwith,ORwo,err=err);
	except:
		return ret;
	conf=0;
	try:
		guess=int(mode(ret)[0])
		conf=len([i for i in ret if i==guess])/float(len(ret))
	except:
		print [ORwith,ORwo,len(ret)];
		return [maf,ORwith,ORwo,-1.0,-1.0,-1.0,0.0]
	if withConf:
		if conf<1.0:
			guess=-1;
	ret=[maf,ORwith,ORwo,conf,guess,x[0],int(guess==x[0])];
	return [float(i) for i in ret]


def attack(n0,n1,filename="",err=.001,minMAF=.05,numSNP=1000,withConf=False):
	print "Load and clean up data"
	if len(filename)==0:
		filename="../GWAS/cleaned2";
	[y,BED]=loadData(filename);
	n=len(y);
	I0=[i for i in range(0,n) if y[i]==0]
	I1=[i for i in range(0,n) if y[i]==1]
	I0=I0[:n0];
	I1=I1[:n1];
	I=I1;
	I.extend(I0);
	y=[y[i] for i in I];
	BED=BED[I,:];
	m=BED.sid_count;
	n=len(y);
	print m;

	maf=np.sum(BED.read().val,axis=0)/float(2*n);
	print maf[:10]
	if len(maf)!=m:
		print "Ouch!";
	J=[j for j in range(0,m) if maf[j]>= minMAF and maf[j]<(1-minMAF)];
	rand.shuffle(J);
	BED=BED[:,J];
	maf=[maf[j] for j in J];
	
	m=len(J);
	print m;
	
	BEDTemp=BED[0,:100]
	print BEDTemp.read().val
	if numSNP>0:
		BED=BED[:,:numSNP];
		maf=maf[:numSNP];
		m=numSNP;
	A=BED.read().val;
	correct=A[0];
	"""
	BED2=BED[1:,:];
	A2=BED2.read().val;
	OR=[];
	ORwo=[];
	for i in range(0,m):
		try:
			OR[i]=;
		except:
			OR[i]=-1.0;
		try:
			ORwo[i]=;
		except:
			ORwo=-1.0
	"""
	snpNames=BED.sid;
	print "Time to run guess!"
	print A.shape;
	guess=[test_sub(A[:,i],y,err,withConf,i) for i in range(0,m)]
	guess=[[float(i) for i in g] for g in guess]
	return np.asarray(guess)
	






def genData(n0=10,n1=10,reps=10,SD=4,numSNP=100,err=.001,savename=""):
	argv=[]

	RES=[]



	if len(savename)==0:
		savename="data/Res_"+str(n0)+"_"+str(n1)+"_"+str(SD)+".txt"
	print "n0 equals "+str(n0);
	print "n1 equals "+str(n1);
	print "err equals "+str(err);
	A=attack(n0,n1,filename="",err=SD,minMAF=.05,numSNP=numSNP,withConf=True)
	print len(A);
	#print A;
	print sum(A[:,-1])/float(len(A))
	I=[i for i in range(0,len(A)) if A[i,-4]>.99]
	print len(I)/float(len(A));
	if len(I)>0:
		print sum(A[I,-1])/float(len(I))
	i=-1;
	j=-1;
	print str(i)+" "+str(j)+" "+str(len([k for k in range(0,len(A)) if A[k,-3]==i and A[k,-2]==j]))
	for i in range(-1,3):
		for j in range(0,3):
			print str(i)+" "+str(j)+" "+str(len([k for k in range(0,len(A)) if A[k,-3]==i and A[k,-2]==j]))


	np.save(savename,arr=A);


if __name__=="__main__":
	args=sys.argv
	n0=int(args[1])
	n1=int(args[2])
	SD=int(args[3])
	numSNPs=int(args[4])
	genData(n0=n0,n1=n1,SD=SD,numSNP=numSNPs);












