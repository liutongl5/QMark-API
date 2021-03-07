
import ssl, urllib.request
import json

import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "pyQMark"))
from parseQMarkApi import dictParseQMark
from htmlQMark import htmlQMarkDict
from jsonQMark import jsonQMarkDict

def ReadIssueComment(argv):

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

	dictParseOption = json.loads(argv[3])
	strIssueCommentUrl = argv[2]
	headers = { \
		"Accept": "application/vnd.github.v3+json", \
		"Authorization": f"token {argv[1]}" \
	}
	data= {"body": ""}

	if ("userId" in dictParseOption) :
		dictDataBody = {}

		try:
			dictDataBody["userId"] = int(dictParseOption["userId"])
		except:
			return -1
		strUserSecret = ""
		if ("userSecret" in dictParseOption):
			strUserSecret = dictParseOption["userSecret"]
		boolHideSecret = True
		if ( ("hideSecret" in dictParseOption) and (dictParseOption["hideSecret"] == "False") ):
			boolHideSecret = False
		dictQMark = dictParseQMark(dictDataBody["userId"], strUserSecret, boolHideSecret)

		if ( ("html" in dictParseOption) and (dictParseOption["html"] == "True") ):
			dictDataBody["html"] = htmlQMarkDict( dictQMark )
			# print(dictDataBody["html"]) # debug
			if ( ("json" in dictParseOption) and (dictParseOption["json"] == "True") ):
				dictDataBody["json"] = jsonQMarkDict( dictQMark )
		else:
			dictDataBody["json"] = jsonQMarkDict( dictQMark )

		data["body"] = json.dumps(dictDataBody).encode('utf-8')
		# print( data["body"] ) # debug

		req = urllib.request.Request(strIssueCommentUrl, data=json.dumps(data).encode('utf-8'), headers=headers) 
		with urllib.request.urlopen(req, context=ssl.SSLContext()) as response:
			strQMarkXml = response.read().decode('UTF-8')
			print(strQMarkXml) # debug

def main():
	if len(sys.argv) < 4:
		print("Not enough argv. At least 3 arguments required.")
		return -1
	else:
		ReadIssueComment(sys.argv)

	return 0

if __name__ == '__main__':
	main()
