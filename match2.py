import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from skimage.feature import match_template
from skimage import measure

fname="formstograde\\test1.png"
img = np.array(Image.open(fname).convert("L")).astype(np.uint8)
coin = np.array(Image.open("QR.png").convert("L"))



contours = measure.find_contours(img, 0.8)

# Display the image and plot all contours found
fig, ax = plt.subplots()
ax.imshow(img, interpolation='nearest', cmap=plt.cm.gray)

for n, contour in enumerate(contours):
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()