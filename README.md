# Facial Recogntion Flask Server

## Overview

This Flask server provides facial recognition capabilities by converting facial images into 128-dimensional vectors. It allows you to identify and remember faces by processing images and storing facial embeddings. The server exposes a set of RESTful APIs to interact with the facial recognition system, including adding new faces and identifying faces from images.

## Requirements

- Python
- Flask
- dlib
- face recognition
- numpy
- opencv
- Thread


## Installation

1. Clone the repository

```git clone https://github.com/Mohammed-Saajid/facerecognitionserver.git```

2. Run the server

```python server.py```

3. Host the server using ngrok or any other similar service.

```ngrok http 5000```

## API Endpoints

### - Remember a face :
   - Endpoint : '/uploadImages'
   - Method : 'POST'
   - Description : To remember a face
   - Request body : Three face images with a string which contains the name and note to be added.

### - Upload image to Check for a face :
   - Endpoint : '/upload'
   - Method : 'POST'
   - Description : Uploads an image to start a thread which will start the process of checking whether this face is already recognized or not
   - Request Body : An image which has to be checked.

### Retrieve the status for the Face Recognition thread.'
   - Endpoint : '/result/<task_id>'
   - Method : 'GET'
   - Description : Retrieves the status of the thread  which does the face recogntion task for the respective task number. 
   - Request Body : Task ID         


## Conclusion

This server is originally made for the Echo Sight app, But this structure is a versatile one and can be used for other projects as well. 