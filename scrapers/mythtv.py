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
from commoncore import mythtv
from scrapecore.scrapers.common import DirectScraper, QUALITY

class mythtvScraper(DirectScraper):
	valid = kodi.get_condition_visiblity("System.HasAddon(pvr.mythtv)")
	service='mythtv'
	name='MythTV'

	settings_definition = [
		'<setting label="MythTV" type="lsep" />',
		'<setting default="false" id="mythtv_enable" type="bool" label="Enable MythTV" visible="System.HasAddon(pvr.mythtv)" enabled="System.HasAddon(pvr.mythtv)" />',
		'<setting label="Requires PVR.MythTV to be enabled" type="text" enable="false" visible="!System.HasAddon(pvr.mythtv)" />',
	]
	
	def search_shows(self, args):
		results = []
		result = mythtv.search_episodes(args['title'], args['season'], args['episode'])
		if result:
			media = {
				"title": "%s %sx%s" % (args['title'], args['season'], args['episode']),
				"host": self.name,
				"host_icon": '',
				"raw_url": result['url'],
				"service": self.service,
				"size": result['size'],
				"quality": QUALITY.LOCAL,
				"extension": result['extension']
				}
			results.append(media)
				
		results = self.verify_results(self.process_results, results)
		return results
	
	def search_movies(self, args):
		results = []
		result = mythtv.search_movies(args['title'], args['year'])
		if result:
			media = {
				"title": "%s (%s)" % (args['title'], args['year']),
				"host": self.name,
				"host_icon": '',
				"raw_url": result['url'],
				"service": self.service,
				"size": result['size'],
				"quality": QUALITY.LOCAL,
				"extension": result['extension']
			}
			results.append(media)
		
		results = self.verify_results(self.process_results, results)
		return results

		
