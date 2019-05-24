#coding: utf-8
import subprocess
import pydub
from datetime import datetime

def jtalk(t, name, base_dir='.'):
	open_jtalk=['open_jtalk']
	mech=['-x',base_dir + '/dic']
	#htsvoice=['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
	htsvoice=['-m',base_dir+'/voices/mei/mei_normal.htsvoice']
	speed=['-r','1.0']
	outwav=['-ow',name + '.wav']
	cmd=open_jtalk+mech+htsvoice+speed+outwav
	t = t.encode()
	c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
	c.stdin.write(t)
	c.stdin.close()
	c.wait()
	# sound = pydub.AudioSegment.from_wav("open_jtalk.wav")
	# sound.export(name+".mp3", format="mp3") 
	# aplay = ['aplay','-q','open_jtalk.wav']
	# wr = subprocess.Popen(aplay)

def say_datetime():
	d = datetime.now()
	text = '%s月%s日、%s時%s分%s秒' % (d.month, d.day, d.hour, d.minute, d.second)
	jtalk(text)
	aplay = ['aplay','-q','open_jtalk.wav']
	wr = subprocess.Popen(aplay)

if __name__ == '__main__':
	say_datetime()
