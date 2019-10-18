import requests
from bs4 import BeautifulSoup
import urllib.error

def getjobs():
	url="https://stackoverflow.com/jobs?l=india"
	http=requests.get(url)
	soup=BeautifulSoup(http.text,'lxml')
	jobdetails=soup.findAll(class_="-job-summary")
	string=""
	
	for jobs in jobdetails:
		jobtitle=list(jobs.children)[1].getText().lstrip('\n').rstrip('\n')
		#jobtitle=jobtitle.lstrip("\n");
		jobtitle2=list(jobs.children)[3].getText().lstrip('\n').rstrip('\n')
		#jobdetails=jobdetails.lstrip("\n")
		string+="\n"+"JOB NAME:---"+jobtitle+" COMPANY:-- "+jobtitle2+"\n"
	return string