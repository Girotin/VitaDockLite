import os
import time
import subprocess
from os import path
import NekoMimi as nm
import multiprocessing as mp

banner = nm.figlet('VDock Lite','small')
print(banner)

def load():
	pwd = subprocess.getoutput('pwd')
	home = subprocess.getoutput('echo $HOME')
	run = subprocess.getoutput('mkdir ~/.config/VDockLite/')
	config = f'{home}/.config/VDockLite/options.conf'
	if path.exists(config):
		print("\u001b[34mLoading from config file...\u001b[0m")
		base = nm.ReadFromFile(config)
		lines = base.split("\n")
		for a in lines:
			if a.startswith('theme'):
				theme = a.split(' ')[1]
			if a.startswith('fullscreen'):
				try:
					fs = int(a.split(' ')[1])
				except:
					fs = 0
		return theme, fs
	else:
		print("\u001b[31mNo config found, using default values\u001b[0m")
		run = subprocess.getoutput(f'cp {pwd}/options.conf {config}')
		theme = 'default'
		fs = 0
		return theme, fs

theme, fs = load()

def BGM(theme=theme):
	pwd = subprocess.getoutput('pwd')
	bgm = pwd + f"/theme/{theme}/bgm*"
	construct = f"mpv {bgm} --no-audio-display --loop &"
	try:
		os.remove('run.py')
	except:
		pass
	nm.writeToFile(construct,'run.sh')
	run = subprocess.Popen(['bash',f'{pwd}/run.sh'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	stdout,stderr=run.communicate()
	return

def loop(theme,fs):
	b = mp.Process(target = BGM)
	wallpaperEngine = "xwallpaper --zoom "
	pwd = subprocess.getoutput('pwd')
	home = subprocess.getoutput('echo $HOME')
	connect = pwd + f"/theme/{theme}/connect.*"
	connected = pwd + f"/theme/{theme}/connected.*"
	bgm = pwd + f"/theme/{theme}/bgm.*"
	fullscreenC = ['','--fullscreen']
	fullscreen = fullscreenC[fs]
	b.start()
	run = subprocess.getoutput(f"{wallpaperEngine}{connect}")
	safe = 0

	while True:
		#sudo apt install v4l-utils
		devices = subprocess.getoutput('v4l2-ctl --list-devices')
		entry = devices.split("\n")
		x = 0
		for line in entry:
			x = x + 1
			if line.startswith("PSVita"):
				safe = 1
				run = subprocess.getoutput(f"pkill mpv")
				print("\u001b[32mVita Plugged in!\u001b[0m")
				vdev = f"/dev/video{entry[x][-1]}"
				print(f"\u001b[33mVita on>\u001b[0m {vdev}")
				print("\n")
				run = subprocess.getoutput(f"{wallpaperEngine}{connected}")
				run = subprocess.getoutput(f'mpv av://v4l2:{vdev} --profile=low-latency --untimed {fullscreen}')
			else:
				run = subprocess.getoutput(f"{wallpaperEngine}{connect}")
				if safe == 1:
					b.terminate()
					b = ''
					b = mp.Process(target = BGM)
					b.start()
					safe = 0
		time.sleep(1)


# main = mp.Process(target = loop)
# main.start()
if __name__ == '__main__':
	loop(theme,fs)
