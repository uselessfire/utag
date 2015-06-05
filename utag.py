#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  This program distributed under Apache 2.0 license.
#  See LICENSE.txt for more details.
#  © UselessFire

# v. 0.7 Beta Public




# фикс ошибки при отсутсвии файла
# настройки
# move label object to left


import sys, os, gtk, shutil, gc

from traceback import format_exc

core = os.path.abspath(__file__)
coreDir = os.path.dirname(core)

sys.path.insert(0, coreDir + '/libs.zip')

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3




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





configFile = '%s/.config/utag.conf' % os.path.expanduser("~")


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


title = u'UTag - %s'


class UtagWindow:
	def __init__(self, files):
		self.files = files
		self.All = len(self.files)
		self.number = int()
		
		self.window = gtk.Window()
		
		self.window.set_title('UTag')
#		self.window.set_border_width(0)
		
		self.window.set_resizable(False)
		
		self.window.connect("delete_event", self.dialog)
		self.window.connect("destroy", gtk.main_quit)
		
		
		fileMenu = gtk.MenuItem(u'Файл')
		menu = gtk.Menu()
		
		openMenu = gtk.MenuItem(u'Открыть')
		openMenu.connect("activate", self.fileOpenDialog)
		openMenu.show()
		menu.append(openMenu)
		
		settingsMenu = gtk.MenuItem(u'Настройки')
		settingsMenu.show()
		menu.append(settingsMenu)
		
		exitMenu = gtk.MenuItem(u'Выход')
		exitMenu.connect("activate", gtk.main_quit)
		exitMenu.show()
		menu.append(exitMenu)
		
		fileMenu.set_submenu(menu)
		fileMenu.show()
		menuBar = gtk.MenuBar()
		menuBar.show()
		menuBar.append(fileMenu)
 		
		
		self.Vbox = gtk.VBox(False, 0)
		self.Vbox.pack_start(menuBar, False, False, 2)
		
		frame = gtk.Frame(u'Информация')
		frame.show()
		self.label = gtk.Label()
		self.label.show()
		self.label.set_justify(gtk.JUSTIFY_LEFT)
		self.label.set_line_wrap(True)
		self.label.set_alignment(0, 0)
		self.label.set_selectable(True)
		self.label.set_text(u'Необходимо открыть файлы.\nЭто можно сделать с помошью меню "Файл" или нажав правой кнопкой на файл и выбрав "Открыть с помощью UTag".')
		frame.add(self.label)
		self.Vbox.add(frame)
		
		# entrances
		
		# artist
		response, self.artist = self.tag_entry(u'Исполнитель')
		self.Vbox.add(response)
		self.artist.connect("activate", self.update_label)
		
		
		# album
		frame = gtk.Frame(u'Альбом')
		frame.show()
		self.Vbox.add(frame)
		
		VBox = gtk.VBox()
		VBox.show()
		frame.add(VBox)
		
		self.asArtist = gtk.CheckButton(u'Как исполнитель')
		self.asArtist.show()
		self.asArtist.connect("toggled", self.as_artist_handler)
		VBox.add(self.asArtist)
		
		self.album = gtk.Entry(max=64)
		self.album.show()
		VBox.add(self.album)
		
#		response, self.album = self.tag_entry(u'Альбом')
#		self.Vbox.add(response)
		
		# title
		response, self.title = self.tag_entry(u'Название')
		self.Vbox.add(response)
		self.title.connect("activate", self.update_label)
		
		
		temp = gtk.Expander(u'Дополнительно')
		temp.show()
		self.Vbox.add(temp)
		
		Vbox = gtk.VBox()
		Vbox.show()
		temp.add(Vbox)
		
		self.deleteAll = gtk.CheckButton(u'Очистить всё')
		self.deleteAll.show()
		Vbox.add(self.deleteAll)
		self.deleteAll.connect("toggled", self.delete_all_handler)
		
		self.expanderBox = gtk.HBox()
		self.expanderBox.show()
		Vbox.add(self.expanderBox)
		
		self.expanderBox1 = gtk.VBox()
		self.expanderBox1.show()
		self.expanderBox.add(self.expanderBox1)
		
		self.expanderBox2 = gtk.VBox()
		self.expanderBox2.show()
		self.expanderBox.add(self.expanderBox2)
		
		self.expanderBox3 = gtk.VBox()
		self.expanderBox3.show()
		self.expanderBox.add(self.expanderBox3)
		
		# date
#		frame = gtk.Frame(u'Год')
#		frame.show()
#		adj = gtk.Adjustment(0.0, 1.0, 2999.0, 1.0, 1.0, 0.0)
#		self.date = gtk.SpinButton(adj, 0, 0)
#		self.date.show()
#		frame.add(self.date)
#		self.expanderBox1.add(frame)
		response, self.date = self.tag_entry(u'Год')
		self.expanderBox1.add(response)
		
		# genre
		response, self.genre = self.tag_entry(u'Жанр')
		self.expanderBox2.add(response)
		
		# tracknumber
#		frame = gtk.Frame(u'Номер трека')
#		frame.show()
#		adj = gtk.Adjustment(0.0, 1.0, 99.0, 1.0, 1.0, 0.0)
#		self.tracknumber = gtk.SpinButton(adj, 0, 0)
#		self.tracknumber.show()
#		frame.add(self.tracknumber)
#		self.expanderBox3.add(frame)
		response, self.tracknumber = self.tag_entry(u'Номер трека')
		self.expanderBox3.add(response)
		
		# website
		response, self.website = self.tag_entry(u'Сайт')
		self.expanderBox1.add(response)
		
		# organization
		response, self.organization = self.tag_entry(u'Организация')
		self.expanderBox2.add(response)
		
		# encodedby
		response, self.encodedby = self.tag_entry(u'Закодировано')
		self.expanderBox3.add(response)
		
		# copyright
		response, self.copyright = self.tag_entry(u'Авторские права')
		self.expanderBox1.add(response)
		
		# discnumber
#		frame = gtk.Frame(u'Номер диска')
#		frame.show()
#		adj = gtk.Adjustment(0.0, 1.0, 99.0, 1.0, 1.0, 0.0)
#		self.discnumber = gtk.SpinButton(adj, 0, 0)
#		self.discnumber.show()
#		frame.add(self.discnumber)
#		self.expanderBox2.add(frame)
		response, self.discnumber = self.tag_entry(u'Номер диска')
		self.expanderBox2.add(response)
		
		# composer
		response, self.composer = self.tag_entry(u'Композитор')
		self.expanderBox3.add(response)
		
		# lyricist
		response, self.lyricist = self.tag_entry(u'Слова')
		self.expanderBox1.add(response)
		
		# bpm
#		frame = gtk.Frame(u'Темп (ударов в минуту)')
#		frame.show()
#		adj = gtk.Adjustment(0.0, 1.0, 9999.0, 0.8, 1.0, 0.0)
#		self.bpm = gtk.SpinButton(adj, 0, 0)
#		self.bpm.show()
#		frame.add(self.bpm)
#		self.expanderBox2.add(frame)
		response, self.bpm = self.tag_entry(u'Темп (ударов в минуту)')
		self.expanderBox2.add(response)
		
		# media
		response, self.media = self.tag_entry(u'Тип')
		self.expanderBox2.add(response)
		
		# length
#		frame = gtk.Frame(u'Длина')
#		frame.show()
#		adj = gtk.Adjustment(0.0, 1.0, 9999.0, 0.8, 1.0, 0.0)
#		self.length = gtk.SpinButton(adj, 0, 0)
#		self.length.show()
#		frame.add(self.length)
#		self.expanderBox1.add(frame)
		response, self.length = self.tag_entry(u'Длина')
		self.expanderBox1.add(response)
		
		
		frame = gtk.Frame(u'Обложка')
		frame.show()
		VBox = gtk.VBox()
		VBox.show()
		frame.add(VBox)
		
		self.deleteAlbumArt = gtk.CheckButton(u'Удалить')
		self.deleteAlbumArt.show()
		VBox.add(self.deleteAlbumArt)
		
		self.albumArtChooser = gtk.FileChooserButton(u'Выберите обложку')
		self.albumArtChooser.set_filter(self.imageFilter)
		self.albumArtChooser.show()
		VBox.add(self.albumArtChooser)
		
		self.expanderBox3.add(frame)
		
		
		self.mainEntrances = {
			'artist':		self.artist,
			'album':		self.album,
			'title':		self.title
		}
		self.additionalEntrances = {
			'date':			self.date,
			'genre':		self.genre,
			'tracknumber':	self.tracknumber,
			'website':		self.website,
			'organization':	self.organization,
			'encodedby': 	self.encodedby,
			'copyright': 	self.copyright,
			'discnumber': 	self.discnumber,
			'composer': 	self.composer,
			'lyricist':		self.lyricist,
			'bpm':			self.bpm,
			'media':		self.media,
			'length':		self.length
		}
		self.entrances = self.mainEntrances.copy()
		self.entrances.update(self.additionalEntrances)
		
		
		self.Hbox = gtk.HBox(True, 0)
		
		
		
		self.delete_and_next_button = gtk.Button(u'Удалить и следующий')
		self.delete_and_next_button.connect('clicked', self.delete_and_next_file)
		self.Hbox.add(self.delete_and_next_button)
		self.delete_and_next_button.show()
		self.delete_and_next_button.unrealize()
		
		self.next_button = gtk.Button(u'Пропустить')
		self.next_button.connect('clicked', self.next_file)
		self.Hbox.add(self.next_button)
		self.next_button.show()
		
		self.save_and_next_button = gtk.Button(u'Сохранить и следующий')
		self.save_and_next_button.connect('clicked', self.save_and_next_file)
		self.save_and_next_button.show()
		self.Hbox.add(self.save_and_next_button)
		
		self.buttons = (self.save_and_next_button, self.next_button, self.delete_and_next_button)
		
		if not self.files:
			for button in (self.save_and_next_button, self.next_button, self.delete_and_next_button):
				button.set_sensitive(False)
		
		
		
		
		
		self.Vbox.show()
		self.window.add(self.Vbox)
		
		self.Vbox.add(self.Hbox)
		self.Hbox.show()
		
		self.window.show()
		

		if self.files: self.next_file()
	
	
	def save_and_next_file(self, widget=None):
		if self.asArtist.get_active():
			self.album.set_text(self.artist.get_text())
		for name, entry in self.entrances.items():
			text = entry.get_text()
			if text and ((not self.deleteAll.get_active()) or name in self.mainEntrances):
				self.mp3[name] = text
			elif name in self.mp3:
				try:
					del self.mp3[name]
				except:
					if self.dialog(title=u'Произошла ошибка', message=u'Произошла ошибка при удалении тега "%s" в файле "%s":\n%s.\nПовторить?' % (name, self.mp3.filename, format_exc())):
						self.next_file()
					else:
						return self.save_and_next_file()
					
		
		try:
			self.mp3.save()
			artFile = self.albumArtChooser.get_filename()
			if self.deleteAlbumArt.get_active():
				self.id3 = MP3(self.mp3.filename, ID3=ID3)
				if u'APIC' in self.id3.tags: del self.id3.tags[u'APIC']
				if u'APIC:' in self.id3.tags: del self.id3.tags[u'APIC:']
				if u'APIC:None' in self.id3.tags: del self.id3.tags[u'APIC:None']
				self.id3.save()
			elif artFile:
				self.id3 = MP3(self.mp3.filename, ID3=ID3)
				self.id3.tags.add(
					APIC(
						encoding=3,
						mime=('image/png' if artFile.endswith('.png') else 'image/jpeg'),
						type=3,
						data=open(artFile).read()
					)
				)
				self.id3.save()
			
		except:
			if self.dialog(title=u'Произошла ошибка', message=u'Произошла ошибка при сохранении файла "%s":\n%s.\nПовторить?' % (self.mp3.filename, format_exc())):
				self.next_file()
			else:
				self.save_and_next_file()
		else:
			print u'Файл "%s" был сохранён' % self.mp3.filename
			
			newName = (u'%s - %s.mp3' % \
				(
					(self.artist.get_text()		if	self.artist.get_text()		else    u'Неизвестно'),
					(self.title.get_text()		if	self.title.get_text()		else    u'Неизвестно')
				)
			)
			
			newDir = ("%s/%s" % (mvDir, (self.artist.get_text() if self.artist.get_text() else u'Неизвестно')) if artistSort else mvDir)
			
			if artistSort and (not os.path.exists(newDir)):
				os.mkdir(newDir)
			
			realPath = os.path.realpath(self.mp3.filename)
			newRealPath = os.path.realpath("%s/%s/%s" % (os.path.split(realPath)[0], newDir, newName))
			
			newDir = os.path.dirname(newRealPath)
			if not os.path.exists(newDir):
				os.makedirs(newDir)
			
			
			if realPath != newRealPath:
				if os.path.exists(newRealPath):
					if not self.dialog(title=u'Конфликт', message=u'Файл "%s" уже существует в папке "%s"\nЗаменить?' % (newName, newDir)):
						os.remove(newRealPath)
						shutil.move(realPath, newRealPath)
						print u'Файл "%s" был перемещён в папку "%s" с названием "%s" с перезаписью' % (self.mp3.filename, newDir, newName)
						self.next_file()
				else:
					shutil.move(realPath, newRealPath)
					print u'Файл "%s" был перемещён в папку "%s" с названием "%s"' % (self.mp3.filename, newDir, newName)
					self.next_file()
			else:
				print u'Файл "%s" был оставлен с текущим именем' % self.mp3.filename
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
			self.albumArtChooser.unselect_all()
			self.update_label()
			self.window.set_title(title % self.mp3.filename)
			print u'Переход к файлу "%s"' % self.mp3.filename
		else:
			gtk.main_quit()



	def update_label(self, widget=None):	
		minutes = self.mp3.info.length / 60
		seconds = self.mp3.info.length % 60
		self.label_text = default_label_text % \
			(
			self.mp3.filename,
			self.number, # номер файла
			self.All, # число всех файлов
			self.mp3.info.length,  # длина в секундах
			minutes,
			completion(minutes), # добавляем окончание для минут
			seconds,
			completion(seconds), # добавляем окончание для секунд
			self.mp3.info.bitrate / 1024,
			'%s'
			)
		self.label.set_text(self.newName())
	
	
	def as_artist_handler(self, button):
		if button.get_active():
			self.album.hide()
		else:
			self.album.show()
	
	
	def delete_all_handler(self, button):
		if button.get_active():
			for entrance in self.additionalEntrances.values():
				entrance.parent.hide()
		else:
			for entrance in self.additionalEntrances.values():
				entrance.parent.show()
	
	
	newName = lambda self, widget=None: self.label_text % \
		(u'%s - %s.mp3' % \
			(
				(self.artist.get_text()		if	self.artist.get_text()	else	u'Неизвестно'),
				(self.title.get_text()		if	self.title.get_text()	else	u'Неизвестно')
			)
		)

#	def update_newName(self, widget=None):
#		self.label.set_text(
#			self.label_text % \
#				(u'%s - %s.mp3' % \
#					(
#						(self.artist.get_text()		if	self.artist.get_text()	else	u'Неизвестно'),
#						(self.title.get_text()		if	self.title.get_text()	else	u'Неизвестно')
#					)
#				)
#		)
#		self.label.set_justify(gtk.JUSTIFY_LEFT)




	def dialog(self, widget=None, event=None, title=u'Уверены?', message=u'Несохранённые изменения будут утеряны!'):
		dialog = gtk.MessageDialog(
			parent=self.window,
			type=gtk.MESSAGE_QUESTION,
			buttons=gtk.BUTTONS_YES_NO,
			message_format=message
		)
		
		dialog.set_title(title)
		
		response = dialog.run()
		dialog.destroy()
		
		return not response == gtk.RESPONSE_YES
	
	
	def fileOpenDialog(self, a, b=None):
		dialog = gtk.FileChooserDialog(title=u'Открыть', parent=self.window, action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		dialog.set_select_multiple(True)
		dialog.set_filter(self.mp3Filter)
		if dialog.run() == gtk.RESPONSE_OK:
			newFiles = dialog.get_filenames()
			firstFile = not bool(self.files)
			self.files += newFiles
			self.All += len(newFiles)
			if firstFile:
				self.next_file()
				for button in self.buttons:
					button.set_sensitive(True)
			else:
				self.update_label()
			
		dialog.destroy()
	
	
	imageFilter = gtk.FileFilter()
	imageFilter.add_mime_type('image/jpeg')
	imageFilter.add_mime_type('image/png')
	
	mp3Filter = gtk.FileFilter()
	mp3Filter.add_mime_type('audio/mpeg')
	


def completion(number):
	number = int(number)
	if number > 10:
		if number <= 20:
			return unicode()
		else:
			number %= 10
	if number == 1:
		return u'а'
	elif number in (2, 3, 4):
		return u'ы'
	else:
		return unicode()



def main():
	sys.argv = sys.argv[1:]
	if sys.argv and (sys.argv[0] in ('--help', 'help', '-h')):
		print(Help)
	else:
		if not os.path.exists(mvDir):
			os.makedirs(mvDir)
		mp3files = list()
		for x in sys.argv:
			if (not os.path.isdir(x)) and x.lower().endswith('mp3'):
				mp3files.append(x)
			else:
				print(u'Невозможно открыть файл "%s": это не MP3 файл' % x)
#		os.chdir(os.path.split(os.path.abspath(mp3files[0]))[0])
		UtagWindow(mp3files)
		gtk.main()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(1)
	else:
		sys.exit(0)
