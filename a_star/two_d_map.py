#!/usr/bin/python3

import numpy as np


class map2D:
    """
    2d map
    """

    rgb_dic = {0: [255 / 255, 255 / 255, 255 / 255],  # white
               1: [0, 0, 0],  # black
               2: [0, 255 / 255, 0],  # green
               3: [255. / 255, 0, 0],  # red
               4: [0, 0, 255 / 255],  # blue
               5: [102. / 255, 204. / 255, 255 / 255],  # sky blue
               6: [220. / 255, 220. / 255, 220. / 255],  # gainsboro
               7: [156. / 255, 156. / 255, 156. / 255]  # dark grey
               }

    def __init__(self, map2d):
        self.row_size = np.shape(map2d)[0]
        self.col_size = np.shape(map2d)[1]
        self.ori_map = np.copy(map2d)
        self.parent = np.full((self.row_size, self.col_size, 2), -1)
        self.color_stat = np.copy(map2d)

    def valid_pos(self, row, col):
        """
        Find whether a point is valid (within map)
        """
        return 0 <= row < self.row_size and 0 <= col < self.col_size

    def valid_pos_xy(self, x, y):
        """
        Find whether a point is valid (within map) in xy coordinates
        """
        return 0 <= x <= self.col_size and 0 <= y <= self.row_size

    def is_blank(self, row, col):
        """
        Find whether a point is blank in the map
        """
        if self.valid_pos(row, col):
            return self.ori_map[int(row)][int(col)] == 0
        else:
            return False

    def is_blank_xy(self, x, y):
        """
        Find whether a point is blank in the map in xy coordinates
        """
        if self.valid_pos_xy(x, y):
            row, col = self.__transfer_xy(x, y)
            return self.is_blank(row, col)
        else:
            return False

    def is_inside_block(self, row, col):
        """
        Find whether a point is inside a block
        """
        dirs = [np.array([1, 0]), np.array([-1, 0]), np.array([0, 1]), np.array([0, -1])]
        pt = np.array([row, col])
        acc = 0
        for single_dir in dirs:
            candidate = pt + single_dir
            if not self.is_blank(candidate[0], candidate[1]):
                acc = acc + 1
        return acc >= 4

    def is_inside_block_xy(self, x, y):
        """
        Find whether a point is inside a block in xy coordinates
        """
        row, col = self.__transfer_xy(x, y)
        return self.is_inside_block(row, col)

    def find_parent(self, row, col):
        """
        Find the parent. If no parent, return (-1, -1)
        """
        if self.valid_pos(row, col):
            return self.parent[int(row)][int(col)]
        else:
            print("({}, {}) is not a valid grid, find parent failed.".format(row, col))

    def set_parent(self, row, col, parent):
        """
        Set the parent
        """
        if self.valid_pos(row, col):
            self.parent[int(row)][int(col)] = np.copy(parent)
        else:
            print("({}, {}) is not a valid grid, set parent failed.".format(row, col))

    def set_stat(self, row, col, stat):
        """
        Set status of a grid
        :param stat: 0: blank, 1: block, 2: green, 3: red, 4: blue
        """
        if self.valid_pos(row, col):
            self.color_stat[int(row)][int(col)] = stat
        else:
            print("({},{}) is not available.".format(row, col))

    def set_stat_xy(self, x, y, stat):
        """
        Set status of a grid in xy coordinates
        :param stat: 0: blank, 1: block, 2: green, 3: red, 4: blue
        """
        row, col = self.__transfer_xy(x, y)
        self.set_stat(row, col, stat)

    def get_stat(self, row, col):
        """
        Get the status of a grid
        """
        if self.valid_pos(row, col):
            return self.color_stat[int(row)][int(col)]
        else:
            print("({},{}) is not available.".format(row, col))

    def get_stat_xy(self, x, y):
        """
        Get the status of a grid in xy coordinates
        """
        row, col = self.__transfer_xy(x, y)
        return self.get_stat(row, col)

    def render_image(self):
        """
        Provide the matrix that render the image
        """
        result = np.zeros((self.row_size, self.col_size, 3))
        for row in range(0, self.row_size):
            for col in range(0, self.col_size):
                result[int(row)][int(col)] = np.array(self.rgb_dic[int(self.color_stat[int(row)][int(col)])])
        return result

    def __transfer_xy(self, x, y):
        """
        transfer xy coordinates to picture coordinates
        """
        col = self.col_size - 1 if (x == self.col_size) else np.floor(x)
        row = self.row_size - 1 if (y == 0) else np.floor(self.row_size - y)
        return int(row), int(col)

    def transfer_to_xy(self, pt):
        """
        transfer grid to xy coordinates
        """
        x = pt[1]
        y = self.row_size - pt[0]
        return np.array([x, y])
