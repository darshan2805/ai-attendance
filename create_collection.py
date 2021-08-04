# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 12:19:28 2021

@author: DARSHAN
"""

import boto3
import csv

client = boto3.client('rekognition',
                      aws_access_key_id = "",
                      aws_secret_access_key = "",
                      region_name = 'ap-south-1')

def create_collection(collection_id):
    
    print('Creating collection:' + collection_id)
    
    response=client.create_collection(CollectionId=collection_id)
    
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code:' + str(response['StatusCode']))
    print('Done...')
    
def main():
    collection_id='ai-attendance'
    create_collection(collection_id)
    
if __name__ == "__main__":
    main()
