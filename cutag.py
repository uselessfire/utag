#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#


# Russian version of UTag
# v. 1.0.1 Public

#  This program distributed under Apache 2.0 license.
#  See LICENSE.txt for more details.
#  © UselessFire


import os

def File(confFile, text=None, ini=False):
	if text is None:
		if os.path.exists(confFile):
			noSetFile = open(confFile, 'r')
			text = noSetFile.read()
			noSetFile.close()
			return text.decode('utf8')
		else:
			return File(confFile, str())
	else:
		if ini:
			if os.path.exists(confFile):
				return File(confFile)
			else:
				return File(confFile, text)
		else:
			confFile, text = unicode(confFile), unicode(text)
			folder = os.path.dirname(confFile)
			if folder and not os.path.exists(folder):
				os.makedirs(folder)
			noSetFile = open(confFile, 'w')
			noSetFile.write(text)
			noSetFile.close()
			return text



mvDir = 'tagged'

configFile = '%s/.config/utag' % os.path.expanduser("~")


defaultConfig = \
'''# False - нет
# True - да
mvDir = '.' # каталог, в который будут перемещаться отредактированная музыка
artistSort = True # сортировать артистов по папкам'''

	
exec(File(configFile, defaultConfig, True))


default_label_text = \
u'''Название файла: "%s" (%i/%i)
Длина: %i секунд (%i минут%s %i секунд%s)
Битрейт: %i КБ\с
Файл будет переименован в "%s"'''



Help = u'''UTag - изменение тегов mp3 файлов

Использование:
utag --help | -h | help - эта справка
utag <имена файлов> - изменить теги этих файлов

После сохранения файл будет перемещён в папку "%s" под именем "<исполнитель> - <название>.mp3"''' % mvDir

Edit = u'''\nЧто вы хотите изменить?
1  - Артист
2  - Альбом
3  - Название трека
4  - Год
5  - Жанр
6  - Номер трека
7  - Сайт
8  - организация
9  - кем закодировано
10 - права
11 - номер диска
12 - композитор
13 - слова
14 - темп (ударов в минуту)
15 - тип
16 - длина


- - удалить файл
0 - пропустить
+ - сохранить файл, переименовать его, переместить в папку %s и перейти к следующему

Для удаления тега начните его изменять и оставьте пустым
''' % mvDir

items = {
	1:	'artist',
	2:	'album',
	3:	'title',
	4:	'date',
	5:	'genre',
	6:	'tracknumber',
	7:	'website',
	8:	'organization',
	9:	'encodedby',
	10:	'copyright',
	11:	'discnumber',
	12:	'composer',
	13:	'lyricist',
	14:	'bpm',
	15:	'media',
	16:	'length'
	} #######################добавить в программу№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№




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
	if inp in ('-', '+', '0'):   ############переделать под новые команды
		return inp
	elif (isNumber(inp)) and (int(inp) in range(1, 15)):
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
			print(u'Трека: %s' % y[0])
		
		elif x == 'date':
			print(u'Год: %s' % y[0])
		
		elif x == 'genre':
			print(u'Жанр: %s' % y[0])
		
		elif x == 'tracknumber':
			print(u'Номер трека: %s' % y[0])
		
		elif x == 'website':
			print(u'Сайт: %s' % y[0])
		
		elif x == 'organization':
			print(u'Организация: %s' % y[0])
		
		elif x == 'encodedby':
			print(u'Кем закодировано: %s' % y[0])
		
		elif x == 'copyright':
			print(u'Права: %s' % y[0])
		
		elif x == 'discnumber':
			print(u'Номер диска: %s' % y[0])
		
		elif x == 'composer':
			print(u'Композитор: %s' % y[0])
		
		elif x == 'liricist':
			print(u'Слова: %s' % y[0])
		
		elif x == 'bpm':
			print(u'Темп: %s' % y[0])
		
		elif x == 'media':
			print(u'Тип: %s' % y[0])
		
		elif x == 'length':
			print(u'Длина: %s' % y[0])


def tag(File, number, All):
	ftag = MP3(File, ID3=EasyID3)
	ret = edit(ftag, number, All)
	if ret == '+': # save
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
	elif ret == '-': # remove
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
