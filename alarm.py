# https://qiita.com/RyosukeKamei/items/d3b787896a07943b3932
# GPIOを制御するライブラリ
import wiringpi
# タイマーのライブラリ
import time

# APIのリクエストに必要
import requests
import json

# 音楽再生用
import subprocess

# APIのURL
apiUrl = "https://kazuki-alarm-65535.herokuapp.com/alarm"

# ボタンを繋いだGPIOの端子番号
button_pin = 17 # 11番端子

# GPIO初期化
wiringpi.wiringPiSetupGpio()
# GPIOを出力モード（1）に設定
wiringpi.pinMode( button_pin, 0 )
# 端子に何も接続されていない場合の状態を設定
# 3.3Vの場合には「2」（プルアップ）
# 0Vの場合は「1」と設定する（プルダウン）
wiringpi.pullUpDnControl( button_pin, 2 )

# アラーム用
alarm = False

first = True

# whileの処理は字下げをするとループの範囲になる（らしい）
while True:
	# print(first)

    # GPIO端子の状態を読み込む
	# ボタンを押すと「0」、放すと「1」になる
	# GPIOの状態が0V(0)であるか比較
	if( wiringpi.digitalRead(button_pin) == 0 ):
		# 0V(0)の場合に表示
		# print ("Switch ON")
		# 初回呼び出し時はアラームを有効化する
		if(first):
			res = requests.get(apiUrl + '/set')
			data = json.loads(res.text)
			assert data["res"] == "success"
			first = False

		# cnt += 1
		
		
		# アラーム機能が有効
		# リクエスト送信を行って結果の取得をする
		res = requests.get(apiUrl)
		# 結果はJSON形式
		data = json.loads(res.text)
		# 結果をコンソールに出力
		# print("設定時刻: ", data["set"])
		# print("現在時刻: ", data["now"])
		# print("アラーム: ", data["alarm"])

		if(data["alarm"] == "true"):
			# print("鳴ったよ")
			subprocess.run(['aplay', 'mezamashi_voice.wav'])



	else:
		if(first == False):
			first = True
			# print("無効化しました")
			# アラームを無効化する
			data = {"msg":"goodMng_stopPlz"}
			res = requests.post(apiUrl + '/stop', data=data)
			data = json.loads(res.text)
			# print(data["res"])
			# 次回呼ばれたときに有効化するためにfirstをTrueにする
		# else:
			# print("無効化してるよ！")

		# 3.3V(1)の場合に表示
		# print ("Switch OFF")
	
	time.sleep(1)