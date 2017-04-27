import seaborn as sns;
import pandas as pd;
import numpy as np;
import matplotlib.pyplot as plt;



##A is 4 by 3, first row rep no in, etc
def drawIt(A):
	DF=pd.DataFrame(A,columns=[0,1,2],index=["No Guess",0,1,2]);
	DF.columns.name="True Genotype"
	DF.index.name="Guess"
	sns.heatmap(DF);
	plt.show();



def drawFromFile(filename):
	fil=open(filename);
	lines=fil.readlines();
	fil.close();
	A=[[0.0 for j in range(0,3)] for i in range(0,4)]
	lines=[l.strip().split() for l in lines]
	lines=[[int(i) for i in s] for s in lines]
	noGuess=0;
	guess=0;
	for s in lines:
		A[(s[0]+1)][s[1]]=float(s[2]);
		if s[0]==-1:
			noGuess=noGuess+s[2];
		else:
			guess=guess+s[2]
	print "Percent Guessed: "+str(guess/float(guess+noGuess));

	A=np.asarray(A);
	drawIt(A);



if __name__=="__main__":
	filename="drawIt.txt"
	drawFromFile(filename);
