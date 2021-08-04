# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 12:30:16 2021

@author: DARSHAN
"""

import boto3 
import csv

client = boto3.client('rekognition',
                      aws_access_key_id = "", 
                      aws_secret_access_key = "",
                      region_name = 'ap-south-1')



def add_faces_to_collection (bucket,photo,collection_id):
    
   response = client.index_faces(CollectionId=collection_id,
                                 Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                 ExternalImageId=photo,
                                 MaxFaces=1,
                                 QualityFilter="AUTO",
                                 DetectionAttributes=['ALL'])

   print ('Results for ' + photo)
   print('Faces indexed:')
   for faceRecord in response['FaceRecords']:
      print(' Face ID: ' + faceRecord['Face']['FaceId']) 
      print(' External Id:' + faceRecord['Face']["ExternalImageId"])
      print(' Location: {}'.format(faceRecord['Face']['BoundingBox']))
    
   print('Faces not indexed:')
   for unindexedFace in response['UnindexedFaces']:
       print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
       print(' Reasons:')
       for reason in unindexedFace['Reasons']:
           print('  ' + reason)

   return len(response ['FaceRecords'])

def main():

    bucket = 'ai-attendance'
    collection_id = 'ai-attendance'
    photos = ["darshan.jpg", "janha.jpeg","naresh.jpeg","kishore.jpeg"]

    for photo in photos:
        indexed_faces_count = add_faces_to_collection (bucket, photo, collection_id)
        print("Faces indexed count: " + str(indexed_faces_count))
        
if __name__ ==  "__main__":
    main()
