import time
import face_recognition    
import cv2
import numpy as np
import uuid
from threading import Thread
from flask import Flask, jsonify, request
import os

script_dir = os.path.dirname(__file__)

print(script_dir)

if not os.path.exists(script_dir+"//faces"):
     os.makedirs(script_dir+"//faces")

if not os.path.exists(script_dir+"//faces//facialdata"):
     os.makedirs(script_dir+"//faces//facialdata")

face_cascade = cv2.CascadeClassifier(script_dir+"\\face_detector.xml")

def checkface(image_path):
         time.sleep(5)
         unknown_image = cv2.imread(image_path)
         print(image_path)
         gray = cv2.cvtColor(unknown_image, cv2.COLOR_RGB2GRAY)
         faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5)
         if len(faces)==0:
             
             return False
         
         return True


def rememberthisface(name,note):
                        
        i = 1        
        total_encoding = []
        while i<4: 
            img = face_recognition.load_image_file(script_dir+f"\\faces\\{name}{i}.jpg",mode='RGB')

            faceenc = face_recognition.face_encodings(img)
            total_encoding.extend(faceenc)
            i+=1
        
            time.sleep(2)
        
        nameencoding = name+"faceencoding.txt"
        notefile = name + "note.txt"
        
        
        total_encodingdup = total_encoding.copy()
        total_encoding = np.array(total_encoding)

        with open(script_dir+"\\faces"+"\\"+"facialdata\\"+name+"\\"+nameencoding,'w') as f:
            total_encodingS=str(total_encodingdup)
            total_encodingS = total_encodingS.replace('array','')
            total_encodingS = total_encodingS.replace('(','')
            total_encodingS = total_encodingS.replace(')','')
            f.write(str(total_encodingS))
        with open(script_dir+"\\faces"+"\\"+"facialdata\\"+name+"\\"+notefile,'w') as fn:
            fn.write(note)

app = Flask(__name__)
tasks = {}

def checkforfaces(taskid, imgpath):

         unknown_image = face_recognition.load_image_file(imgpath,mode='RGB')
         faceencoding = face_recognition.face_encodings(unknown_image)
         

         directory = script_dir + "\\faces\\facialdata\\"

         for root, dirs, files in os.walk(directory):
             flag = 0
             for filename in files:
               if filename.endswith("faceencoding.txt"):
                 filepath = os.path.join(root, filename)

                 with open(filepath, "r") as f:
                   text = f.read()
                   sfaces = np.array(eval(text))
                   faceencoding = np.array(faceencoding)    
                   results = []
                 
                   for i in sfaces:
                        a = face_recognition.compare_faces(i,faceencoding,tolerance=0.5)
                   results.append(a) 
                   print(a)
                   results = np.array(results)
                   result = results.any()
                   print(result)
                 
                   if result:
                        pathlist = filepath.split('\\')
                        name = pathlist[6]
                        name = name.replace("faceencoding.txt","")
                        flag = 1
                                                                        
               if flag == 1:
                    if filename.endswith("note.txt"):
                         filepath = os.path.join(root, filename)
                         with open(filepath,"r") as f:
                              text = f.read()
                              finalresult =  (name+" has been found in this image."+"This was the note you said when remembering this person. "+text)
                              tasks[taskid] = {'status': 'completed', 'result': finalresult}
                              print(finalresult)
                              return
               else:               
                    finalresult = "No recognised people have been found in the current view"            
                    tasks[taskid] = {'status': 'completed', 'result': finalresult}                     
         print(finalresult)
         

@app.route('/uploadImages', methods=['POST'])
def upload_file():
    text_data = request.form['textData']
    

    for file_key in request.files:
        file = request.files[file_key]
        if file.filename != '':
            filename = file.filename
            app.config['UPLOAD_FOLDER'] = script_dir+"//faces"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    text = eval(text_data)
    print(text_data)
    
      

    if text[0] == "rememberface":
         tests = []
           
         if not os.path.exists(script_dir+"\\faces\\facialdata\\"+text[1]):
            os.makedirs(script_dir+"\\faces\\facialdata\\"+text[1])
            print(f"Folder created successfully."+"C:\\Users\\admin\\Project\\uploads\\infos\\"+text[1])
            thread = Thread(target=rememberthisface,args=(text[1],text[2]))
            thread.start()
         else:
            print(f"Folder already exists."+"C:\\Users\\admin\\Project\\uploads\\"+text[1])
         
         return 'Face Remembered Succesfully'    
            

        
    
@app.route('/upload',methods = ['POST'])
def uploadimage():

    for file_key in request.files:
        file = request.files[file_key]
        if file.filename != '':
            filename = file.filename
            app.config['UPLOAD_FOLDER'] = script_dir+"//faces"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
 
    if not checkface(script_dir+"\\faces\\capturedimage.jpg") :
               return "No Face Detected"
    taskid = str(uuid.uuid4())    
    tasks[taskid] = {'status': 'processing'}
    thread = Thread(target=checkforfaces, args=(taskid, script_dir+"\\faces\\capturedimage.jpg"))
    thread.start()
    return jsonify({'task_id': taskid})
    


@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Invalid task ID'}), 404

    task_info = tasks[task_id]
    if task_info['status'] == 'processing':
        return jsonify({'status': 'processing'}), 202
    else:
        return jsonify({'status': 'completed', 'result': task_info['result']}), 200


if __name__ == '__main__':
    app.run(debug=True)


    
