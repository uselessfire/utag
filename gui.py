#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  This program distributed under Apache 2.0 license.
#  See LICENSE.txt for more details.
#  © UselessFire

# v. 0.3.2 Beta Public


mvDir = "tagged"


import sys, os, gtk, shutil, gc

gc.enable()

from traceback import format_exc

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3



default_label_text = \
u'''Название файла: "%s" (%i/%i)
Длина: %i секунд (%i минут %i секунд)
Битрейт: %i КБ\с
Файл будет переименован в '''



Help = u'''UTag - изменение тегов mp3 файлов

Использование:
--help | -h | help - эта справка

UTag <имена файлов> - изменить теги этих файлов
'''



class utag_window:
	def __init__(self, files):
		self.files = files
		self.All = len(self.files)
		self.number = int()
		
		self.window = gtk.Window()
		
		self.window.set_title('UTag')
#		self.window.set_border_width(0)
		
		self.window.connect("delete_event", self.dialog)
		self.window.connect("destroy", gtk.main_quit)
		
		self.Vbox = gtk.VBox(False, 0)
		
		
		self.labelframe = gtk.Frame(u'Информация')
		self.labelframe.show()
		self.label = gtk.Label()
		self.label.show()
		self.labelframe.add(self.label)
		self.Vbox.add(self.labelframe)
		
		# entrances
		
		# artist
		response, self.artist = self.tag_entry(u'Исполнитель')
		self.Vbox.add(response)
		self.artist.connect("activate", self.update_newName)
		
		
		# album
		response, self.album = self.tag_entry(u'Альбом')
		self.Vbox.add(response)
		
		# title
		response, self.title = self.tag_entry(u'Название')
		self.Vbox.add(response)
		self.title.connect("activate", self.update_newName)
		
		# date
		response, self.date = self.tag_entry(u'Год')
		self.Vbox.add(response)
		
		# genre
		response, self.genre = self.tag_entry(u'Жанр')
		self.Vbox.add(response)
		
		# tracknumber
		response, self.tracknumber = self.tag_entry(u'Номер трека')
		self.Vbox.add(response)
		
		
		self.entrances = {
			'artist': self.artist,
			'album': self.album,
			'title': self.title,
			'date': self.date,
			'genre': self.genre,
			'tracknumber': self.tracknumber
		}
		
		
		self.Hbox = gtk.HBox(False, 0)
		
		
		
		self.delete_and_next_button = gtk.Button(u'Удалить и следующий')
		self.delete_and_next_button.connect('clicked', self.delete_and_next_file)
		self.Hbox.add(self.delete_and_next_button)
		self.delete_and_next_button.show()
		
		self.next_button = gtk.Button(u'Пропустить')
		self.next_button.connect('clicked', self.next_file)
		self.Hbox.add(self.next_button)
		self.next_button.show()
		
		self.save_and_next_button = gtk.Button(u'Сохранить и следующий')
		self.save_and_next_button.connect('clicked', self.save_and_next_file)
		self.save_and_next_button.show()
		self.Hbox.add(self.save_and_next_button)
		
		
		
		
		
		self.Vbox.show()
		self.window.add(self.Vbox)
		
		self.Vbox.add(self.Hbox)
		self.Hbox.show()
		
		self.window.show()
		
		
		self.next_file()
	
	
	
	def save_and_next_file(self, widget=None):
		for name, entry in self.entrances.items():
			text = entry.get_text()
			if text:
				self.mp3[name] = text
			elif name in self.mp3:
				try:
					del self.mp3[name]
				except:
					if self.dialog(title=u'Произошла ошибка', message=u'Произошла ошибка при удалении тега "%s" в файле "%s":\n%s.\nПовторить?' % (name, self.mp3.filename, format_exc())):
						self.next_file()
					else:
						self.save_and_next_file()
					return
		
		try:
			self.mp3.save()
		except:
			if self.dialog(title=u'Произошла ошибка', message=u'Произошла ошибка при сохранении файла "%s":\n%s.\nПовторить?' % (self.mp3.filename, format_exc())):
				self.next_file()
			else:
				self.save_and_next_file()
		else:
			print u'Файл "%s" был сохранён' % self.mp3.filename
			
			newName = (u'%s - %s.mp3' % \
				(
					(self.artist.get_text()	if	self.artist.get_text()	else    u'Неизвестно'),
					(self.title.get_text()		if	self.title.get_text()		else    u'Неизвестно')
				)
			)
			
			if os.path.exists("%s/%s" % (mvDir, newName)):
				if not self.dialog(title=u'Заменить?', message=u'Файл "%s" уже существует в папке "%s"' % (newName, mvDir)):
					os.remove("%s/%s" % (mvDir, newName))
					shutil.move(self.mp3.filename, "%s/%s" % (mvDir, newName))	
					print u'Файл "%s" был перемещён в папку "%s" с названием "%s" с перезаписью' % (self.mp3.filename, mvDir, newName)
					self.next_file()
			else:
				shutil.move(self.mp3.filename, "%s/%s" % (mvDir, newName))	
				print u'Файл "%s" был перемещён в папку "%s" с названием "%s"' % (self.mp3.filename, mvDir, newName)
				self.next_file()
		
		
	
	
	def delete_and_next_file(self, widget=None):
		try:
			os.remove(self.mp3.filename)
		except:
			if self.dialog(title=u'Произошла ошибка', message=u'Произошла ошибка при удалении файла "%s":\n%s.\nПовторить?' % (self.mp3.filename, format_exc())):
				self.next_file()
			else:
				self.delete_and_next_file()
		else:
			print u'Файл "%s" был удалён' % self.mp3.filename
			self.next_file()
	
	
	
	def tag_entry(self, title):
		frame = gtk.Frame(title)
		entry = gtk.Entry(max=64)
		entry.show()
		frame.add(entry)
		frame.show()
		return (frame, entry)
	
	
	
	def next_file(self, widget=None):
		if self.files:
			self.mp3 = MP3(self.files.pop(0), ID3=EasyID3)
			self.number += 1
			for name, entry in self.entrances.items():
				if name in self.mp3.keys():
					entry.set_text(self.mp3[name][0])
				else:
					entry.set_text(str())
			self.update_label()
			print u'Переход к файлу "%s"' % self.mp3.filename
		else:
			gtk.main_quit()



	def update_label(self):
		self.label_text = default_label_text % \
			(
			self.mp3.filename,
			self.number,
			self.All,
			self.mp3.info.length, 
			self.mp3.info.length / 60,
			self.mp3.info.length % 60,
			self.mp3.info.bitrate / 1024
			) + '"%s"'
		self.update_newName()
		
		
	update_newName = lambda self, widget=None: self.label.set_text(
		self.label_text % \
				(u'%s - %s.mp3' % \
					(
						(self.artist.get_text()    if   self.artist.get_text()   else    u'Неизвестно'),
						(self.title.get_text()      if   self.title.get_text()     else    u'Неизвестно')
					)
				)
		)




	def dialog(self, widget=None, event=None, title=u'Уверены?', message=u'Несохранённые изменения будут утеряны!'):
		self.dialog = gtk.MessageDialog(
			parent=self.window,
			type=gtk.MESSAGE_QUESTION,
			buttons=gtk.BUTTONS_YES_NO,
			message_format=message
		)
		
		self.dialog.set_title(title)
		
		response = self.dialog.run()
		self.dialog.destroy()
		
		return not response == gtk.RESPONSE_YES
		
#		if response == gtk.RESPONSE_YES:
#			return False
#		else:
#			return True
		
		



def main():
	sys.argv = sys.argv[1:]
	if sys.argv and (sys.argv[0] in ('--help', 'help', '-h')):
		print(Help)
	else:
		if not os.path.exists(mvDir):
			os.makedirs(mvDir)
		files = (sys.argv if sys.argv else os.listdir(chr(46)))
		mp3files = list()
		for x in files:
			if (not os.path.isdir(x)) and x.endswith('mp3'):
				mp3files.append(x)
			else:
				print(u'Невозможно открыть файл "%s": это не MP3 файл' % x)
		if mp3files:
			os.chdir(os.path.split(os.path.abspath(mp3files[0]))[0])
			utag_window(mp3files)
			gtk.main()
		else:
			print(u'\n\nНе указано файлов')
		



if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit()

