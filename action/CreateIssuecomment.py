
import ssl, urllib.request
import json

import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "pyQMark"))
from parseQMarkApi import dictParseQMark
from htmlQMark import htmlQMarkDict
from jsonQMark import jsonQMarkDict

def PostIssueComment(argv):

	# argv: input arguments: 
	# 		[1] Admin GithubToken to be used for posting replies of generated results
	# 		[2] Url of IssueComment page # ${{ github.event.issue.url }}
	# 		[3] strParseOption: 
	# 				"userId": QMarkUserId
	# 				"userSecret": "QMarkUserSecret"
	# 				"hideSecret": True/False
	# 				"html": True/False
	# 				"json": True/False
	# 			# [3] should be the message body of issue comment # ${{ github.event.comment.body }}

	dictParseOption = {}
	for strOption in (argv[3].split("&")) :
		arrOption = strOption.split("=")
		if (len(arrOption) == 2) :
			dictParseOption[ arrOption[0].strip() ] = arrOption[1].strip()
	# print( json.dumps(dictParseOption) ) # debug
	strIssueCommentUrl = argv[2]
	headers = { \
		"Accept": "application/vnd.github.v3+json", \
		"Authorization": f"token {argv[1]}" \
	}
	payloadData= {"body": ""}

	if ("userId" in dictParseOption) :
		dictPayloadDataBody = {}

		try:
			dictPayloadDataBody["userId"] = int(dictParseOption["userId"])
		except:
			return -1
		strUserSecret = ""
		if ("userSecret" in dictParseOption):
			strUserSecret = dictParseOption["userSecret"]
		boolHideSecret = True
		if ( ("hideSecret" in dictParseOption) and (dictParseOption["hideSecret"] == "False") ):
			boolHideSecret = False
		dictQMark = dictParseQMark(dictPayloadDataBody["userId"], strUserSecret, boolHideSecret)

		if ( ("html" in dictParseOption) and (dictParseOption["html"] == "True") ):
			dictPayloadDataBody["html"] = htmlQMarkDict( dictQMark )
			# print(dictPayloadDataBody["html"]) # debug
			if ( ("json" in dictParseOption) and (dictParseOption["json"] == "True") ):
				dictPayloadDataBody["json"] = jsonQMarkDict( dictQMark )
		else:
			dictPayloadDataBody["json"] = jsonQMarkDict( dictQMark )

		payloadData["body"] = json.dumps(dictPayloadDataBody)
		# print( json.dumps(payloadData) ) # debug
		# print(strIssueCommentUrl)

		req = urllib.request.Request(strIssueCommentUrl, data=json.dumps(payloadData).encode('utf-8'), headers=headers) 
		with urllib.request.urlopen(req, context=ssl.SSLContext()) as response:
			strQMarkXml = response.read().decode('UTF-8')
			print(strQMarkXml) # debug

def main():
	if len(sys.argv) < 4:
		print("Not enough argv. At least 3 arguments required.")
		return -1
	else:
		PostIssueComment(sys.argv)

	return 0

if __name__ == '__main__':
	main()
