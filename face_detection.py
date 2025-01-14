import argparse
import cv2
import imutils
import numpy as np

argp=argparse.ArgumentParser()
argp.add_argument('-p','--protxt',required=True,help='Protxt file for model architecture')
argp.add_argument('-m','--model',required=True,help='saved model file')
argp.add_argument('-c','--confidence',default=0.5,help='confidence of detected face',type=float)
arguments=vars(argp.parse_args())


cnet = cv2.dnn.readNetFromCaffe(arguments["protxt"], arguments["model"])

#cnet=cv2.dnn.readNetFromCaffe(arguments['model'],arguments['protxt'])

name = input('Enter your name : ')

cap=cv2.VideoCapture(0)

face_data =[]
count = 0

while True:

	ret,frame=cap.read()
	if ret==False:
		continue

	#cv2.imshow('frame',frame)
	frame = cv2.flip(frame,1)
	frame = imutils.resize(frame, width=400)

	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,(300, 300), (104.0, 177.0, 123.0))# frame,scalefactor,size,mean
	
	(h, w) = frame.shape[:2]
	cnet.setInput(blob)
	predictions=cnet.forward()


	
	for i in range(predictions.shape[2]): #predictions.shape[2] is the number of detected objects

		confidence=predictions[0,0,i,2]

		if confidence<arguments['confidence']:
			continue

		text = "{:.4f}%".format(confidence * 100)


		box = predictions[0, 0, i, 3:7] * np.array([w, h, w, h])
		
		(startX, startY, endX, endY) = box.astype("int")
		offset=10
		y=startY-offset
		cv2.putText(frame, text, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 240, 255), 2)


		cv2.rectangle(frame,(startX,startY),(endX,endY),(255,255,255),2)
		cv2.imshow('face',frame)
		#print(startX,startY)
		
		if startY<0:
			startY = 0
		if startX<0:
			startX = 0

		a = frame[ startY : endY , startX : endX ]
		a = cv2.resize(a,(100,100))
		count = count +1
		if count % 2 == 0 :	

			a = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
			face_data.append(a)
		
		print(count)
		cv2.imshow('abc',a)
		
		#forcc = cv2.VideoWriter_fourcc(*'YUY2')
		#video = cv2.VideoWriter('data/video.mp4',forcc,20.0,(640,480))
	if count == 500:
		break

	if cv2.waitKey(1) & 0xFF == ord('q') :
		break

# print('frame',frame.shape)
# print('blob',blob.shape)
# print(predictions.shape)
cap.release()
cv2.destroyAllWindows()



# Saving the file:



face_data=np.asarray(face_data)
print(face_data.shape)
face_data=face_data.reshape((face_data.shape[0],-1))
np.save('data/'+ name+'.npy',face_data)
print('data saved succesfully')


#Code to run this programm
# python face_detection.py --protxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel







#Notes by me:	
# at a typical run the shapes are
# frame (300, 400, 3)
# blob (1, 3, 300, 300)
# predictions(1, 1, 110, 7)
