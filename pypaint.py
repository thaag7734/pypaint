from os import system, getcwd
from msvcrt import kbhit, getch
import re
import json

filters = [
	re.compile('^\.+$'),
	re.compile('^.*[<>:"/\\|?*].*$')
]

cancel = re.compile('^[cC][aA][nN][cC][eE][lL]$')

canvas = [['┌','─','─','─','─','─','─','─','─','─','─','─','─','─','─','─','─','─','─','─','─','┐']]
for i in range(0,20):
	canvas.append(['│',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','│'])
canvas.append(['└','─','─','─','─','─','─','─','─','─','─','─','─','─','─','─','─','─','─','─','─','┘'])

cursor = {
	'x': 1,
	'y': 1,
	'icon': '\\',
	'iconPainted': '▀'
}

def saveCanvas(canvas, invalid=False):
	system('mode con: cols=50 lines=28')
	system('cls')
	if invalid:
		print('Invalid filename!')
	name = input('Name to save file as (type cancel to go back):\n> ')
	if name == '':
		saveCanvas(canvas, True)
	elif re.match(cancel, name):
		return paint(canvas, True)
	for _filter in filters:
		if re.match(_filter, name):
			saveCanvas(canvas, True)
	json.dump({'canvas': canvas}, open(f'{name}.pypnt', 'w+'))
	input(f'Canvas saved as "{getcwd()}\\{name}.pypnt".\nPress Enter to return to PyPaint...\n')
	return paint(canvas, True)

def loadCanvas(canvas, nonexist=False):
	system('mode con: cols=50 lines=28')
	system('cls')
	if nonexist:
		print('Error loading file!')
	path = input('Path to file (type cancel to go back):\n> ')
	if path == '':
		loadCanvas(canvas, True)
	elif re.match(cancel, path):
		return paint(canvas, True)
	if not path.endswith('.pypnt'):
		path += '.pypnt'
	try:
		canvobj = json.load(open(f'{path}', 'r'))
	except FileNotFoundError:
		loadCanvas(canvas, True)
	return paint(canvobj['canvas'], True)

def paint(canvas, firstRun):
	system('mode con: cols=23 lines=28')
	while True:
		if firstRun:
			screenUpdate = True
			firstRun = False
		else:
			screenUpdate = False
		c = kbhit()
		if c:
			ch = ord(getch())
			if ch == 119 and canvas[cursor['y'] - 1][cursor['x']] != '─':
				cursor['y'] -= 1
				screenUpdate = True
			elif ch == 97 and canvas[cursor['y']][cursor['x'] - 1] != '│':
				cursor['x'] -= 1
				screenUpdate = True
			elif ch == 115 and canvas[cursor['y'] + 1][cursor['x']] != '─':
				cursor['y'] += 1
				screenUpdate = True
			elif ch == 100 and canvas[cursor['y']][cursor['x'] + 1] != '│':
				cursor['x'] += 1
				screenUpdate = True
			elif ch == 32:
				if canvas[cursor['y']][cursor['x']] != '█':
					canvas[cursor['y']][cursor['x']] = '█'
				else:
					canvas[cursor['y']][cursor['x']] = ' '
				screenUpdate = True
			elif ch == 13:
				saveCanvas(canvas)
			elif ch == 8:
				loadCanvas(canvas)
			elif ch == 27:
				exit()
		if screenUpdate:
			system('cls')
			for line in range(0, len(canvas)):
				l = ''
				for spot in range(0, len(canvas[line])):
					if cursor['y'] == line and cursor['x'] == spot:
						if canvas[cursor['y']][cursor['x']] == '█':
							l += cursor['iconPainted']
						else:
							l += cursor['icon']
					else:
						l += str(canvas[line][spot])
				print(l)
			print('Move:  WASD')
			print('Paint: [SPACE]')
			print('Save:  [ENTER]')
			print('Load:  [BACKSPACE]')
			print('Exit:  [ESC]')

paint(canvas, True)
