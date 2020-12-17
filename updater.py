import urllib.request, os
url = "https://github.com/Txar/Sector/archive/master.zip"
versionsDownloaded = 1
filename = "versions/Sector.zip"
if os.path.exists(filename) == True:
	while True:
		filename = "versions/Sector (" + str(versionsDownloaded) + ").zip"
		if os.path.exists(filename) == True:
			versionsDownloaded = versionsDownloaded + 1
		else:
			break
	name = "Sector (" + str(versionsDownloaded) + ").zip"
else:
	name = "Sector.zip"
print ("Started downloading.")
filename, headers = urllib.request.urlretrieve(url, filename="versions/" + name)
print ("Downloaded the latest version at: " + str(filename))