import math
import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage import transform as tf

margins = dict(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0, right=1)

text = data.text()

tform = tf.SimilarityTransform(scale=1, rotation=math.pi / 4,
                               translation=(text.shape[0] / 2, -100))

rotated = tf.warp(text, tform)
back_rotated = tf.warp(rotated, tform.inverse)

fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(8, 3))
fig.subplots_adjust(**margins)
plt.gray()
ax1.imshow(text)
ax1.axis('off')
ax2.imshow(rotated)
ax2.axis('off')
ax3.imshow(back_rotated)
ax3.axis('off')



from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)
							 
tform = tf.SimilarityTransform(scale=1, rotation=math.pi / 4,
                               translation=(text.shape[0] / 2, -100))
descriptor_extractor = ORB(n_keypoints=25)

descriptor_extractor.detect_and_extract(text)
keypoints1 = descriptor_extractor.keypoints


descriptor_extractor.detect_and_extract(rotated)
keypoints2 = descriptor_extractor.keypoints


tform.estimate(keypoints1,keypoints2)
transformed = tf.warp(rotated,tform.inverse)