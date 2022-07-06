import numpy as np
from PIL import Image
from math import sqrt

img = Image.open("my_picture.jpg")
pixels = np.array(img)

width, height, channels = pixels.shape

actual_width = ...
actual_units = ...

(x1, y1) = ...
(x2, y2) = ...

pixel_distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

actual_distance = (pixel_distance / width) * actual_width

print(f"The distance between the two points is about {actual_distance:.3f} {actual_units}")