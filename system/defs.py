import os
import re
import uuid
import json
import pydub
import urllib
import xmltodict
import requests
from bs4 import BeautifulSoup
from .jtalk import jtalk

def make_snd(bgm_dir=[], say_str=[], base_dir=''):
	base_sound = pydub.AudioSegment.empty()
	for i in bgm_dir:
		base_sound += pydub.AudioSegment.from_file(i, format='mp3').fade_in(3000)

	say_sounds = pydub.AudioSegment.empty()
	cnt = 0
	for i in say_str:
		uuid_filename = str(uuid.uuid4())
		if base_dir != '':
			jtalk(i, uuid_filename, base_dir)
		else:
			jtalk(i, uuid_filename)
		say_sounds += pydub.AudioSegment.from_file(uuid_filename+'.wav', format='wav')
		if cnt != len(say_str)-1:
			say_sounds += pydub.AudioSegment.silent(duration=500)

		cnt = cnt + 1

	snd_back1 = base_sound[:13*1000]
	base_sound = base_sound[10*1000:]
	ratio = 0.4
	say_sounds = say_sounds + 11
	base_sound = base_sound + pydub.utils.ratio_to_db(ratio)
	base_sound = base_sound.overlay(say_sounds, 3000)
	str_num = say_sounds.duration_seconds
	# op = op_back1.fade_out(3000) + base_sound
	all_snd = snd_back1.append(base_sound, crossfade=3000)
	all_snd = all_snd[:(13 + str_num + 15)*1000].fade_out(3000)
	uuid_f = str(uuid.uuid4()) + '.mp3'
	all_snd.export(uuid_f, format='mp3')

	return(uuid_f)

def make_news(url=''):
	return ('')

def make_weather(code=''):
	if code == '':
		return False;

	url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=' + code
	r = requests.get(url)
	data = json.loads(r.text)
	description = data['description']['text'].replace('\n', '')

	url = 'http://weather.livedoor.com/forecast/rss/area/' + code + '.xml'
	req = urllib.request.Request(url)

	with urllib.request.urlopen(req) as response:
		XmlData = response.read()
	root = xmltodict.parse(XmlData)

	cnt = 0
	week = []
	for i in root['rss']['channel']['item'][1:]:
		week.append(i['description'])
	return({'today': description, 'week': week})

