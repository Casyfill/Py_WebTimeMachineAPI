#!/usr/bin/env python

import scraperwiki
import requests, json
import datetime


# chech if closest date is in delta
def inDelta(base,timestamp, delta_days):
    def days_between(base,timestamp):
        d1 = datetime.datetime.strptime(base, "%Y%m%d")
        d2 = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%S")
        return abs((d1-d2).days)
        
    if days_between(base, timestamp) <= delta_days:
        return True
    else:
        return False
    

# gets closest date url
def requestDates(url, timestamp, delta_days=15):
    
	payload = {'url':url, 'timestamp':timestamp}
	result = json.loads(requests.get("http://archive.org/wayback/available?", params = payload).text)
	
	status = False
	
	try:
	    status = result['archived_snapshots']['closest']['available']
	except:
	    pass
	    
	if status:
	    if inDelta(timestamp, str(result['archived_snapshots']['closest']['timestamp']), delta_days):
	        return {'status':'ok', 'url':result['archived_snapshots']['closest']['url'], 'timestamp':result['archived_snapshots']['closest']['timestamp']}
	    else:
	        return {'status':'badDate', 'url':result['archived_snapshots']['closest']['url'], 'timestamp':result['archived_snapshots']['closest']['timestamp'] }
	else: return {'status':'noUrl', 'url':None, 'timestamp':'?' }
    

# links
links = [] # links to request

# saving links for list
unique_keys = [ 'baseLink' ]
for link in links:
    r = requestDates(link, '20140805', delta_days=15)
    r['baseLink']= link
    scraperwiki.sql.save(unique_keys, r)
    print link


