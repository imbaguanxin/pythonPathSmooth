import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

from a_star.two_d_map import map2D


def load_map_from_pic(path):
    image = Image.open(path)
    image = image.convert('L')
    image = image.convert('1')
    data = np.asarray(image)
    data = 1 * data
    data[0, :] = 0
    data[-1, :] = 0
    data[:, 0] = 0
    data[:, -1] = 0
    data = data + 1 - data * 2
    print(data)
    plt.imshow(data)
    # plt.savefig("warehouse2.png", dpi=1600)
    plt.show()
    return data


def shrinkMap(shrink_param=5):
    path = r"./img/warehouser2_balloon.bmp"
    image = cv2.imread(path)
    image = cv2.dilate(image, np.ones((5, 5)), iterations=shrink_param)
    cv2.imwrite("./img/warehouse2_shrink.bmp", image)
    b, g, r = cv2.split(image)
    image = cv2.merge([r, g, b])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plt.imshow(image)
    plt.show()


if __name__ == '__main__':
    warehouse_map = map2D(load_map_from_pic("./img/warehouse2_original.bmp"))
    warehouse_balloon = map2D(load_map_from_pic("./img/warehouse2_balloon.bmp"))
    shrinkMap()
