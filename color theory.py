import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
import imageio.v2 as imageio
# Open a simple image
parser = argparse.ArgumentParser()
parser.add_argument('--image')
args = parser.parse_args()

img = cv2.imread(r"C:\Users\sansi\OneDrive\Pictures\Screenshots\face.jpg")
img1=imageio.imread(r"C:\Users\sansi\OneDrive\Pictures\Screenshots\face.jpg")
plt.imshow(img1)
plt.show()
if img is None:
    print("No image available")
    exit()

# Converting from BGR to HSV color space
img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Skin color range for HSV color space
HSV_mask = cv2.inRange(img_HSV, (0, 15, 0), (17, 170, 255))
HSV_mask = cv2.morphologyEx(HSV_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

# Converting from BGR to YCbCr color space
img_YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

# Skin color range for YCbCr color space
YCrCb_mask = cv2.inRange(img_YCrCb, (0, 135, 85), (255, 180, 135))
YCrCb_mask = cv2.morphologyEx(YCrCb_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

# Merge skin detection (YCbCr and HSV)
global_mask = cv2.bitwise_and(YCrCb_mask, HSV_mask)
global_mask = cv2.medianBlur(global_mask, 3)
global_mask = cv2.morphologyEx(global_mask, cv2.MORPH_OPEN, np.ones((4, 4), np.uint8))

HSV_result = cv2.bitwise_not(HSV_mask)
YCrCb_result = cv2.bitwise_not(YCrCb_mask)
global_result = cv2.bitwise_not(global_mask)

cv2.imwrite("1_HSV.jpg", HSV_result)
cv2.imwrite("2_YCbCr.jpg", YCrCb_result)
cv2.imwrite("3_global_result.jpg", global_result)

# Get the HSV image and mask it to get only skin
mask = cv2.inRange(img_HSV, (0, 15, 0), (17, 170, 255))
# Merge it with the original image
skin = cv2.bitwise_and(img, img, mask=mask)

# Extract the color RGB and remove the black pixels from the mask
rows, cols, _ = skin.shape
k1, k2, k3 = [], [], []
for i in range(rows):
    for j in range(cols):
        k = skin[i, j]
        if not ((k == np.array([0, 0, 0])).all()):
            k1.append(k[0])
            k2.append(k[1])
            k3.append(k[2])

Bmediant = sum(k1) / len(k1)
Gmediant = sum(k2) / len(k2)
Rmediant = sum(k3) / len(k3)

cv2.imwrite("coloredHSV-SkinDetection.jpg", skin)

# Calculate median color in BGR format
median_color_BGR = (int(Rmediant), int(Gmediant), int(Bmediant))

# Calculate brightness (using average of R, G, and B values)
brightness = (Rmediant + Gmediant + Bmediant) / 3

# Define thresholds for brightness categories
very_dark_threshold = 85
dark_threshold = 125
medium_threshold = 165
light_threshold = 205
# Beyond this is considered very light

# Classify based on brightness
if brightness < very_dark_threshold:
    classification = "Skin Color: Very Dark, Colour palette: Bold and Vibrant undertones (Warm & Vibrant undertones)"
elif very_dark_threshold <= brightness < dark_threshold:
    classification = "Skin Color: Dark, Colour palette: Earth and Jewel undertones"
elif dark_threshold <= brightness < medium_threshold:
    classification = "Skin Color: Medium, Colour palette: Golden and Yellow undertones (Warm undertones)"
elif medium_threshold <= brightness < light_threshold:
    classification = "Skin Color: Light, Colour palette: Grey and Peach undertones (Neutral & Cool undertones)"
else:
    classification = "Skin Color: Very Light, Colour palette: Pink and Blue undertones (Cool undertones)"

print(f"The median color in the detected skin region is classified as: {classification}")

# Display the median color in BGR using Matplotlib
plt.imshow([[median_color_BGR]])

plt.title('Median Color')
plt.show()
