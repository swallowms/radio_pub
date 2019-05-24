import os
import pydub
import shutil
import datetime
from system.defs import *
from system.upload import *

base_dir = '/Users/develop/radio2/'

def dir_r(i):
    global base_dir
    return base_dir + i

if os.path.exists('radio.mp3'):
    os.remove('radio.mp3')

#テンポラリー作成
if not os.path.exists('.tmp'):
    os.mkdir('.tmp')
else:
    shutil.rmtree('.tmp')
    os.mkdir('.tmp')

#テンポラリディレクトリに移動
os.chdir('.tmp')

sounds_data = []
dt = datetime.datetime.now()
now_time = str(dt.year) + '年' + str(dt.month) + '月' + str(dt.day) + '日' + str(dt.hour) + '時' + 'になりました！'
say_str = ['おはようございます。', now_time, 'AIラジオのお時間です。', 'このラジオはハリボテ研究所。けいせいさんの音楽でお送りします。']
sounds_data.append(make_snd([dir_r('music/op/1.mp3')], say_str, base_dir))

# ニュースの取得系は自作してください
news_str = make_news('')

in_news = []
for i, k in news_str.items():
    in_news.append(i+'。'+k)

sounds_data.append(make_snd([dir_r('music/news/1.mp3'), dir_r('music/news/2.mp3')], in_news, base_dir))
weather = make_weather('130010')
in_weather = ['本日の気象情報です。', weather['today'], '週間天気予報です。']
for i in weather['week']:
    in_weather.append(i)

sounds_data.append(make_snd([dir_r('music/weather/1.mp3'), dir_r('music/weather/2.mp3')], in_weather, base_dir))

in_ending = ['以上で' + str(dt.year) + '年' + str(dt.month) + '月' + str(dt.day) + '日' + str(dt.hour) + '時'+'のAIラジオは終了です。', 'この番組はハリボテ研究所。けいせいさんの音楽でお送りしました。']
sounds_data.append(make_snd([dir_r('music/ed/afternoon.mp3')], in_ending, base_dir))

sounds = pydub.AudioSegment.empty()

for i in sounds_data:
    sounds += pydub.AudioSegment.from_file(i, format="mp3")

sounds.export("../radio.mp3", format="mp3")

#テンポラリー削除
os.chdir('../')
shutil.rmtree('.tmp')

stream_it('playlist.txt', 'radio')


