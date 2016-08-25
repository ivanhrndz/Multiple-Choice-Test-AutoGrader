import numpy as np
from skimage import exposure, img_as_float
from PIL import Image
import os
import cv2
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)
def rectify(h):
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew

def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")

	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]

	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]

	# return the ordered coordinates
	return rect
def process_image(img):
	blurred = cv2.GaussianBlur(np.array(img), (5, 5), 0)
	#blurred = cv2.medianBlur(gray, 5)

	# apply Canny Edge Detection
	edged = cv2.Canny(blurred, 0, 50)
	orig_edged = edged.copy()

	# find the contours in the edged image, keeping only the
	# largest ones, and initialize the screen contour
	(contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
	contours = sorted(contours, key=cv2.contourArea, reverse=True)


	# get approximate contour
	for c in contours:
		p = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * p, True)

		if len(approx) == 4:
			target = approx
			break


	# mapping target points to 500x647 quadrilateral
	approx = rectify(target)
	w= int(2328 / 5.0)
	h= int(3024 / 5.0)
	pts2 = np.float32([[0,0],[w,0],[w,h],[0,h]])

	M = cv2.getPerspectiveTransform(approx,pts2)
	dst = cv2.warpPerspective(np.array(img),M,(w,h))
	return Image.fromarray(dst).convert("L")

	
def process_image2(img1,img2):
	
	#get the reference image
	
	img1 = img1.convert("L").resize( [int(.50 * s) for s in img1.size], Image.ANTIALIAS )
	img2 = img2.convert("L").resize( [int(.50 * s) for s in img2.size], Image.ANTIALIAS )
	#.resize((500,647), Image.ANTIALIAS)
	#img2 = img2.convert("L").resize((1,647), Image.ANTIALIAS)
	
	img1 = np.array(img1)


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

	#tf=AffineTransform()
	#tf.estimate(reference_landmarks[idx1],landmarks[idx2])
	#warped_img = warp(img2,tf)
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
	resized = isolated.resize((500,647), Image.ANTIALIAS)
	return resized
	
def cropscale(im,(height,width)):

	aspect = width / float(height)

	ideal_width =500
	ideal_height = 647

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




