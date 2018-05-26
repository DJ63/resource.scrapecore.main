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

class cookingScraper(DirectScraper):
	service='cooking'
	name='CookingCH'
	base_url = 'http://www.cookingchanneltv.com'
	referrer = 'http://www.cookingchanneltv.com'
	show_url = '/videos/players/full-episodes-player'
	
	def resolve_url(self, raw_url):
		if raw_url.startswith('//'): raw_url = 'http:' + raw_url
		html = self.request(raw_url, append_base=False)
		match = re.compile('<video src="(.+?)"',re.DOTALL).search(html)
		if match:
			return match.group(1)
		return ''
	
	def list_shows(self):
		shows = []
		dom = self.request(self.show_url, return_type='dom', cache_limit=EXPIRE_TIMES.DAY)
		temp = dom.find_all('div', {"class": "m-MediaBlock o-Capsule__m-MediaBlock m-MediaBlock--playlist"})
		for t in temp:
			match = t.find('h4')
			title = match.find('span').content('span')
			href = match.find('a').attribute('href')
			show = {"title": title, "url": href, "image": ""}
			shows.append(show)
		return shows
	
	def list_episodes(self, url):
		episodes = []
		if url.startswith('//'): url = 'http:' + url
		html = self.request(url, append_base=False, cache_limit=EXPIRE_TIMES.DAY)
		html = re.compile('<div id="video-player".+?type="text/x-config">(.+?)</script>',re.DOTALL).search(html)
		if not html: return []
		vids = json.loads(html.group(1))['channels'][0]['videos']
		for v in vids:
			episode = {"title": v['title'], "url": v['releaseUrl'], "image": ""}
			episodes.append(episode)
		return episodes
