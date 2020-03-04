#!/usr/bin/python3

import numpy as np


class map2D:
    """
    2d map
    """

    color_dic = {"white": 0,
                 "black": 1,
                 "green": 2,
                 "red": 3,
                 "blue": 4,
                 "skyBlue": 5}
    rgb_dic = {0: [255 / 255, 255 / 255, 255 / 255],
               1: [0, 0, 0],
               2: [0, 255 / 255, 0],
               3: [255. / 255, 0, 0],
               4: [0, 0, 255 / 255],
               5: [102. / 255, 204. / 255, 255 / 255]}

    def __init__(self, map2d):
        self.row_size = np.shape(map2d)[0]
        self.col_size = np.shape(map2d)[1]
        self.ori_map = np.copy(map2d)
        self.parent = np.full((self.row_size, self.col_size, 2), -1)
        self.color_stat = np.copy(map2d)

    def valid_pos(self, row, col):
        return 0 <= row < self.row_size and 0 <= col < self.col_size

    def valid_pos_xy(self, x, y):
        return 0 <= x <= self.col_size and 0 <= y <= self.row_size

    def is_blank(self, row, col):
        if self.valid_pos(row, col):
            return self.color_stat[int(row)][int(col)] == 0
        else:
            return False

    def is_blank_xy(self, x, y):
        if self.valid_pos_xy(x, y):
            row, col = self.__transfer_xy(x, y)
            return self.is_blank(row, col)
        else:
            return False

    def is_inside_block(self, row, col):
        dirs = [np.array([1, 0]), np.array([-1, 0]), np.array([0, 1]), np.array([0, -1])]
        pt = np.array([row, col])
        acc = 0
        for singleDir in dirs:
            candidate = pt + singleDir
            if not self.is_blank(candidate[0], candidate[1]):
                acc = acc + 1
        return acc == 4

    def is_inside_block_xy(self, x, y):
        row, col = self.__transfer_xy(x, y)
        return self.is_inside_block(row, col)

    def find_parent(self, row, col):
        if self.valid_pos(row, col):
            return self.parent[int(row)][int(col)]
        else:
            print("({}, {}) is not a valid grid, find parent failed.".format(row, col))

    def set_parent(self, row, col, parent):
        if self.valid_pos(row, col):
            self.parent[int(row)][int(col)] = np.copy(parent)
        else:
            print("({}, {}) is not a valid grid, set parent failed.".format(row, col))

    def set_stat(self, row, col, stat):
        if self.valid_pos(row, col):
            self.color_stat[int(row)][int(col)] = stat
        else:
            print("({},{}) is not available.".format(row, col))

    def get_stat(self, row, col):
        if self.valid_pos(row, col):
            return self.color_stat[int(row)][int(col)]
        else:
            print("({},{}) is not available.".format(row, col))

    def render_image(self):
        result = np.zeros((self.row_size, self.col_size, 3))
        for row in range(0, self.row_size):
            for col in range(0, self.col_size):
                stat = self.color_stat[int(row)][int(col)]
                if stat == 0:
                    result[int(row)][int(col)] = np.array([1, 1, 1])
                elif stat == 1:
                    result[int(row)][int(col)] = np.array([0, 0, 0])
                elif stat == 2:
                    result[int(row)][int(col)] = np.array([0, 1, 0])
                elif stat == 3:
                    result[int(row)][int(col)] = np.array([1, 0, 0])
                elif stat == 4:
                    result[int(row)][int(col)] = np.array([0, 0, 1])
                elif stat == 5:
                    result[int(row)][int(col)] = np.array([102. / 255, 204. / 255, 255 / 255])

            # result[int(row)][int(col)] = np.array(self.rgb_dic[int(self.color_stat[int(row)][int(col)])])
        return result

    def __transfer_xy(self, x, y):
        col = self.col_size - 1 if (x == self.col_size) else np.floor(x)
        row = self.row_size - 1 if (y == 0) else np.floor(self.row_size - y)
        return int(row), int(col)
