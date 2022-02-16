from geoip import geolite2
import time
from geopy.geocoders import Nominatim
def listeToDictionnaire(liste):
	output={}
	output['titre']=liste.titre
	return output

def remplirDonne(ip, user):
	test="126.53.24.5"
	lookup=geolite2.lookup(test)
	#geolocator=Nominatim(user_agent="minimalist")
	#location=geolocator.reverse(str(lookup.location))
	
	donne={'ip':ip, 'user':user, 'nationalite':lookup.country, 'timeZone':lookup.timezone, 'continent':lookup.continent, 'location':'12345'}
	return donne


def getSlug():
	tab=['A', 'B', 'C', 'D', 'E', 'F', 'T', 'X', 'R', 'Q']
	slug=time.time()
	slug=str(slug)
	slug=slug.replace('.', '')
	
	for item in slug:
		item=int(item)
		item=tab[item]
		
	return slug