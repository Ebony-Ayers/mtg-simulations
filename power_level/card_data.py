import os
import requests
import json
import urllib.request

def getDateFileName():
	r = requests.get("https://api.scryfall.com/bulk-data")
	data = json.loads(r.content.decode("utf-8"))
	for element in data["data"]:
		if element["type"] == "oracle_cards":
			downloadURL = element["download_uri"]
			fileName = "data/" + downloadURL[downloadURL.rfind("/")+1:]
			
			#check if the file already exists
			files = os.listdir("data/")
			for f in files:
				if os.path.isfile("data/" + f) and (("data/" + f) == fileName):
					print(">> Most up to date data already downloaded")
					return fileName
			
			#if no file exists download it
			print(">> Downloading the most up to date data")
			urllib.request.urlretrieve(downloadURL, fileName)
			return fileName

def parseData(fileName):
	rawData = None
	with open(fileName, 'r') as inputFile:
		rawData =  inputFile.read()
	jsonData = json.loads(rawData)
	print(">> Parsed data")
	return jsonData

def getParsedData():
	return parseData(getDateFileName())

if __name__ == "__main__":
	getParsedData(getDateFileName())
