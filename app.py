# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 00:02:59 2021

@author: DARSHAN
"""

from flask import Flask,render_template,request,redirect,url_for
import requests

app = Flask(__name__)
@app.route('/')

def stats():
    url = "https://ctnb7rko3b.execute-api.ap-south-1.amazonaws.com/attendance_flask/getcount"
    response = requests.get(url)
    r = response.json()
    print(r)
    return render_template('stats.html',a=sum(r),b=str(r[0]),c=str(r[1]),d=str(r[2]),e=str(r[3]))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
