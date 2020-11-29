#!/usr/bin/python3

import numpy as np
import math
import matplotlib.pyplot as plt
import copy
from queue import PriorityQueue


class Move:

    def __init__(self, x, y, g, h):
        self.x = x
        self.y = y
        self.g = g
        self.h = h

    def __lt__(self, other):
        selfPriority = self.g + self.h
        otherPriority = other.g + other.h
        return selfPriority < otherPriority

    def get_loc(self):
        return np.array([int(self.x), int(self.y)])


class aStar:

    def __init__(self, map2d):
        self.map2d = copy.copy(map2d)
        self.__waiting_list = PriorityQueue()
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
        self.__waiting_list = PriorityQueue()
        self.__score_flag = score_flag
        # populating the waiting list with the starting point
        score_g, score_h = self.__find_score(start_point, start_point, end_point, 0)
        print(score_g)
        print(score_h)
        init_point = Move(start_point[0], start_point[1], score_g, score_h)
        self.__waiting_list.put(init_point)
        # 8 possible directions
        direction_list = [np.array([1., 0.]),
                          np.array([0., 1.]),
                          np.array([1., 1.]),
                          np.array([-1., 0.]),
                          np.array([0., -1.]),
                          np.array([-1., 1.]),
                          np.array([-1., -1.]),
                          np.array([1., -1.])]
        direction_list = list(map(lambda d: d * grid_size, direction_list))
        loop_count = 0

        # ensure start and destination is blank.
        if (not self.map2d.is_blank(end_point[0], end_point[1])) or (
                not self.map2d.is_blank(start_point[0], start_point[1])):
            print("start point or destination not blank, please reset.")
        else:
            self.map2d.set_stat(start_point[0], start_point[1], 3)
            # start searching
            while not self.__waiting_list.empty():
                loop_count += loop_count
                candidate = self.__waiting_list.get()
                candidate_point = candidate.get_loc()
                # check each direction
                for direction in direction_list:
                    father_h = candidate.h
                    next_point = candidate_point + direction
                    if self.map2d.get_stat(next_point[0], next_point[1]) == 0:
                        # find score
                        score_g, score_h = self.__find_score(candidate_point, next_point, end_point, father_h)
                        # populating waiting list
                        self.__waiting_list.put(Move(next_point[0], next_point[1], score_g, score_h))
                        # set have been to and parent
                        self.map2d.set_stat(next_point[0], next_point[1], 3)
                        self.map2d.set_parent(next_point[0], next_point[1], candidate_point)
                        if np.all(np.absolute(next_point - end_point) < np.array([0.001, 0.001])):
                            self.__waiting_list = PriorityQueue()
                            break
                if visual:
                    loop_count = 0 if loop_count == draw_count else loop_count
                    self.__render()

            if visual:
                self.__render()
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

    def __find_score(self, curr_p, next_p, dest_p, father_h):
        h, g = 0., 0.
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

    def __render(self):
        plt.imshow(self.map2d.render_image())
        plt.show()
