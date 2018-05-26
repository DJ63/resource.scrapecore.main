# -*- coding: utf-8 -*-

'''*
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
*'''

from commoncore import kodi
from scrapecore.scrapers.common import DirectScraper, QUALITY
try: 
	from mastercontrol import api as master_control
except: pass

class master_controlScraper(DirectScraper):
	service='master_control'
	name='Master Control'
	
	settings_definition = [
		'<setting label="Master Control" type="lsep" />',
		'<setting default="false" id="master_control_enable" type="bool" label="Enable Master Control" visible="System.HasAddon(master.control)" enabled="System.HasAddon(master.control)" />',
		'<setting label="Requires Master Control to be enabled" type="text" enable="false" visible="!System.HasAddon(master.control)" />'
	]
	
	def search_shows(self, args):
		results = []
		files = master_control.search_files('tvshow', args['trakt_id'], title=args['title'], season=args['season'], episode=args['episode'], match_title=True)
		for f in files['files']:
			result = {"title": f['filename'], "raw_url": master_control.get_cached_url(f['hashid']), "service": self.service, "host": '', "size": f['size'], "extension": self.get_file_type(f['filename']), "quality": QUALITY.LOCAL}
			results.append(result)
		results = self.verify_results(self.process_results, results)
		return results
	
	def search_movies(self, args):
		results = []
		files = master_control.search_files('movie', args['trakt_id'], year=args['year'], match_title=True)
		for f in files['files']:
			result = {"title": f['filename'], "raw_url": master_control.get_cached_url(f['hashid']), "service": self.service, "host": '', "size": f['size'], "extension": self.get_file_type(f['filename']), "quality": QUALITY.LOCAL}
			results.append(result)
		results = self.verify_results(self.process_results, results)
		return results
		
