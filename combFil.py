if __name__=="__main__":
	dct={};
	for i in range(-1,3):
		for j in range(0,3):
			dct[(i,j)]=0;
	for k in range(1,11):
		fil=open("100peop_"+str(k)+".txt");
		lines=fil.readlines();
		fil.close();
		lines=[l.split() for l in lines]
		lines=[s for s in lines if len(s)==3]
		lines=[s for s in lines if s[0][0]!="n" and s[0][0]!="e"]
		print len(lines);
		print "hi"
		print lines
		lines=[[int(i) for i in s] for s in lines]
		lines=[l for l in lines if l[1]>-1];
		for l in lines:
			dct[tuple(l[:2])]=l[2]+dct[tuple(l[:2])];
	print dct;

	fil=open("100peopv2.txt","w")
	for d in dct:
		fil.write(str(d[0])+" "+str(d[1])+" "+str(dct[d])+"\n");
	fil.close();


