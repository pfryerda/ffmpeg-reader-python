import sys
import requests ##http://docs.python-requests.org/en/master/, install using $ pipenv install requests
import os
import re
from subprocess import call, STDOUT

# NOTE: Sample URLS
# "http://techslides.com/demos/sample-videos/small.mp4"
# "http://www.sample-videos.com/video/flv/720/big_buck_bunny_720p_30mb.flv"

url = sys.argv[1] if sys.argv[1] else "ERROR";
if url == "ERROR":
    raise Exception("Did enter a URL. Please try again with a valid URL")

urlSplitArr = url.split('/')

fileName = urlSplitArr[len(urlSplitArr) - 1]
homeEnvironmentVar = os.environ["HOME"]
fileLocation = homeEnvironmentVar+"/Downloads/"+fileName

print "Saving video to " + fileLocation

res = requests.get(url, stream=True)
res.raise_for_status()

with open(fileLocation, "wb") as file:
    for chunk in res.iter_content(10024): # Writing 10KB at a time
        file.write(chunk)

thumbnail = "thumbnail.bmp"

print "Video Saved. Extracting thumbnail to " + thumbnail

call(["ffmpeg", "-y", "-i", fileLocation, "-vf", "fps=1/600", thumbnail], stdout=open(os.devnull, 'w'), stderr=STDOUT) # -y = always overwrite, -i = url, -vf = video, fps=frequency of capture
call(["open", thumbnail])

# NOTE: Could be improved by having the duration of the video calculated, and the 
# ffmpeg -i file.flv 2>&1 | grep "Duration"| cut -d ' ' -f 4 | sed s/,// | sed 's@\..*@@g' | awk '{ split($1, A, ":"); split(A[3], B, "."); print 3600*A[1] + 60*A[2] + B[1] }'
