# pip install opencv-python
# pip install google-cloud_vision
# you need to install pandas etc

# I wrote this code to be able to read an image from a webcam using google cloud vision ML API
# then it compares the text the program has read to the feed file using Levenshtein
# i like this as it seems to work well just by comparing two strings
# so it looks up a website based on the image it sees

# YOU MUST ADD YOUR GOOGLE CLOUD API KEY FOR THIS TO WORK. PLACE IT IN THE SAME
# DIRECTORY AS MAIN.PY

import cv2

# define a video capture object
vid = cv2.VideoCapture(0)

while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)
    print('Press q to capture the image and read the text')

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite(filename='image.jpg', img=frame)
        print('Image has been saved')
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

import io
import os
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'YOUR_GOOGLE_CLOUD_VISION_API_KEY_FILE_HERE.json'

# Imports the Google Cloud client library
from google.cloud import vision

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('image.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations
#print(labels)

response = client.text_detection(image=image)  # returns TextAnnotation
df = pd.DataFrame(columns=['locale', 'description'])

texts = response.text_annotations
for text in texts:
    df = df.append(
        dict(
            locale=text.locale,
            description=text.description
        ),
        ignore_index=True
    )

wordsonbottle = str(df['description'][0])

# Load the Pandas libraries with alias 'pd'
import pandas as pd
data = pd.read_csv("feed.csv")
# Preview the first 5 lines of the loaded data
# print(data.head())

import Levenshtein as lev

highestRatio = 0

for ind in data.index:
     fuseName = str((data['Name'][ind]))
     cleanfuseName = ''.join(char for char in fuseName if char.isalnum())
     cleanwordsonbottle = ''.join(char for char in wordsonbottle if char.isalnum())
     Distance = lev.distance(cleanfuseName.lower(), cleanwordsonbottle.lower()),
     Ratio = lev.ratio(cleanfuseName.lower(), cleanwordsonbottle.lower())
     #print(cleanwordsonbottle + '---' + cleanfuseName + '--- Distance:' + str(Distance) + '--- Ratio:' + str(Ratio))
     if float(Ratio) > highestRatio:
         highestRatio = float(Ratio)
         maximumindex = ind
         #print('Best match:' + str(highestRatio))

print('\n')
print('With a match score of ' + str(highestRatio) + '. I saw :'+ cleanwordsonbottle + ' to find: ' + data['Name'][maximumindex])
print('Please find below the link to the website for ' + data['Name'][maximumindex])
print(data['ProductUrl'][maximumindex])