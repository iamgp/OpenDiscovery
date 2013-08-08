import urllib2
from xml.etree import ElementTree as ET
import csv
import os

__author__ = 'Gareth Price'
__email__ = 'gareth.price@warwick.ac.uk'
__version__ = '1.0'
__license__ = 'MIT'

class Compound:
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.smiles = None
		self.inchikey = None
		self.mf = None
		self.rb = None
		self.chemblid = None
		self.prefname = None
		self.knowndrug = None
		self.medchem = None
		self.ruleof3 = None
		self.mw = None
		self.alogp = None
		self.acidpka = None
		self.basicpka = None
		self.logp = None
		self.logd = None

	@property
	def Smiles(self):
		if self.smiles == None:
			self.loadDataForCompound()
		return self.smiles

	@property
	def stdInChiKey(self):
		if self.inchikey == None:
			self.loadDataForCompound()
		return self.inchikey

	@property
	def molecularFormula(self):
		if self.mf == None:
			self.loadDataForCompound()
		return self.mf

	@property
	def rotatableBonds(self):
		if self.rb == None:
			self.loadDataForCompound()
		return self.rb

	@property
	def chemblId(self):
		if self.chemblid == None:
			self.loadDataForCompound()
		return self.chemblid

	@property
	def preferredCompoundName(self):
		if self.prefname == None:
			self.loadDataForCompound()
		return self.prefname

	@property
	def knownDrug(self):
		if self.knowndrug == None:
			self.loadDataForCompound()
		return self.knowndrug

	@property
	def medChemFriendly(self):
		if self.medchem == None:
			self.loadDataForCompound()
		return self.medchem

	@property
	def passesRuleOfThree(self):
		if self.ruleof3 == None:
			self.loadDataForCompound()
		return self.ruleof3

	@property
	def molecularWeight(self):
		if self.mw == None:
			self.loadDataForCompound()
		return self.mw
	@property
	def alogp(self):
		if self.alogp == None:
			self.loadDataForCompound()
		return self.alogp

	@property
	def acdAcidicPka(self):
		if self.acidpka == None:
			self.loadDataForCompound()
		return self.acidpka

	@property
	def acdBasicPka(self):
		if self.basicpka == None:
			self.loadDataForCompound()
		return self.basicpka

	@property
	def acdLogp(self):
		if self.logp == None:
			self.loadDataForCompound()
		return self.logp

	@property
	def acdLogd(self):
		if self.logd == None:
			self.loadDataForCompound()
		return self.logd

	def loadDataForCompound(self):
		if self.key == 'smiles':
			searchurl = 'https://www.ebi.ac.uk/chemblws/compounds/smiles/%s' % self.value
		elif self.key == 'inchikey':
			searchurl = 'https://www.ebi.ac.uk/chemblws/compounds/stdinchikey/%s' % self.value

		response = urllib2.urlopen(searchurl)
		tree = ET.parse(response)
		
		print tree

		self.smiles = self.findValueForKey('smiles', tree)
		self.inchikey = self.findValueForKey('stdInChiKey', tree)
		self.mf = self.findValueForKey('molecularFormula', tree)
		self.rb = self.findValueForKey('rotatableBonds', tree)
		self.chemblid = self.findValueForKey('chemblId', tree)
		self.prefname = self.findValueForKey('preferredCompoundName', tree)
		self.knowndrug = self.findValueForKey('knownDrug', tree)
		self.medchem = self.findValueForKey('medChemFriendly', tree)
		self.ruleof3 = self.findValueForKey('passesRuleOfThree', tree)
		self.mw = self.findValueForKey('molecularWeight', tree)
		self.alogp = self.findValueForKey('alogp', tree)
		self.acidpka = self.findValueForKey('acdAcidicPka', tree)
		self.basicpka = self.findValueForKey('acdBasicPka', tree)
		self.logp = self.findValueForKey('acdLogp', tree)
		self.logd = self.findValueForKey('acdLogd', tree)

	def findValueForKey(self, key, tree):
		try:
			return tree.find('./%s' % key).text
		except:
			return ''

	def describe(self):
		dictionary = {'smiles': self.Smiles, 'stdInChiKey': self.inchikey, 'molecularFormula': self.mf, 'rotatableBonds': self.rb, 'chemblId':self.chemblid, 'preferredCompoundName': self.prefname, 'medChemFriendly': self.medchem, 'passesRuleOfThree': self.ruleof3, 'molecularWeight': self.mw, 'acdAcidicPka':self.acidpka, 'alogp':self.alogp, 'acdBasicPka':self.basicpka, 'acdLogp':self.logp, 'acdLogd': self.logd}
		return dictionary

def writeCSV(compound, file, headers):
	file =  os.path.expanduser(file)
	with open('%s.csv' % file,'wb') as f:
		w = csv.DictWriter(f, compound.describe().keys())
		if headers == True:
			w.writeheader()
		w.writerow(compound.describe())

def status():
	searchurl = 'http://www.ebi.ac.uk/chemblws/status/'
	response = urllib2.urlopen(searchurl)
	tree = ET.parse(response)
	root = tree.getroot()
	print root[0].text

def usage():
	print 'import chembl'
	print 'then: c = chembl.Compound(\'inchikey OR smiles\', InChiKeyString (or) SmilesString)'
	print 'can use c.describe() to return a dictionary of return values from the API'
	print 'or chemble.writeCSV(c, \'path/to/where/csv/should/be/saved/without/extension)'
	print '... to write a csv.'
