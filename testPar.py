import pp;
import Attack;
import scipy;
import datetime;

def testIt():
	print "done!";
	k=0;
	j=datetime.datetime.now().time();
	for i in range(0,100000):
		k=k+1;
	k=datetime.datetime.now().time();
	return [j,k];

ncpus=5;
ppservers = ()
job_server = pp.Server(ncpus, ppservers=ppservers)

job1 = [job_server.submit(testIt, (), (), ("datetime",)) for i in range(0,100)];

#for job in job1:
ret=[job() for job in job1];
print ret[:6];
