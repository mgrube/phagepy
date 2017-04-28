import fcp
import pickle
import sys
from SampleManager import *

#Fetches a list of samples that have been recently inserted
def recent_inserts(loc, node):
	recents = pickle.loads(node.get(uri=loc + "/recentinserts", followRedirect=True)[1])
	return recents

def stats(loc, node):
	stats = pickle.loads(node.get(uri=loc + "/stats", followRedirect=True)[1])
	return stats

def fetchallsamples(loc, node):
	samples = pickle.loads(n.get(uri=loc + "/samplelist", followRedirect=True)[1])
	return samples

if __name__=="__main__":
	n = fcp.node.FCPNode()

	uri = "USK@760O9oWaTNUMfNkVzm0yvpihEhdaKasm6ssYIpVf8Cs,grC7jQbnR8Ar9jYY2YA9DPBojbG5ptPOGdhIeDDrD9Q,AQACAAE/phageproto/0"

	print "Welcome to Phage 0.0.1!"

	try:
		if sys.argv[1] == "--list-all":
			samples = fetchallsamples(uri, n)
			for v in samples.values():
				print "SHA256SUM: " + v.sha256sum + ", " + v.magictype + ", " + str(v.size)
			n.shutdown()
		if sys.argv[1] == "--list-inserted":
			samples = fetchallsamples(uri, n)
			for k in samples.values():
				try:
					print "SHA256SUM: " + k.sha256sum + ", " + k.magictype + ", " + k.chk + "," + str(k.size)
				except AttributeError:
					pass
			n.shutdown()
		if sys.argv[1] == "--grab-latest":
			newestinserts = recent_inserts(uri, n)
			for i in newestinserts:
				print "Retrieving " + i.sha256sum
				vxdata = n.get(i.chk, file=i.sha256sum)[1]
			n.shutdown()
	except IndexError:
		print "--list-all - produce a full list of stored samples"
		print "--list-inserted - produce a list of all samples that have been inserted"
		print "--grab-latest - download most recently available samples"

 
