import logging
import json
from controller.S3Controller import S3Controller
from controller.MusicController import MusicController
from controller.UserController import UserController
from controller.SubController import SubController


items = MusicController.get_all_item()

S3Controller.create_bucket("song-image")
for item in items:
    S3Controller.upload_file(item['img_url'],"song-image",item['title'])

