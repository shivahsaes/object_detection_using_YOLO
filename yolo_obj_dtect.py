import cv2
import numpy as np
print("YOLO OBJECT DETECTION MODEL \n ")

print("written by Shiva Sai Sankoju \n")

print("loading...................")

# Load Yolo
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("class.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]




#loading a image

img=cv2.imread('test1.jpg')
img=cv2.resize(img,(1000,700))


#defining h,w,c of image
height,width,channel = img.shape

#detecting objects using blob

blob = cv2.dnn.blobFromImage(img,0.00392,(416,416),(0,0,0), True,crop = False)
net.setInput(blob)
outs=net.forward(output_layers)


#showing info of objects on the screen 

confidences = []
class_ids = []
boxes = []

for out in outs:
	for detection in out:
		scores = detection[5:]
		class_id = np.argmax(scores)
		confidence = scores[class_id]
		if confidence>0.5:
			#object detected
			centre_x = int(detection[0]*width)
			centre_y = int(detection[1]*height)
			w = int(detection[2]*width)
			h = int(detection[3]*height)

			#rectangle coordinates
			x = int(centre_x - w/2)
			y = int(centre_y - h/2)

			boxes.append([x,y,w,h])
			confidences.append(float(confidence))
			class_ids.append(class_id)
indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.5,0.4)

font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        colors = np.random.uniform(0,255,size=(len(classes),3))
        color = colors[i]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
        
print("number of objects detected = " +str(len(boxes)))
print("confidence levels = ")
for x in confidences:
        print(float(x)*100 ,"%")



cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
