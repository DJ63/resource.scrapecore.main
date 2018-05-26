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
import json
from commoncore import kodi
from commoncore.baseapi import EXPIRE_TIMES
from scrapecore.scrapers.common import DirectScraper, QUALITY

class comedycentralScraper(DirectScraper):
	service='comedycentral'
	name='ComedyCentral'
	base_url = 'http://www.cc.com'
	referrer = 'http://www.cc.com'
	
	def get_data(self, html):
		data = re.search('var triforceManifestFeed = (.+?);\n', html)
		if data:
			return json.loads(data.group(1))
		data = re.search('var triforceManifestURL = "(.+?)";', html)
		if data:
			return json.loads(data.group(1))
		return False
	
	def resolve_url(self, raw_url):
		from YDStreamExtractor import getVideoInfo
		info = getVideoInfo(raw_url, 3, True)
		if info is None: return ''
		info = info.streams()
		if len(info) > 1:
			streams = []
			info = sorted(info, key=lambda x: x['idx'])
			for video in info:
				streams.append(video['xbmc_url'])
			return 'playlist://' + str(streams)
		else:
			return info[0]['xbmc_url']
		return ''
	
	def list_shows(self):
		shows = []
		html = self.request('/shows', cache_limit=EXPIRE_TIMES.DAY)
		data = self.get_data(html)
		if data:
			if 'manifest' in data:
				for k in data['manifest']['zones']:
					if k in ['header', 'footer', 'ads-reporting', 'ENT_M171']: continue
					feed_url = data['manifest']['zones'][k]['feed']
					if 'ent_m100' in feed_url or 'ent_m150' in feed_url:
						jdata = self.request(feed_url, return_type="json", append_base=False, cache_limit=EXPIRE_TIMES.DAY)
						for l in jdata['result']['data']['items']:
							if 'sortedItems' in l:
								for show in l['sortedItems']:
									shows.append(show)
		return shows
	
	def list_episodes(self, url):
		episodes = []
		html = self.request(url, cache_limit=EXPIRE_TIMES.DAY)
		data = self.get_data(html)
		if data and 'manifest' in data:
			for k in data['manifest']['zones']:
				if k in ['header', 'footer', 'ads-reporting', 'ENT_M171']: continue
				feed_url = data['manifest']['zones'][k]['feed']
				if 'ent_m081' in feed_url or 'ent_m013' in feed_url:
					jdata = self.request(feed_url, return_type="json", append_base=False, cache_limit=EXPIRE_TIMES.DAY)
					for episode in jdata['result']['episodes']:
						episodes.append({"title": episode['title'], "url": episode['canonicalURL'], "image": ""})
		return episodes
