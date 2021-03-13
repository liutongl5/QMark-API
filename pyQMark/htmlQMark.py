# Qingmang Mark API based on Python
# https://github.com/liutongl5/QMark-API
# Email: liutongl5+QMark@gmail.com

import xml.etree.ElementTree as ET

from parseQMarkApi import dictParseQMark

def htmlQMark(userId=1, userSecret="", hideSecret=False):
	dictQMark = dictParseQMark(userId, userSecret, hideSecret)
	return htmlQMarkDict( dictQMark )

def htmlQMarkDict( dictQMark ):
	etQMarkHtml = ET.Element("div", attrib={"class": "divQMark"})
	etQMarkHtmlCursor = etQMarkHtml

	# Include Title
	etQmarkProcessing = ET.Element("h1", attrib={"class": "h1QMarkTitle"})
	etQmarkProcessing.text = dictQMark["title"]
	etQMarkHtmlCursor.append(etQmarkProcessing)

	# Include LastBuildDate
	etQmarkProcessing = ET.Element("time", attrib={"class": "timeQMarkTime", "datetime": dictQMark["lastBuildDate"]})
	etQmarkProcessing.text = dictQMark["lastBuildDate"]
	etQMarkHtmlCursor.append(etQmarkProcessing)

	# Include Mark Items
	etQMarkHtmlCursor = ET.Element("div", attrib={"class": "divQMarkAllItems"})
	etQMarkHtml.append(etQMarkHtmlCursor)
	for dictQMarkItem in dictQMark["items"]:
		etQMarkHtmlCursor = etQMarkHtml.find('div[@class="divQMarkAllItems"]')
		etQmarkProcessing = ET.Element("div", attrib={"class": "divQMarkItem"})
		etQMarkHtmlCursor.append(etQmarkProcessing)
		etQMarkHtmlCursor = etQmarkProcessing

		# Retrieve Marked Article Title
		strQMarkItemTitle = dictQMarkItem["title"]

		# Include Marked Article Link
		etQmarkProcessing = ET.Element("a", attrib={"href": dictQMarkItem["link"]})
		etQmarkProcessing.text = strQMarkItemTitle
		etQMarkHtmlCursor.append(etQmarkProcessing)

		# Include Quotes (if any)
		etQmarkProcessing = ET.Element("div", attrib={"class": "divQMarkItemQuote"})
		for etQuote in dictQMarkItem["quotes"]:
			etQmarkProcessing.append( ET.fromstring(etQuote) )
		etQMarkHtmlCursor.append(etQmarkProcessing)
		# Include Notes (if any)
		etQmarkProcessing = ET.Element("div", attrib={"div": "divQMarkItemNote"})
		for etNote in dictQMarkItem["notes"]:
			etQmarkProcessing.append( ET.fromstring(etNote) )
		etQMarkHtmlCursor.append(etQmarkProcessing)

		# Include Mark Item Link 
		etQmarkProcessing = ET.Element("p", attrib={"class": "pQMarkItemDate"})
		etQMarkHtmlCursor.append(etQmarkProcessing)
		etQMarkHtmlCursor = etQmarkProcessing
		etQmarkProcessing = ET.Element("a", attrib={"href": dictQMarkItem["guid"]})
		etQMarkHtmlCursor.append(etQmarkProcessing)
		etQMarkHtmlCursor = etQmarkProcessing

		# Include Mark Item PubDate
		etQmarkProcessing = ET.Element("time", attrib={"class": "timeQMarkTime", "datetime": dictQMarkItem["pubDate"]})
		etQmarkProcessing.text = dictQMarkItem["pubDate"]
		etQMarkHtmlCursor.append(etQmarkProcessing)


	strQMarkHtml = ET.tostring( etQMarkHtml, encoding='unicode', method='html' )
	# print( strQMarkHtml ) # debug
	return strQMarkHtml

def main():
	# print( htmlQMark(userId=11,userSecret="YourSecret", hideSecret=True) )

if __name__ == '__main__':
	main()
