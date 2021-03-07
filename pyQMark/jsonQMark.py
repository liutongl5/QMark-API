# Qingmang Mark API based on Python
# https://github.com/liutongl5/QMark-API
# Email: liutongl5+QMark@gmail.com

from parseQMarkApi import dictParseQMark
import json

def jsonQMark(userId=1, userSecret="", hideSecret=False):
	dictQMark = dictParseQMark(userId, userSecret, hideSecret)

	return jsonQMarkDict( dictQMark )

def jsonQMarkDict( dictQMark ):
	strQMarkJson = ""
	
	if ("valid" in dictQMark and dictQMark["valid"] is True):
		strQMarkJson = json.dumps(dictQMark)
	else:
		strQMarkJson = "Error Retrieving XML!"
	
	return strQMarkJson

def main():
	print( jsonQMark(userId=11,userSecret="YourSecret", hideSecret=True) )

if __name__ == '__main__':
	main()
