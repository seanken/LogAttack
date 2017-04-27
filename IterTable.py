import numpy as np;
import scipy as sp;
import random as rand;
import pandas as pd;


class IterTable:
	def __init__(self,table):##table array of disease and covariate info
		self.is_done=False;
		T=[tuple(t) for t in table]
		self.cols=sorted(list(set(T)));
		self.counts={};
		for c in self.cols:
			self.counts[c]=0;
		for t in table:
			self.counts[tuple(t)]=self.counts[tuple(t)]+1;
		self.curTab=[[self.counts[t],0,0] for t in self.cols];
		self.n=len(table)
		self.y=[]
		self.cond=[];
		self.cov=[];
		for i in range(0,len(self.cols)):
			self.y.extend([self.cols[i][0] for j in range(0,self.counts[self.cols[i]])]);
			self.cov.extend([list(self.cols[i][1:]) for j in range(0,self.counts[self.cols[i]])]);

	##
	##sets conditions that table has to fufill
	##
	def setCond(self,cond):
		self.cond=[i for i in cond];


	def nextColumn(self,curCol):
		nextCol=[i for i in curCol]
		if nextCol[0]>0:
			nextCol[0]=nextCol[0]-1;
			nextCol[1]=nextCol[1]+1;
			return nextCol;
		if nextCol[1]>0:
			nextCol[1]=nextCol[1]-1;
			nextCol[2]=nextCol[2]+1;
			return nextCol;
		nextCol=[sum(nextCol),0,0];
		return nextCol;

	def meetCond(self):
		if self.is_done:
			return True;
		

	
	def nextCond(self):
		if len(self.cond)!=6:
			next();
			continue;
		while not self.meetCond():
			next();
			
	
	def next(self):
		for i in range(0,len(self.cols)):
			curCol=self.curTab[i];
			nxtCol=self.nextColumn(curCol);
			self.curTab[i]=nxtCol;
			if sum(nxtCol[1:])>0:
				return;
		self.is_done=True;
	
	
	

	def isDone(self):
		return self.is_done;

	def printIt(self):
		for i in range(0,len(self.cols)):
			print self.cols[i]
			print self.curTab[i]
			print "\n"

	
	def getTable(self):
		return [[i for i in c] for c in self.curTab];

	def get(self):
		x=[0 for i in range(0,self.n)]
		cur=0;
		for i in range(0,len(self.cols)):
			for j in range(0,3):
				num=self.curTab[i][j];
				x[cur:cur+num] =[j for k in range(0,num)];
				cur=cur+num;
		cov=[[i for i in c] for c in self.cov]
		cov=(np.asarray(cov).T).tolist();
		ret=[x]
		ret.extend(cov);
		ret=np.asarray(ret).T;
		#cov.append(x);
		#ret=np.asarray(cov);
		#ret=ret.T;
		return [[i for i in self.y],ret]





def testIterTable(n,numCovar):
	y=[rand.randint(0,1) for i in range(0,n)]
	cov=[[rand.randint(0,1) for i in range(0,n)] for j in range(0,numCovar)]
	Cov=[y];
	Cov.extend(cov);
	Cov=np.asarray(Cov).T
	iter=IterTable(Cov);

	iter.next();
	tab1=iter.getTable();
	print tab1;
	val=iter.get();
	print val;
	i=0;
	"""
	while not iter.isDone():
		print i;
		i=i+1;
		tab2=iter.getTable();
		iter.next();
		tab3=iter.getTable();
		#print iter.isDone();
		#print tab2[:2];
	print tab1;
	print tab2;
	print tab3;
	"""


if __name__=="__main__":
	testIterTable(20,2);


