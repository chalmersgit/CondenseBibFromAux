import sys
import argparse
from pathlib import Path
import re

def getUsedCitations(fileName):
	filePath = Path(fileName)
	if not filePath.is_file():
		sys.exit("Error, could not find file: "+str(fileName))

	# Load in all citations that were used
	with open(filePath, mode='r') as fid:
		usedCitations = [line.strip() for line in fid if line.startswith("\\citation")]

	# Some citations use multiple in one line (e.g., "\cite{a,b,c}"), so let's break them up
	citationLabels = []
	for citation in usedCitations:
		citationLabelsLine = re.search('{(.*)}', citation).group(0)[1:-1].split(',') 
		for citationLabel in citationLabelsLine:
			citationLabels.append(citationLabel)

	return list(set(citationLabels)) # removes duplicates and return

def getAllBibEntries(fileName):
	filePath = Path(fileName)
	if not filePath.is_file():
		sys.exit("Error, could not find file: "+str(fileName))
	data = filePath.read_text()
	nCharacters = len(data)
	bibDict = {}
	nEntries = 0
	startIdx = 0
	endIdx = 0
	i = 0
	while i < nCharacters:
		if data[i]=="@":
			bibtexTagIdx = i
		if data[i]=='{':
			startIdx = i
			labelEndIdx = None
			nestCount = 0
			for j in range(i+1,nCharacters):
				if labelEndIdx is None and data[j]==',':
					labelEndIdx = j
				if data[j]=='{':
					nestCount+=1
				if data[j]=='}':
					nestCount-=1
				if nestCount<0:
					endIdx = j+1
					i = j
					bibEntry = data[bibtexTagIdx:startIdx]+data[startIdx:endIdx]
					bibLabel = data[startIdx+1:labelEndIdx]
					bibDict[bibLabel] = bibEntry
					break
		i+=1
	return bibDict

def getAllBibLabels(fileName):
	filePath = Path(fileName)
	if not filePath.is_file():
		sys.exit("Error, could not find file: "+str(fileName))

	# Gets all citation labels
	with open(filePath, mode='r') as fid:
		allCitations = [re.search('{([^,;]+),', line).group(1).strip() for line in fid if line.startswith("@")]
	return allCitations

def generateBib(bibDict,citationLabels, outputFn='_outputbib.bib'):
	f = open(outputFn, "w") 
	f.write("%% This BibTeX bibliography file was created from pybib.\n\n")
	for label in citationLabels:
		f.write(bibDict[label])
		f.write('\n\n')
	f.close()

def condenseBibFromAux(bibFile, auxFile, outputFn='_outputbib.bib'):
	print("Generating a condensed .bib file from .aux:", bibFile, auxFile)
	print("Saving as:",outputFn)

	bibDict = getAllBibEntries(bibFile)
	usedCitations = getUsedCitations(auxFile)
	generateBib(bibDict,usedCitations,outputFn)


if __name__ == "__main__":
	sys.argv = ['', '--bib', 'bibFile.bib', '--aux', 'auxFile.aux', '--output', '_outputBibFile.bib']

	parser = argparse.ArgumentParser(description='Test.')
	parser.add_argument('--bib', action='store', type=str, help='.bib file', required=True)
	parser.add_argument('--aux', action='store', type=str, help='.aux file', required=True)
	parser.add_argument('--output', action='store', type=str, help='output filename', default='_outputbib.bib', required=False)

	args = parser.parse_args()
	condenseBibFromAux(args.bib, args.aux, args.output)


