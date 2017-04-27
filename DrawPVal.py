import seaborn as sns;
import pandas as pd;
import numpy as np;
import matplotlib.pyplot as plt;



##A is 4 by 3, first row rep no in, etc
def drawIt(A):
	sns.set(font_scale=2) 
	DF=pd.DataFrame(A,columns=[0,1,2,3,4,5,6,7,r"$\geq 8$"],index=[0,1,2,3,4,5,6,7,r"$\geq 8$"]);
	DF.columns.name=r"True $-log_{10}$(P-value)"
	DF.index.name=r"Perturbed $-log_{10}$(P-value)"
	print DF;
	DF.index=DF.index[::-1]
	print DF
	sns.heatmap(DF,vmin=0.0,vmax=1.0)#,annot=True,annot_kws={"size": 20});
	plt.show();



def drawFromFile(filename):
	fil=open(filename);
	line=fil.readline();
	lines=line.split("\r")
	fil.close();
	A=[l.strip().split() for l in lines];
	A=[[float(i) for i in s] for s in A if len(s)>2]
	n=len(A)
	A=[A[n-i-1] for i in range(0,n)]
	print A;
	A=np.asarray(A);
	drawIt(A);



if __name__=="__main__":
	filename="pvals.txt"
	drawFromFile(filename);
