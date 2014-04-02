""" 
 @file
 @brief This file loads the current language based on the computer's locale settings
 @author Noah Figg <eggmunkee@hotmail.com>
 @author Jonathan Thomas <jonathan@openshot.org>
 
 @section LICENSE
 
 Copyright (c) 2008-2014 OpenShot Studios, LLC
 (http://www.openshotstudios.com). This file is part of
 OpenShot Video Editor (http://www.openshot.org), an open-source project
 dedicated to delivering high quality video editing and animation solutions
 to the world.
 
 OpenShot Video Editor is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 OpenShot Video Editor is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with OpenShot Library.  If not, see <http://www.gnu.org/licenses/>.
 """

import os
from PyQt5.QtCore import QLocale, QLibraryInfo, QTranslator, QCoreApplication
from classes.logger import log
from classes import info

def init_language():
	""" Find the current locale, and install the correct translators """
	
	# Get app instance
	app = QCoreApplication.instance()

	# Setup of our list of translators and paths
	translator_types = (
		{"type":'QT',
		 "pattern":'qt_%s',
		 "path":QLibraryInfo.location(QLibraryInfo.TranslationsPath)},
		{"type":'OpenShot',
		 "pattern":os.path.join('%s','LC_MESSAGES','OpenShot'),
		 "path":os.path.join(info.PATH, 'locale')},
		 )
	
	# Determine the environment locale, or default to system locale name
	locale_names = [ os.environ.get('LANG', QLocale().system().name()),
					 os.environ.get('LOCALE', QLocale().system().name()) 
				   ]
	
	# Output all system languages detected
	log.info("Qt Detected Languages: {}".format(QLocale().system().uiLanguages()))
	log.info("LANG Environment Variable: {}".format(os.environ.get('LANG', QLocale().system().name())))
	log.info("LOCALE Environment Variable: {}".format(os.environ.get('LOCALE', QLocale().system().name())))
	
	# Loop through environment variables
	found_language = False
	for locale_name in locale_names:
	
		# Don't try on default locale, since it fails to load what is the default language
		if 'en_US' in locale_name:
			log.info("Skipping English language (no need for translation): {}".format(locale_name))
			continue
	
		# Go through each translator and try to add for current locale
		for type in translator_types:
			trans = QTranslator(app)
			if find_language_match(type["pattern"], type["path"], trans, locale_name):
				# Install translation
				app.installTranslator(trans)
				found_language = True
				
		# Exit if found language
		if found_language:
			log.info("Exiting translation system (since we successfully loaded: {})".format(locale_name))
			break
				

# Try the full locale and base locale trying to find a valid path
#  returns True when a match was found.
#  pattern - a string expected to have one pipe to be filled by locale strings
#  path - base path for file (pattern may contain more path)
#  
def find_language_match(pattern, path, translator, locale_name):
	""" Match all combinations of locale, language, and country """
	
	success = False
	locale_parts = locale_name.split('_')
	
	i = len(locale_parts)
	while not success and i > 0:
		formatted_name = pattern % "_".join(locale_parts[:i])
		log.info('Attempting to load {} in \'{}\''.format(formatted_name, path))
		success = translator.load(formatted_name, path)
		if success:
			log.info('Successfully loaded {} in \'{}\''.format(formatted_name, path))
		i -= 1
		
	return success
	
