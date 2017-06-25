import json
import requests
from PIL import Image, ImageFont, ImageDraw
import urllib
import os
import time
import schedule
import subprocess

def get_photo():
	
	tag = "cars"

	url = "https://www.instagram.com/explore/tags/"+tag+"/?__a=1"#json response url

	page = requests.get(url)

	binary = page.content

	output = json.loads(binary)

	nodes = (output['tag']['media']['nodes'])

	for post in nodes:
		img_url = post['display_src']
		final_img_url = img_url[len(img_url)-15:len(img_url)]
		data = requests.get(img_url)
		img_binary = data.content
		code = post['code']#code that will allow to reach username
		to_username = requests.get("http://www.instagram.com/p/"+code+"/?__a=1")#url that gives access to username
		user_binary = to_username.content
		user_output = json.loads(user_binary)
		username = user_output['graphql']['shortcode_media']['owner']['username']
		file_name = (final_img_url+".jpg")
		if not os.path.exists(file_name):
			with open(file_name,'wb') as file:
				file.write(img_binary)
				print(final_img_url+"Downloaded!")
			blank_canvas = Image.new('RGBA', (500,750),'white')
			to_frame = Image.open(file_name)
			resized = to_frame.resize((480,450))
			logo = Image.open('logo.png')
			logo_resized = logo.resize((425/3, 425/3))
			blank_canvas.paste(resized,(10,45))
			blank_canvas.paste(logo_resized,(180,580))
			font = ImageFont.truetype("/home/danilo/Desktop/insta/Montserrat-Regular.ttf",45)
			text_font = ImageFont.truetype("/home/danilo/Desktop/insta/Montserrat-Regular.ttf",20)
			date_text_font = ImageFont.truetype("/home/danilo/Desktop/insta/Montserrat-Regular.ttf",15)
			BLUE = 11,68,124
			ImageDraw.Draw(blank_canvas).text((95,500),'#'+tag,'black',font=font)
			ImageDraw.Draw(blank_canvas).text((10,18),username,fill=BLUE,font=text_font)
			ImageDraw.Draw(blank_canvas).text((400,24),time.strftime("%d/%m/%Y"),fill='black',font=date_text_font)
			final_name = file_name+".png"
			blank_canvas.save(final_name)
		

get_photo()




schedule.every(1).minutes.do(get_photo)

while 1:
	schedule.run_pending()
	time.sleep(1)
	