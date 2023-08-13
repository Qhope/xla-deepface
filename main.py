from deepface import DeepFace
import cv2
print("Hello World!")

image_path =[ "beckham1.jpeg", "beckham2.jpeg"]

result = DeepFace.verify(image_path[0], image_path[1])
verified = result["verified"]
facialAreas = result["facial_areas"]
img1Bound = facialAreas["img1"]
img2Bound = facialAreas["img2"]
print(verified)

# draw rectangle on detected face

img1 = cv2.imread(image_path[0])
img2 = cv2.imread(image_path[1])

# convert  x,y,w,h to points
img1Bound['w'] = img1Bound['w'] + img1Bound['x']
img1Bound['h'] = img1Bound['h'] + img1Bound['y']

img2Bound['w'] = img2Bound['w'] + img2Bound['x']
img2Bound['h'] = img2Bound['h'] + img2Bound['y']

cv2.rectangle(img1, (img1Bound['x'], img1Bound['y']), (img1Bound['w'],img1Bound['h']), (0, 255, 0), 2)
cv2.rectangle(img2, (img2Bound['x'], img2Bound['y']), (img2Bound['w'], img2Bound['h']), (0, 255, 0), 2)

# resize img to 720px width and 480px height
img1 = cv2.resize(img1, (400, 400))
img2 = cv2.resize(img2, (400, 400))

# concat 2 images
img = cv2.hconcat([img1, img2])



cv2.imshow("Taylor Swift", img)
# cv2.imshow("Taylor Swift 2", img2)
cv2.waitKey(0)
