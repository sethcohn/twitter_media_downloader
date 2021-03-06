import json
import re
from os.path import splitext, basename

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse


def generateResults(inputFile, outputFile, filenameFormat):
	file = open(inputFile).read()
	data = json.loads(file)

	results = {
		'files': {},
		'urls': {
			'periscope': [],
			'instagram': [],
			'others': []
		},
		'text': []
	}

	def slugify(value):
	    import unicodedata
	    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
	    value = re.sub('[<>/\\:"|?*]', '-', value).strip().lower()
	    return value

	def parseFilename(format, date, url):
		disassembled = urlparse(url)
		file = basename(disassembled.path)
		filename, ext = splitext(file)
		replaced = format.replace('%date%', date).replace('%filename%', filename).replace('%ext%', ext[1:])
		slugified = slugify(replaced)
		return slugified

	for media in data['media']:
		# Text
		if media['text']:
			results['text'].append(media['text'])

		# Urls
		for urlType in media['urls']:
			for url in media['urls'][urlType]:
				results['urls'][urlType].append(url)

		# Files
		for url in media['images'] + media['videos']:
			filename = parseFilename(filenameFormat, media['date'], url)
			results['files'][filename] = url

	with open(outputFile, 'w') as file:
		json.dump(results, file, indent=4, default=lambda x:str(x))