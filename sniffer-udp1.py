import subprocess as sub
import re, requests, sys

#Sniff UDP packets and get ip location
#not really useful, but can be funny if u want to scary people on omegle or similar site

lstglobal = []

def wget_info(strZ) :
	ret = requests.get('http://ipinfo.io/'+strZ).json()
	s = ", "
	try:
		print( strZ + s + ret['org'])
		print( ret['country'] + s + ret['region'] + s + ret['postal'] + s + ret['city'] + s +ret['loc'] )
	except KeyError:
		print(ret)

def add_to_list(strZ) :
	global lstglobal
	global argz
	i = strZ[:str.rfind(strZ, ".")]
	if ( not bool(re.search('[a-zA-Z]+',i)) ):
		try:
			index = lstglobal.index(i)
		except ValueError:
			lstglobal.append(i)
			print ("new address: " + i +" try to discover? y/n(default)")
			yn = sys.stdin.readline()
			if( str.find(yn.upper(), 'Y') >= 0) :
				wget_info(i)

if __name__ == '__main__' :
	p = sub.Popen(('sudo', 'tcpdump','-q','-i','wlo1' ,'-l', 'udp'), stdout=sub.PIPE)
	for row in iter(p.stdout.readline, b''):
		strn = row.rstrip()
		add_to_list( (strn[str.find(strn, ">") + 1 : str.rfind(strn, ":")]).strip() )	
