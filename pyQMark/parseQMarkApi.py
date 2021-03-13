# Qingmang Mark API based on Python
# https://github.com/liutongl5/QMark-API
# Email: liutongl5+QMark@gmail.com

import copy
import re
import ssl, urllib.request
import xml.etree.ElementTree as ET
import json, html


def strRetrieveQMark(userId=1, userSecret=""):
	urlQMarkAPI = "https://qingmang.me/users/"+str(userId)+"/feed/?secret="+userSecret
	strQMarkXml = None

	with urllib.request.urlopen(urlQMarkAPI, context=ssl.SSLContext()) as response:
		strQMarkXml = response.read().decode('UTF-8')
		# print(strQMarkXml) # debug

	return strQMarkXml

def dictParseQMark(userId=1, userSecret="", hideSecret=False):
	strQMarkXml = strRetrieveQMark(userId, userSecret)
	etQMarkXmlRoot = None
	try:
		etQMarkXmlRoot = ET.fromstring(strQMarkXml)
		etQMarkXmlRoot = etQMarkXmlRoot.find("channel")
	except Exception as e:
		print("Invalid RSS")
		return {"valid": False, "message": "Invalid RSS"}

	# ============================================================
	# Parse XML into dictQMark
	dictQMark = {"valid": True}

	# Include Title
	etQmarkProcessing = etQMarkXmlRoot.find("title")
	dictQMark["title"] = etQmarkProcessing.text

	# Include LastBuildDate
	etQmarkProcessing = etQMarkXmlRoot.find("lastBuildDate")
	dictQMark["lastBuildDate"] = etQmarkProcessing.text

	if (hideSecret) :
		# As of Mar 2021, secret element is the first and only element with attribute "rel"
		etQmarkProcessing = etQMarkXmlRoot.find('*[@rel="self"]')
		# print(etQMarkSecret) # debug
		dictQMark["link"] = etQmarkProcessing.attrib['href']

	# Include Mark Items
	dictQMark["items"] = []
	for etQMarkXmlItem in etQMarkXmlRoot.findall("item"):
		dictQMarkItem = {}

		# Retrieve Marked Article Title
		etQmarkProcessing = etQMarkXmlItem.find("title")
		if (etQmarkProcessing is None):
			dictQMarkItem["title"] = ""
		else:
			dictQMarkItem["title"] = etQmarkProcessing.text

		# Include Marked Article Link
		etQmarkProcessing = etQMarkXmlItem.find("link")
		if (etQmarkProcessing is None):
			dictQMarkItem["link"] = ""
		else:
			dictQMarkItem["link"] = etQmarkProcessing.text

		etQmarkProcessing = etQMarkXmlItem.find("description")
		etQmarkProcessing = ET.fromstring( "<div>"+html.unescape(etQmarkProcessing.text.strip())+"</div>" )
		# print( ET.tostring(etQmarkProcessing, encoding='unicode') )
		# Include Quotes (if any)
		etQMarkItemQuotes = etQmarkProcessing.find("blockquote")
		dictQMarkItem["quotes"] = []
		if etQMarkItemQuotes is not None:
			for etQuote in etQMarkItemQuotes:
				dictQMarkItem["quotes"].append( ET.tostring(etQuote, encoding='unicode') )
		# Include Notes (if any)
		etQMarkItemNotes = etQmarkProcessing.find("aside")
		dictQMarkItem["notes"] = []
		if etQMarkItemNotes is not None:
			# print("text: "+etQMarkItemNotes.text+"endtext") # debug
			dictQMarkItem["notes"].append( ET.tostring(etQMarkItemNotes, encoding='unicode') )

		# Include Mark Item Link 
		etQmarkProcessing = etQMarkXmlItem.find("guid")
		dictQMarkItem["guid"] = etQmarkProcessing.text

		# Include Mark Item PubDate
		etQmarkProcessing = etQMarkXmlItem.find("pubDate")
		dictQMarkItem["pubDate"] = etQmarkProcessing.text

		dictQMark["items"].append( dictQMarkItem )
		# print(json.dumps(dictQMarkItem)) # debug

	return dictQMark

def main():
	# dictQMark = dictParseQMark(11, hideSecret=True)
	# dictQMark = dictParseQMark(11)

	if ("valid" in dictQMark and dictQMark["valid"] is True):
		print( json.dumps(dictQMark) )
	else:
		print("Error Retrieving XML!")

if __name__ == '__main__':
	main()
