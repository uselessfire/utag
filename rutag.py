#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#


# Russian version of UTag

#  This program distributed under Apache 2.0 license.
#  See LICENSE.txt for more details.
#  © UselessFire


mvDir = u'tagged'


Help = u'''UTag - изменение тегов mp3 файлов

Использование:
--help | -h | help - эта справка

UTag <имена файлов> - изменить теги этих файлов
'''


Edit = u'''\nЧто вы хотите изменить?
1 - Артист
2 - Альбом
3 - Название трека
4 - Год
5 - Жанр (будьте осторожны)
6 - Номер трека


7 - удалить файл
8 - пропустить
0 - сохранить файл, переименовать его и перейти к следующему

Для удаления тега начните его изменять и оставьте пустым
'''

items = {
	1: 'artist',
	2: 'album',
	3: 'title',
	4: 'date',
	5: 'genre',
	6: 'tracknumber'
	}




import sys, os, gc, shutil
gc.enable()

try:
	reload(sys).setdefaultencoding('utf8')
except:
	print(u'Ошибка при установке стандартной кодировки')



core = os.path.abspath(__file__)
coreDir = os.path.split(core)[0]

sys.path.insert(0, coreDir + '/libs')

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3




def isNumber(text):
	try:
		int(text)
	except:
		return False
	else:
		return True


def edit(ftag, number, All):
	print os.popen('clear').read()
	printItems(ftag, number, All)
	print(Edit)
	inp = raw_input().strip()
	if inp in ('0', '7', '8'):
		return inp
	elif (isNumber(inp)) and (int(inp) in range(1, 7)):
		sys.stdout.write('\nВведите:  ')
		x = unicode(raw_input()).strip()
		if x:
			ftag[items[int(inp)]] = x
		else:
			del ftag[items[int(inp)]]
		return edit(ftag, number, All)
	else:
		print('\nНеправильная команда, повторите ввод\n')
		return edit(ftag, number, All)


def printItems(ftag, number, All):
	print(u'Название файла: %s  (%i/%i)' % (ftag.filename, number, All))
	newName = u'%s - %s.mp3' % (
		(ftag['artist'][0] if 'artist' in ftag else u'Неизвестно'),
		(ftag['title'][0] if 'title' in ftag else u'Нет имени')
		)
	print(u'Файл будет переименован в %s\n\n' % newName)
	for x, y in ftag.items():
		if x == 'artist':
			print(u'Артист: %s' % y[0])
		elif x == 'album':
			print(u'Альбом: %s' % y[0])
		elif x == 'title':
			print(u'Название трека: %s' % y[0])
		elif x == 'date':
			print(u'Год: %s' % y[0])
		elif x == 'genre':
			print(u'Жанр: %s' % y[0])
		elif x == 'tracknumber':
			print(u'Номер трека: %s' % y[0])


def tag(File, number, All):
	ftag = MP3(File, ID3=EasyID3)
	ret = edit(ftag, number, All)
	if ret == '0':
		ftag.save()
		newName = u'%s - %s.mp3' % (
			(ftag['artist'][0] if 'artist' in ftag else u'Неизвестно'),
			(ftag['title'][0] if 'title' in ftag else u'Неизвестно')
			)
		if os.path.exists("%s/%s" % (mvDir, newName)):
			print(u'Файл "%s" в папке "%s" уже существует. Заменить? (y/n)' % (newName, mvDir))
			if raw_input().strip() == 'y':
				os.remove("%s/%s" % (mvDir, newName))
				shutil.move(File, mvDir)
				os.rename("%s/%s" % (mvDir, File), "%s/%s" % (mvDir, newName))
			else:
				tag(File, number, All)
		else:
			shutil.move(File, mvDir)
			os.rename("%s/%s" % (mvDir, File), "%s/%s" % (mvDir, newName))
	elif ret == '7':
		os.remove(File)



def main():
	sys.argv = sys.argv[1:]
	if sys.argv and (sys.argv[0] in ('--help', 'help', '-h')):
		print(Help)
	else:
		if not os.path.exists(mvDir):
			os.makedirs(mvDir)
		number = int()
		files = (sys.argv if sys.argv else os.listdir(chr(46)))
		mp3files = list()
		for x in files:
			if (not os.path.isdir(x)) and x.endswith('mp3'):
				mp3files.append(x)
			else:
				print(u'Невозможно открыть файл "%s": это не MP3 файл' % x)
		if mp3files:
			for x in mp3files:
				number += 1
#				try:
				tag(x, number, len(mp3files))
#				except IOError:
#					print(u'Невозможно открыть файл "%s"' % x)
#					mp3files.remove(x)
		else:
			print(u'\n\nНе указано файлов')




if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit()
