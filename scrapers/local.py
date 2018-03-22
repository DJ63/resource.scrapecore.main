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

import re
import xbmc
import json
from commoncore import kodi
from scrapecore.scrapers.common import DirectScraper, QUALITY

class localScraper(DirectScraper):
	service='local'
	name='VideoLibrary'
	
	def search_shows(self, args):
		results = []
		filter_str = '{{"field": "title", "operator": "contains", "value": "{search_title}"}}'
		filter_str = '{{"and": [%s, {{"field": "year", "operator": "is", "value": "%s"}}]}}' % (filter_str, args['year'])
		cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": { "filter": %s, "limits": { "start" : 0, "end": 25 }, "properties" : ["title", "year"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true } }, "id": "libTvShows"}'
		command = cmd % (filter_str.format(search_title=args['title']))
		response = json.loads(xbmc.executeJSONRPC(command))
		if 'result' in response and 'tvshows' in response['result']:
			for r in response['result']['tvshows']:
				kodi.log(r)
				if str(r['year']) != args['year'] or args['title'] not in r['title']: continue
				tvshowid = r['tvshowid']
				break
			cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"tvshowid": %s, "season": %s, "filter": {"field": "%s", "operator": "is", "value": "%s"}, "limits": { "start" : 0, "end": 25 }, "properties" : ["title", "season", "episode", "file", "streamdetails"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true }}, "id": "libTvShows"}'
			command = cmd % (tvshowid, args['season'], 'episode', args['episode'])
			response = json.loads(xbmc.executeJSONRPC(command))
			if 'result' in response and 'episodes' in response['result']:
				for episode in response['result']['episodes']:
					if episode['file'].endswith('.strm'):
						continue
					else:
						result = {"title": self.get_file_from_url(episode['file']), "raw_url": episode['file'], "service": self.service, "host": self.name, "size": kodi.vfs.get_size(episode['file']), "extension": self.get_file_type(episode['file']), "quality": QUALITY.LOCAL}
						results.append(result)
						break
		results = self.verify_results(self.process_results, results)
		return results
	
	def search_movies(self, args):
		results = []
		filter_str = '{{"field": "title", "operator": "contains", "value": "{search_title}"}}'
		filter_str = '{{"and": [%s, {{"field": "year", "operator": "is", "value": "%s"}}]}}' % (filter_str, args['year'])
		cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "filter": %s, "limits": { "start" : 0, "end": 25 }, "properties" : ["title", "year", "file", "streamdetails"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true } }, "id": "libMovies"}'
		command = cmd % (filter_str.format(search_title=args['title']))
		data = json.loads(xbmc.executeJSONRPC(command))
		if 'result' in data and 'movies' in data['result']:
			for r in data['result']['movies']:
				if str(r['year']) != args['year'] or args['title'] not in r['title'] or r['file'].endswith('.strm'): continue
				result = {"title": self.get_file_from_url(r['file']), "raw_url": r['file'], "service": self.service, "host": self.name, "size": kodi.vfs.get_size(r['file']), "extension": self.get_file_type(r['file']), "quality": QUALITY.LOCAL}
				results.append(result)
				break
		results = self.verify_results(self.process_results, results)
		return results
