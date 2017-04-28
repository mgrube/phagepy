from SampleManager import *
import sys
import os
import pickle

class SamplePublisher:

	def __init__(self):
		self.publickey = ""
		self.privatekey = ""
	
	#Write our public and private keys to the file specified at filename
	def keygen(self, node, filename):
		keys = node.genkey()
		self.publickey = keys[0]
		self.privatekey = keys[1]
		f = open(filename, "wb")
		pickle.dump(keys, f)
		f.close()

	def loadkeys(self, filename):
		f = open(filename, "rb")
		keys = pickle.load(f)
		f.close()
		self.publickey=keys[0]
		self.privatekey=keys[1]

	def publishbatch(self, batchsize, sm, node):
		insertedFiles = 0
		for s in sm.samples.values():
			if s.chk == "" and insertedFiles < batchsize:
				print "Publishing sample " + s.sha256sum
				sm.publishsample(s, node)
				print "Done publishing " + s.sha256sum
				insertedFiles += 1
		

	#We need this function in addition to SampleManager.importsamples
	#because when we publish our list to the world, we do it without
	#absolute file paths, as this would compromise anonymity.
	#This function saves the sample list with the paths in tact.
	#This allows us to manipulate our files a bit easier.
	def savesamplelist(self, filename, sampleman):
		f = open(filename, "wb")
		pickle.dump(sampleman.samples, f)
		f.close()

	def loadsamplelist(self, filename, sampleman):
		f = open(filename, "rb")
		samples = pickle.load(f)
		sampleman.samples = dict(sampleman.samples.items() + samples.items())
		f.close()
		

if __name__=="__main__":
	n = fcp.node.FCPNode()
	sp = SamplePublisher()
	sp.keygen(n, "test1")
	print "Pubkey: " + sp.publickey
	print "Privkey: " + sp.privatekey
	sm = SampleManager(sp.publickey, sp.privatekey)
	sm.addsampledir("/home/mike/lin/")
	sp.publishbatch(10, sm, n)
	print "Tell users to request from:  sm.publishupdate(n)"
	n.shutdown()
