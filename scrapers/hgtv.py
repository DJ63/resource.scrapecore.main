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

class hgtvScraper(DirectScraper):
	service='hgtv'
	name='HGTV'
	base_url = 'http://www.hgtv.com'
	referrer = 'http://www.hgtv.com'
	
	settings_definition = """<setting label="{NAME}" type="lsep" />
		<setting default="false" id="{SERVICE}_enable" type="bool" label="Enable {NAME}" visible="true"/>
	"""
	
	def search_shows(self, args):
		results = []
		html = self.request('/shows/full-episodes', cache_limit=EXPIRE_TIMES.DAY)
		a = re.compile('<div class="m-MediaBlock o-Capsule__m-MediaBlock m-MediaBlock--PLAYLIST">.+?href="(.+?)".+?data-src="(.+?)".+?HeadlineText.+?>(.+?)<.+?AssetInfo">(.+?)<', re.DOTALL).findall(html)
		for (url, thumb, name, vidcnt) in a:
			if name == args['title'] and "season-%s" % args['season'] in url:
				html = self.request("http:" + url, append_base=False, cache_limit=EXPIRE_TIMES.DAY)
				html = re.compile('<div id="video-player".+?type="text/x-config">(.+?)</script>',re.DOTALL).search(html)
				if not html: continue
				vids = json.loads(html.group(1))['channels'][0]['videos']
				for v in vids:
					url = v['releaseUrl']
					html = self.request(url, append_base=False, cache_limit=EXPIRE_TIMES.DAY)
					episode = re.compile('"episodeNumber" value=".(.+?)H"',re.DOTALL).search(html)
					if episode and episode.group(1).zfill(3) == str(args['episode']).zfill(3):
						result = {
							"title": v['title'], 
							"raw_url": url, 
							"service": self.service, 
							"host": self.service, 
							"size": 0, 
							"extension": '',
							"quality": QUALITY.HD720
						}
						results.append(result)
						break
				break
		
		results = self.verify_results(self.process_results, results)
		return results
	
	def resolve_url(self, raw_url):
		html = self.request(raw_url, append_base=False)
		match = re.compile('<video src="(.+?)"',re.DOTALL).search(html)
		if match:
			return match.group(1)
		return ''
