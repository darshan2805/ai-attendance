# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 13:35:27 2021

@author: DARSHAN
"""
# Importing of Liraries

import cv2

import boto3

import datetime

import time as time_1

import requests


#Enabling the Cv2 (video Streaming)

video_capture= cv2.VideoCapture(0, cv2.CAP_DSHOW) #captureDevice = camera


#xml file to detect the faces

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                                    
#Creation of ecſent to HeRognition Service 
client = boto3.client('rekognition',
                      aws_access_key_id = "", 
                      aws_secret_access_key = "",
                      region_name = 'ap-south-1')

# Creation of client to S3 Service

s3client = boto3.client("s3",
                       aws_access_key_id = "", 
                      aws_secret_access_key = "",
                      region_name = 'ap-south-1')

#Defining of upload image function to 53 
def uploadimage():

    bucket ="ai-attendance" # Replace with your bucket name

    filename = 'test.jpg'

    relative_filename = 'test.jpg'


    s3client.upload_file(filename, bucket, relative_filename) 
    print("file Uploaded")



def photo():

    bucket = 'ai-attendance'

    collection_id = 'ai-attendance' # Replace with your collection ID

    fileNames = ['test.jpg'] # Naming of Captured Image

    threshold = 70 # Threshold Limit for the similarity

    maxFaces = 2

    for fileName in fileNames:

        response=client.search_faces_by_image (CollectionId=collection_id,
                                       Image={'S3Object':
                                              {'Bucket': bucket,
                                               'Name': fileName}},
                                           FaceMatchThreshold=threshold,
                                           MaxFaces=maxFaces)
        faceMatches=response ['FaceMatches']
        print ('Matching faces')
        for match in faceMatches:
            print ('FaceId:' + match['Face']['FaceId'])
            print('External Id:' + match['Face']["ExternalImageId"])
            #Assigning a variable for external id
            name1=match['Face']["ExternalImageId" ]
            name=name1.split(".") # Spliting the External id to remove . jog extension
            name=name[0]
            date=str(datetime.datetime.now())[0:11] # Capturing time
            time=time_1.strftime('%H')
            period = ""
            if(time == '9'):
                period = "Period1"
            elif(time == '10') :
                period = "Period2"
            else:
               period = "Period3"
            url = "https://m7k44ipkv6.execute-api.ap-south-1.amazonaws.com/attendance_input?name="+name+"&period="+period
            status = requests.request("GET", url)
            print (status.json())
            print("uploaded to DB")
            print("Student Detected :"+name)
            print('Similarity: ' +"{:.2f}".format(match['Similarity']) + "%")

            

while True:
    
    current_time = datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S ")
    time_1 = datetime.datetime.now()
    print ("present time: ", time_1)
    hr = time_1.strftime('*H')
    sd = time_1. minute;

    # Reading of fromes from video streaming ret, frame video_capture.read()
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30,30)
            )
    for (x, y, w, h) in faces:
        print (faces.shape)
        cv2.putText(frame, "faces detected: " + str(faces.shape[0]), (50, 30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 8, 255), 2)
        cv2.rectangle(frame, (x, y), (x+w+30, y+h+30), (0, 255, 0), 1)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color= frame[y:y+h+30, x:x+w+30]
        imgname = "test.jpg"
        cv2.imwrite(imgname, roi_color)
        uploadimage()
        a = photo() 
        print(a)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('Video', frame)

video_capture.release()
cv2.destroyAllWindows()
