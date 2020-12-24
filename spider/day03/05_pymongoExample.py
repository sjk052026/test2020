import pymongo

conn=pymongo.MongoClient('localhost',27017)

db=conn['studb']
myset=db['stuset']
myset.insert_one({'name':'铁锤','hobby':'study'})
