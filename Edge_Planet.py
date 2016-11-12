from planet import api
import os
import cv2

def edges(file):
### runs the canny edge detection on the downloaded planet sat images
    print "file_in", file
    frame = cv2.imread(file)
    edges = cv2.Canny(frame,100,200)
    name, ext = os.path.splitext(file)
    fileout = name + "edges.jpg"
    cv2.imwrite(fileout, edges)

client = api.Client('yourapikey') # you need an API key
body = client.get_scenes_list(scene_type='ortho',count=20) # I think the count is restricted to 1000
geojson = body.get()
# the results are paginated and the total result set count is provided
ls_id=[]
count_cloudy = 0
count_non_cloudy = 0
for f in geojson['features']:
	if f['properties']['cloud_cover']['estimated'] > 0.5:
		count_cloudy = count_cloudy +1
	else:
		count_non_cloudy = count_non_cloudy +1
		ls_id.append(f['id'])

print "count_cloudy", count_cloudy
print "count_non_cloudy", count_non_cloudy
	
directory = '...directory' # define the directory to save the file and later loop through
ids = ls_id[:10]
# create a callback that will write scenes to the 'downloads' directory
# note - the directory must exist!
callback = api.write_to_file(directory)
bodies = client.fetch_scene_geotiffs(ids, callback=callback)
# await the completion of the asynchronous downloads, this is where
# any exception handling should be performed
for b in bodies:
    b.await()
# now all the data has been downloaded you can loop through the directory and call the edge detect method	
for filename in os.listdir(directory):
    if filename.endswith(".tif"):
        frame1 = os.path.join(directory+"/"+filename)
        edges(frame1)
    else:
        continue
