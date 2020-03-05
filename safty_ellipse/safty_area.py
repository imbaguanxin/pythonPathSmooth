import numpy as np
import math
import copy


def find_final_sin_cos(pt1, pt2):
    p_bigger = pt1 if (pt1[0] > pt2[0]) else pt2
    p_smaller = pt2 if (pt1[0] > pt2[0]) else pt1
    dist = np.linalg.norm(pt1 - pt2, ord=2)
    d = p_bigger - p_smaller
    sin = -d[1] / dist
    cos = d[0] / dist
    return sin, cos


def is_in_range(start, dest, check):
    radius = np.linalg.norm(start - dest, ord=2) / 2
    center = (start + dest) / 2
    return np.linalg.norm(center - check) <= radius


def find_b_square(x, y, a, cos, sin):
    up = math.pow(x * sin + y * cos, 2)
    down_up = math.pow(x * cos - y * sin, 2)
    return abs(up / (1 - (down_up / math.pow(a, 2))))


def tangent_line(a_square, b_square, cos, sin, given_pt, ctr):
    turning = np.array([[cos, -sin], [sin, cos]])
    pt = given_pt - ctr
    pt = np.matmul(turning, pt.T)
    a_temp = pt[0] / a_square
    b_temp = pt[1] / b_square
    if a_temp == 0:
        pt1 = np.array([0, 1 / b_temp])
        pt2 = np.array([1, 1 / b_temp])
    elif b_temp == 0:
        pt1 = np.array([1 / a_temp, 0])
        pt2 = np.array([1 / a_temp, 1])
    else:
        pt1 = np.array([0, 1 / b_temp])
        pt2 = np.array([1 / a_temp, 0])
    turning = np.array([[cos, sin], [-sin, cos]])
    pt1 = np.matmul(turning, pt1.T)
    pt2 = np.matmul(turning, pt2.T)
    return get_line_from_pts(pt1.T, pt2.T, given_pt)


def get_line_from_pts(pt1, pt2, ctr):
    d = pt1 - pt2
    if d[0] == 0:
        a = 1
        b = 0
        c = -ctr[0]
    elif d[1] == 0:
        a = 0
        b = 1
        c = -ctr[1]
    else:
        a = d[1] / float(d[0])
        b = -1
        c = ctr[1] - a * ctr[0]
    return a, b, c


def find_search_constraint(pt1, pt2, radius):
    direction = pt1 - pt2
    turning = np.array([[0, -1], [1, 0]])
    dir90 = (np.matmul(turning, direction.T) / np.linalg.norm(direction, ord=2)) * radius
    dir_radius = direction / np.linalg.norm(pt1 - pt2) * radius
    pt190 = pt1 + dir90 + dir_radius
    pt1m90 = pt1 - dir90 + dir_radius
    pt290 = pt2 + dir90 - dir_radius
    pt2m90 = pt2 - dir90 - dir_radius
    line1a, line1b, line1c = get_line_from_pts(pt190, pt1m90, pt190)
    line2a, line2b, line2c = get_line_from_pts(pt290, pt2m90, pt290)
    line3a, line3b, line3c = get_line_from_pts(pt190, pt290, pt190)
    line4a, line4b, line4c = get_line_from_pts(pt1m90, pt2m90, pt1m90)
    return np.array([[line1a, line1b, line1c],
                     [line2a, line2b, line2c],
                     [line3a, line3b, line3c],
                     [line4a, line4b, line4c]])


def find_search_range_dynamic(start, dest, radius, xb, yb):
    xl = math.floor(max(1, min(start[0], dest[0]) - radius))
    xh = math.ceil(min(xb, (max(start[0], dest[0]) + radius)))
    yl = math.floor(max(1, min(start[1], dest[1]) - radius))
    yh = math.ceil(min(yb, (max(start[1], dest[1]) + radius)))
    return xl, xh, yl, yh


def is_same_side(matrix, check, origin):
    ori_res = np.matmul(matrix, np.array([[origin[0], origin[1], 1]]).T)
    check_res = np.matmul(matrix, np.array([[check[0], check[1], 1]]).T)
    return np.all(ori_res * check_res > 0)


def find_b_square_fixed_abratio(pt, adivb, cos, sin, ctr):
    return math.pow((pt[0] - ctr[0]) * cos - (pt[1] - ctr[1]) * sin, 2) / math.pow(adivb, 2) \
           + math.pow((pt[0] - ctr[0]) * sin + (pt[1] - ctr[1]) * cos, 2)


class safetyEllipse:

    def __init__(self, map2d, radius):
        self.map2d = copy.copy(map2d)
        self.__radius = radius

    def ellipse_generate(self, way_point):
        cons_list = []
        ellipse_list = []
        for i in range(0, len(way_point) - 1):
            start_pt = self.map2d.transfer_to_xy(way_point[i])
            dest_pt = self.map2d.transfer_to_xy(way_point[i + 1])
            lines, ellipse = self.__single_seg_ellipse(start_pt, dest_pt)
            cons_list.append(lines)
            ellipse_list.append(ellipse)
        return cons_list, ellipse_list

    def __single_seg_ellipse(self, start, dest):
        # find a square search range
        xl, xh, yl, yh = self.__find_search_range(start, dest)
        ellipse = []
        # build first ellipse
        a = np.linalg.norm(start - dest, ord=2) / 2
        ctr = (start + dest) / 2
        min_b_square = a * a
        min_x, min_y = 1, 1
        sine, cosine = find_final_sin_cos(start, dest)
        for i in range(xl, xh):
            for j in range(yl, yh):
                if ((not self.map2d.is_blank_xy(i, j))
                        and (not self.map2d.is_inside_block_xy(i, j))
                        and is_in_range(start, dest, np.array([i, j]))):
                    # self.map2d.set_stat_xy(i, j, 3)
                    temp_bsq = find_b_square(i - ctr[0], j - ctr[1], a, cosine, sine)
                    if temp_bsq < min_b_square:
                        # print("point: {}, {}".format(i, j))
                        # print(temp_bsq)
                        min_b_square = temp_bsq
                        min_x = i
                        min_y = j
        # color the minimum point and center
        self.map2d.set_stat_xy(min_x, min_y, 3)
        self.map2d.set_stat_xy(math.ceil(ctr[0]), math.ceil(ctr[1]), 4)
        # push the ellipse in the ellipse list
        ellipse.append(np.array([a, math.sqrt(min_b_square), cosine, sine, ctr]))
        # find the tangent line related to the minimum point
        tl1a, tl1b, tl1c = tangent_line(a * a, min_b_square, cosine, sine, np.array([min_x, min_y]), ctr)

        # find the square constraints
        constraint = find_search_constraint(start, dest, self.__radius)
        # add the first tangent line to the constraints
        constraint = np.concatenate((constraint, np.array([[tl1a, tl1b, tl1c]])), axis=0)

        sxl, sxh, syl, syh = find_search_range_dynamic(start, dest, self.__radius, self.map2d.col_size,
                                                       self.map2d.row_size)
        barriers = []
        for i in range(sxl, sxh):
            for j in range(syl, syh):
                if ((not self.map2d.is_blank_xy(i, j))
                        and (not self.map2d.is_inside_block_xy(i, j))
                        and is_same_side(constraint, np.array([i, j]), ctr)):
                    barriers.append(np.array([i, j]))
                    self.map2d.set_stat_xy(i, j, 3)
        abratio = a / math.sqrt(min_b_square)
        while barriers:
            min_place = 0
            min_xy = barriers[0]
            b_square = find_b_square_fixed_abratio(min_xy, abratio, cosine, sine, ctr)
            for i in range(len(barriers)):
                temp_pt = barriers[i]
                temp_b_sqr = find_b_square_fixed_abratio(temp_pt, abratio, cosine, sine, ctr)
                if temp_b_sqr < b_square:
                    b_square = temp_b_sqr
                    min_xy = temp_pt
                    min_place = i
            self.map2d.set_stat_xy(min_xy[0], min_xy[1], 4)
            barriers.pop(min_place)
            ellipse.append(
                np.array([math.sqrt(math.pow(abratio, 2) * b_square), math.sqrt(b_square), cosine, sine, ctr]))
            tla, tlb, tlc = tangent_line(math.pow(abratio, 2) * b_square, b_square, cosine, sine, min_xy, ctr)
            constraint = np.concatenate((constraint, np.array([[tla, tlb, tlc]])), axis=0)
            # delete points in barriers
            barriers = [pt for pt in barriers if is_same_side(constraint, ctr, pt)]
        # color the safe area
        for i in range(sxl, sxh):
            for j in range(syl, syh):
                if is_same_side(constraint, np.array([i, j]), ctr):
                    if self.map2d.get_stat_xy(i, j) == 0:
                        self.map2d.set_stat_xy(i, j, 6)
                    else:
                        self.map2d.set_stat_xy(i, j, 7)
        return constraint, ellipse

    def __find_search_range(self, start, dest):
        dis = np.linalg.norm(start - dest, ord=2) / 2
        ctr = (start + dest) / 2
        x_low = max(1, math.floor(ctr[0] - dis))
        x_high = min(self.map2d.col_size, math.ceil(ctr[0] + dis))
        y_low = max(1, math.floor(ctr[1] - dis))
        y_high = min(self.map2d.row_size, math.ceil(ctr[1] + dis))
        return x_low, x_high, y_low, y_high

    def xy_to_row_col(self, x, y):
        row = -y + self.map2d.row_size
        return row, x

    def ellipse_mesh(self, ellipse_obj, sample=100, xy_to_row_col=True):
        a = ellipse_obj[0]
        b = ellipse_obj[1]
        cos = ellipse_obj[2]
        sin = ellipse_obj[3]
        ctr = ellipse_obj[4]
        rot = np.array([[cos, sin], [-sin, cos]])
        phi = np.linspace(0, math.pi * 2, sample, endpoint=True)
        x = a * np.cos(phi)
        y = b * np.sin(phi)
        xy = np.array([x, y])
        points = np.matmul(rot, xy) + np.repeat(np.array([ctr]).T, sample, axis=1)
        if xy_to_row_col:
            row, col = self.xy_to_row_col(points[0], points[1])
            return np.array([col, row])
        return points

    def line_mesh(self, line, boundary=[0, 800, 0, 800], xy_to_row_col=True):
        a = line[0]
        b = line[1]
        c = line[2]
        min_x = boundary[0]
        max_x = boundary[1]
        min_y = boundary[2]
        max_y = boundary[3]
        if a == 0:
            x = np.array([min_x, max_x])
            y = -c / b * np.array([1, 1])
        elif b == 0:
            y = np.array([min_y, max_y])
            x = -c / a * np.array([1, 1])
        else:
            x = np.array([min_x, max_x])
            y = -c / b + -a / b * x
        if xy_to_row_col:
            row, col = self.xy_to_row_col(x, y)
            return np.array([col, row])
        else:
            return np.array([x, y])
