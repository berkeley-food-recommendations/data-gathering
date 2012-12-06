from factual import Factual
from factual_api_keys import KEY, SECRET
import json

factual = Factual(KEY,SECRET)

if __name__ == "__main__":
	limit=50
	maximum=500
	results =[]
	query = factual.table("restaurants").filters({"$and":[{"region":"CA"},{"locality":"berkeley"}]}).include_count(True).limit(str(limit)).offset("0").sort("address:asc")
	tot=query.total_row_count()
	curOffset = limit
	results= results+query.data()
	while(curOffset<min(tot,maximum)):
		query = factual.table("restaurants-us").filters({"$and":[{"region":"CA"},{"locality":"berkeley"}]}).include_count(True).limit(str(limit)).offset(str(curOffset)).sort("address:asc")
		results = results+query.data()
		curOffset=curOffset+limit
	
	# this is to get the rest of the restaurants
	# reverse the query and get the ones we didn't get earlier
	if (tot>maximum):
		curOffset = 0
		nextMax = tot - maximum 
		while(curOffset<nextMax): 
			if ((nextMax-curOffset)<50):
				lim = (nextMax-curOffset) % limit
			else:
				lim = limit
			query = factual.table("restaurants-us").filters({"$and":[{"region":"CA"},{"locality":"berkeley"}]}).include_count(True).limit(str(lim)).offset(str(curOffset)).sort("address:desc")
			results = results + query.data()
			curOffset=curOffset+lim
	#print tot
	#print len(results)
	#print results
	print json.dumps(results)
		
	
