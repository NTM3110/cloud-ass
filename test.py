import logging
import json
from controller.S3Controller import S3Controller
from controller.MusicController import MusicController
from controller.UserController import UserController
from controller.SubController import SubController

target = "tom"

title = "#40"
name = "tom"
SubController.delete_item(name,title)
subs = SubController.get_all_item()
subs_user = []
for i in subs:
    if i['username'] == name:
        subs_user.append(MusicController.get_item(i['songTitle']))

print(subs_user)
print(name)
