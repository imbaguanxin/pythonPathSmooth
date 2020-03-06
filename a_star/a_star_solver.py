#!/usr/bin/python3

import numpy as np
import math
import matplotlib.pyplot as plt
import copy


class aStar:

    def __init__(self, map2d):
        self.map2d = copy.copy(map2d)
        self.__waiting_list = []
        self.__waiting_list_score = np.array([])
        self.__score_flag = "diagonal"

    def path_plan(self, start_point, end_point, score_flag="diagonal", grid_size=1, draw_count=10000, visual=True):
        """
        The main function of astar algorithm
        :param start_point: point to begin
        :param end_point: destination
        :param score_flag: the distance function. Default is "diagonal", possible other options:"cartesian", "manhattan"
        :param grid_size: the search step, default is 1
        :param draw_count: the number of step in each drawing
        :param visual: whether do visualization during astar search
        :return: the continuous path way point
        """
        self.__waiting_list = []
        self.__score_flag = score_flag
        # populating the waiting list with the starting point
        score_g, score_h = self.__find_score(start_point, start_point, end_point, 0)
        self.__waiting_list.append([start_point, score_h])
        self.__waiting_list_score = \
            np.concatenate((self.__waiting_list_score, np.array([score_h + score_g])), axis=None)
        # 8 possible directions
        direction_list = [np.array([1, 0]), np.array([0, 1]), np.array([1, 1]), np.array([-1, 0]), np.array([0, -1]),
                          np.array([-1, 1]), np.array([-1, -1]), np.array([1, -1])]
        for i in range(0, len(direction_list)):
            direction_list[i] = direction_list[i] * grid_size
        loop_count = 0

        # ensure start and destination is blank.
        if (not self.map2d.is_blank(end_point[0], end_point[1])) or (
                not self.map2d.is_blank(start_point[0], start_point[1])):
            print("start point or destination not blank, please reset.")
        else:
            self.map2d.set_stat(start_point[0], start_point[1], 3)
            # start searching
            while self.__waiting_list:
                loop_count = loop_count + 1
                candidate = self.__waiting_list_min()
                candidate_point = candidate[0]
                # check each direction
                for direction in direction_list:
                    father_h = candidate[1]
                    next_point = candidate_point + direction
                    if self.map2d.get_stat(next_point[0], next_point[1]) == 0:
                        # find score
                        score_g, score_h = self.__find_score(candidate_point, next_point, end_point, father_h)
                        # populating waiting list
                        self.__waiting_list.append([np.copy(next_point), score_h])
                        self.__waiting_list_score = np.concatenate(
                            (self.__waiting_list_score, np.array([score_h + score_g])), axis=None)
                        # set have been to and parent
                        self.map2d.set_stat(next_point[0], next_point[1], 3)
                        self.map2d.set_parent(next_point[0], next_point[1], candidate_point)
                        if np.all(np.absolute(next_point - end_point) < np.array([0.001, 0.001])):
                            self.__waiting_list = []
                            break
                if visual and loop_count == draw_count:
                    loop_count = 0
                    img_result = self.map2d.render_image()
                    plt.imshow(img_result)
                    plt.show()
            if visual:
                img_result = self.map2d.render_image()
                plt.imshow(img_result)
                plt.show()
            print("astar finished!")
            # Find the way points
            way_point = [np.copy(end_point)]
            curr_p = np.copy(end_point)
            curr_parent = self.map2d.find_parent(curr_p[0], curr_p[1])
            # loop until finding the start point.
            while not np.all(np.absolute(curr_parent - np.array([-1, -1])) < np.array([0.001, 0.001])):
                way_point.insert(0, curr_parent)
                curr_p = curr_parent
                curr_parent = self.map2d.find_parent(curr_p[0], curr_p[1])
            return way_point

    def line_fitter(self, way_point):
        """
        simplify way points to turning points
        :param way_point: result from path planning
        :return: simplified points
        """
        result = [way_point[0]]
        if len(way_point) > 2:
            curr_pt = way_point[0]
            next_pt = way_point[1]
            curr_dir = next_pt - curr_pt
            for i in range(1, len(way_point) - 1):
                curr_pt = way_point[i]
                next_pt = way_point[i + 1]
                direction = next_pt - curr_pt
                if not np.all(np.absolute(direction - curr_dir) < np.array([0.001, 0.001])):
                    result.append(next_pt)
                    curr_dir = direction
            result.append(way_point[-1])
        return result

    def __waiting_list_min(self):
        """
        Find the point with minimum score in waiting list
        :return:
        """
        if self.__waiting_list:
            min_index = int(np.argmin(self.__waiting_list_score))
            self.__waiting_list_score = np.delete(self.__waiting_list_score, min_index)
            result = self.__waiting_list[min_index]
            self.__waiting_list.pop(min_index)
            return result
        else:
            print("waiting list is empty when finding min!")

    def __find_score(self, curr_p, next_p, dest_p, father_h):
        h, g = 0, 0
        if self.__score_flag == "diagonal":
            g = abs(abs(next_p[0] - dest_p[0]) - abs(dest_p[1] - next_p[1])) \
                + math.sqrt(2) * min(abs(next_p[0] - dest_p[0]), abs(dest_p[1] - next_p[1]))
            h = np.linalg.norm(curr_p - next_p, ord=2) + father_h
        elif self.__score_flag == "cartesian":
            g = np.linalg.norm(next_p - dest_p, ord=2)
            h = np.linalg.norm(curr_p - next_p, ord=2) + father_h
        elif self.__score_flag == "manhattan":
            g = np.lianlg.norm(next_p - dest_p, ord=1)
            h = np.linalg.norm(curr_p - next_p, ord=1) + father_h
        return g, h
