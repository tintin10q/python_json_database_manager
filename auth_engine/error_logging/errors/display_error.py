import os
from glob import iglob

latest = 0

while True:
	for file in iglob("./*.html"):
		
		if "latest_error" in file:
			continue
		if new_latest := os.stat(file).st_ctime > latest:  # never file
			print(f"New error: {file}")
			latest = new_latest
			
			with open(file) as f:
				error = f.read()
				
			with open("latest_error.html", "w+") as latest_error:
				latest_error.write(error)
				
			os.remove(file)
