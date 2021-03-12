
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
	# 		[3] Creation time of Issuecomment # ${{ github.event.comment.created_at }}

	strIssueCommentTime = argv[3]
	strIssueCommentUrl = argv[2]+"?since="+strIssueCommentTime
	headers = { \
		"Accept": "application/vnd.github.v3+json", \
		"Authorization": f"token {argv[1]}" \
	}

	req = urllib.request.Request(strIssueCommentUrl, headers=headers) 
	with urllib.request.urlopen(req, context=ssl.SSLContext()) as response:
		strResponse = response.read().decode('UTF-8')
		# print(strResponse) # debug
		jsonResponse = json.loads(strResponse)
		for issuecomment in jsonResponse:
			if (issuecomment["user"]["login"].startswith("github")) :
				print( issuecomment["url"] )
				delReq = urllib.request.Request(issuecomment["url"], headers=headers, method='DELETE') 
				with urllib.request.urlopen(delReq, context=ssl.SSLContext()) as delResponse:
					strResponse = delResponse.read().decode('UTF-8')
					print(strResponse) # debug
				break

def main():
	if len(sys.argv) < 4:
		print("Not enough argv. At least 3 arguments required.")
		return -1
	else:
		PostIssueComment(sys.argv)

	return 0

if __name__ == '__main__':
	main()
