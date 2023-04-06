  
import json
from controller.S3Controller import S3Controller
  
# Opening JSON file
f = open('a1.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
# print(data)
# Iterating through the json
# list
S3Controller.create_bucket("song-image",None)

# for i in data['songs']:
#     print(i['title'])
#     S3Controller.upload_file(i['img_url'],'song_image',i['title'])
  
# Closing file
f.close()