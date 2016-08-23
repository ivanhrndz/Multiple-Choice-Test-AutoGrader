import numpy as np
from skimage import exposure, img_as_float
from PIL import Image
import os
import time
import cv2
from skimage.feature import CENSURE
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)


def process_image(img1,img2):
	
	#get face images
	fname="formstograde\\test1.png"
	img1 = np.array(img1))


	img2 = np.array(img2)

	descriptor_extractor = ORB(n_keypoints = 1000 )

	descriptor_extractor.detect_and_extract(img1)
	reference_landmarks = descriptor_extractor.keypoints
	descriptors1 = descriptor_extractor.descriptors

	descriptor_extractor.detect_and_extract(img2)
	landmarks = descriptor_extractor.keypoints
	descriptors2 = descriptor_extractor.descriptors
	matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)
	idx1 = np.array(matches12)[:,0]
	idx2 = np.array(matches12)[:,1]
	#detector = CENSURE()

	#detector.detect(img1)
	#reference_landmarks = detector.keypoints[:100]  
	
	#detector = CENSURE()
	#detector.detect(img2)
	#landmarks = detector.keypoints[:100]  
	
	#feed the landmarks to a procrustes analysis to match a template face landmarks
	transformation = transformation_from_points(reference_landmarks[idx1],landmarks[idx2])
	
	#feed the procrustes to a warpaffline where old coordinates are adjusted to new coordinates

	#h, status = cv2.findHomography(landmarks[idx2],reference_landmarks[idx1])
	#im_dst = cv2.warpPerspective(np.array(img2), h, (img1.shape[1]*1,img1.shape[0]*1))
	warped_img = cv2.warpAffine(np.array(img2), transformation[:2], (img1.shape[1]*2,img1.shape[0]*2))
	from skimage import measure

	# Find contours at a constant value of 0.8
	contours = measure.find_contours(warped_img, 0.8)
	contour_lengths = [len(x) for x in contours]

	projected_image = Image.fromarray(warped_img).convert("L")
	#projected_image.save('result.png')
	rectangle = contours[np.argmax(contour_lengths)]
	x,y = zip(*rectangle)
	
	#save the aligned face image
	isolated = projected_image.crop((np.int(np.min(y))+1, np.int(np.min(x))+1, np.int(np.max(y))-1, np.int(np.max(x))-1))
	return cropscale(isolated,img2.shape)
def cropscale(im,(height,width)):

	aspect = width / float(height)

	ideal_width =588
	ideal_height = 804

	ideal_aspect = ideal_width / float(ideal_height)

	if aspect > ideal_aspect:
		# Then crop the left and right edges:
		new_width = int(ideal_aspect * height)
		offset = (width - new_width) / 2
		resize = (offset, 0, width - offset, height)
	else:
		# ... crop the top and bottom:
		new_height = int(width / ideal_aspect)
		offset = (height - new_height) / 2
		resize = (0, offset, width, height - offset)

	thumb = im.crop(resize).resize((ideal_width, ideal_height), Image.ANTIALIAS)
	return thumb


def transformation_from_points(points1, points2):
    points1 = np.matrix(points1.astype(np.float64))
    points2 = np.matrix(points2.astype(np.float64))

    c1 = np.mean(points1, axis=0)
    c2 = np.mean(points2, axis=0)
    points1 -= c1
    points2 -= c2

    s1 = np.std(points1)*1.0
    s2 = np.std(points2)*1.0
    points1 /= s1
    points2 /= s2

    U, S, Vt = np.linalg.svd(points1.T * points2)
    R = (U * Vt).T

    return np.vstack([np.hstack(((s2 / s1) * R,
                                       c2.T - (s2 / s1) * R * c1.T)),
                         np.matrix([0., 0., 1.])])




