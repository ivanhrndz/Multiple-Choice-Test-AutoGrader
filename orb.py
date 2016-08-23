from skimage import data
from skimage import transform as tf
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from skimage.feature import CENSURE

img1 = np.array(Image.open("test1.png").convert("L"))
img2 = tf.rotate(img1, 180)
tform = tf.AffineTransform(scale=(1.3, 1.1), rotation=0.5,
                           translation=(0, -200))
img3 = tf.warp(img1, tform)

descriptor_extractor = ORB(n_keypoints=10)

detector = CENSURE()
detector.detect(img1)
keypoints1 = detector.keypoints

#descriptor_extractor.detect_and_extract(img1)
#keypoints1 = descriptor_extractor.keypoints


#descriptor_extractor.detect_and_extract(img2)
#keypoints2 = descriptor_extractor.keypoints

detector = CENSURE()
detector.detect(img2)
keypoints2 = detector.keypoints

detector = CENSURE()
detector.detect(img3)
keypoints3 = detector.keypoints

#descriptor_extractor.detect_and_extract(img3)
#keypoints3 = descriptor_extractor.keypoints

