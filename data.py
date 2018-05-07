from PIL import Image
import urllib2 as urllib
from traceback import print_exc
import io
import os
import sys
import pymysql
import pymysql.cursors
from flask import Flask, request, jsonify
import requests 
from uuid import uuid4
from cStringIO import StringIO


app= Flask(__name__)

db = pymysql.connect(host="localhost" ,user="root",password= "pranjal2000",db= "CUSTOMER")

cursor = db.cursor()

#@app.route('/test',methods=['GET'])
#def test():
#	customerid=request.form['']
#	return customerid



@app.route('/', methods=['GET'])
def returnall():
	sql="""SELECT * FROM DOCUMENTS1 where 1"""
	try:   
	    cursor.execute(sql)
	    results = cursor.fetchall()
	    print "columns :", 
	    for col_name in cursor.description:
		print col_name[0],
	    print
	    for row in results:
		print row
		db.commit()
	    return 'success', 200	 
	except Exception as e:
	    print_exc()
	    print "Error: Unable to fetch data from MySQL"
	    db.rollback() 
	    return 'failure', 500


#img_path = "/home/parth/Downloads/test"

#path = "https://www.stasheasy.com/s3/load_file?filePath=webroot/document/pan_proof/627/pan-proof2018-01-06-13-53-53-3919.jpg"

#@app.route('/<path:path>',methods=['POST'])
#def static_file(path):
 #   return app.send_static_file(path)
@app.route('/insert-data', methods=['POST'])
def addon():
	try:
		customer_id = request.form['customer_id']
		
		
		query = """SELECT IMAGE_PATH FROM DOCUMENTS1 WHERE CUST_ID = '{ABC}'""".format(ABC = customer_id)
		cursor.execute(query)
		result=cursor.fetchall()
		response = list()
		#db.commit()
		#img_path = request.form['image_path']
		for image in result:
			compressed_file_name=str(uuid4())+".png"
			img_url  = image[0]
			#print "Getting", img_url
			img_data = requests.get(img_url)
			img  = Image.open(io.BytesIO(img_data.content))
			base_url = "/home/parth/"+compressed_file_name
	
			img.save(base_url,quality=65)
	 
			img.save(base_url,optimize=True,quality=65)
			response.append(base_url)
			#img_file = Image.open(urllib.urlopen(base_url))
			print "GETTING " , base_url
			with open(base_url, 'rb') as f:
				response=f.read()#data
			#os.remove(compressed_file_name)
			return response #data
			
			
		return jsonify({"images": response})
		#return '<html><body><img src="data:image/*;base64,'+data+'" /></body></html>'
	#try:
	#	sql_insert=""" INSERT INTO PHOTOTABLE2 (NAME, IMAGE_PATH) VALUES ('default_name', "{path_of_image}")""".format             (path_of_image=img_path)
	except Exception as e:
	       #print_eximage (5)c()# print "error in inserting ", str(e)
		print "------------------------------------"
		print_exc()
		print "------------------------------------"
		return 'error', 500
'''
	try:
		cursor.execute(image)
	
		db.commit()
		 
	except:
		print "Error: Unable to insert data from MySQL"
	
		db.rollback()
	return 'sucess', 200
'''					       
		    		


if __name__ == '__main__':
    app.run(debug=True)

