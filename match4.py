import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


from scipy import ndimage as ndi

from skimage import feature
fname="formstograde\\test1.png"
img1 = np.array(Image.open(fname).convert("L")).astype(np.uint8)
coin = np.array(Image.open("QR.png").convert("L"))

from skimage import transform as tf
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)

import matplotlib.pyplot as plt


img2 = np.array(Image.open(fname).convert("L").rotate(1,expand=True))

tform = tf.AffineTransform()


descriptor_extractor = ORB(n_keypoints=25)

descriptor_extractor.detect_and_extract(img1)
keypoints1 = descriptor_extractor.keypoints


descriptor_extractor.detect_and_extract(img2)
keypoints2 = descriptor_extractor.keypoints


tform.estimate(keypoints1,keypoints2)

tform2 = tf.SimilarityTransform(scale=tform.scale,rotation=tform.rotation,translation=tform.translation)
warped = tf.warp(img1,tform2)
transformed = tf.warp(img2,tform2.inverse)



