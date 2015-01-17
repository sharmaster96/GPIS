import urllib, urllib2, os, zipfile, os.path

base_url = "http://archive3d.net/"

#unarchives a file and places its contents in destination
def unzip(filename, destination):
    with zipfile.ZipFile(filename) as zf:
        for member in zf.infolist():
            words, path = member.filename.split('/'), destination
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)

def download_shapes_from(category):
	print "starting download: " + category

	#loop iterates over the 3 categories of shapes to download from
	for num in [8, 429, 436]: #used brute force to generate urls for the 3 categories; no evident pattern
		url, folder, sub_folder_list = base_url + "?category=" + str(num), "Archive3D/" + category, []
		
		#page url generation
		iter_list = [''] + ['&page=' + str(25+24*x) for x in range(31)]
		if num == 8:
			iter_list = iter_list[:2]
		elif num == 436:
			iter_list = iter_list[:13]

		#loop iterates over the pages containing objects in a given category
		for addend in iter_list:
			url += addend
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			if not os.path.exists(folder):
				os.makedirs(folder)
			html_code = response.read()

			counter = 1
			
			#loop iterates over the objects on a given page, downloading, unarchiving, and placing each one in the appropriate location
			while True:
				index, counters = html_code.find('<a href="?a=download&amp;id='), {}
				if index == -1: break
				url_2 = base_url + html_code[index+9:index+36]
				url_2 = url_2.replace('amp;', '')
				sub_request = urllib2.Request(url_2)
				sub_response = urllib2.urlopen(sub_request)
				html_code, html_code_2 = html_code[html_code.find('title="Download')+16:], sub_response.read()
				obj = html_code[:html_code.find("3")-1]
				sub_folder = folder + "/" + obj + "s"
				print "downloading object: " + obj.lower()
				if not os.path.exists(sub_folder):
					os.makedirs(sub_folder)
				if obj in counters.keys():
					counter = counters[obj] + 1
				else:
					counter, counters[obj] = 1, 1
				download_url, dir_name = url_2.replace('id', 'do=get&id'), obj.lower() + "_" + str(counter)
				urllib.urlretrieve(download_url, "temp")
				os.makedirs(sub_folder + "/" + dir_name)
				unzip("temp", sub_folder + "/" + dir_name)

download_shapes_from("Tools & Devices")
download_shapes_from("Kitchen Ware")
download_shapes_from("Kitchen Equipment")

print "download complete."

