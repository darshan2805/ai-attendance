1# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 13:14:58 2021

@author: DARSHAN
"""

import boto3
import csv

client = boto3.client('rekognition',
                      aws_access_key_id = "", 
                      aws_secret_access_key = "",
                      region_name = 'ap-south-1')

def list_faces_in_collection(collection_id):
    maxResults=2
    faces_count=0
    tokens=True
    
    response=client.list_faces(CollectionId=collection_id,
                               MaxResults=maxResults)
    
    print('Faces in collection : ' + collection_id)
    while tokens:
        faces=response['Faces']
        for face in faces:
            print("Face Id :"+ face["FaceId"]) 
            print ("External Id : " + face["ExternalImageId"]) 
            faces_count+=1
        if 'NextToken' in response:
            nextToken=response[ 'NextToken']
            response=client.list_faces(CollectionId=collection_id,
                                       NextToken=nextToken, MaxResults=maxResults)
        else:
            tokens=False
    return faces_count

def main():
    bucket = 'ai-attendance'
    collection_id = 'ai-attendance'
    
    faces_count=list_faces_in_collection(collection_id)
    print("faces count: " + str(faces_count))
    
if __name__ == "__main__":
    main()
