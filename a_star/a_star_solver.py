#!/usr/bin/python3

from a_star.two_d_map import map2D
import numpy as np
import math
import matplotlib.pyplot as plt


class aStar:

    def __init__(self, map2d):
        self.map2d = map2d
        self.waiting_list = []
        self.waiting_list_score = np.array([])
        self.score_flag = "diagonal"

    def path_plan(self, start_point, end_point, score_flag="diagonal", grid_size=1, draw_count=10000, visual=True):
        self.waiting_list = []
        self.score_flag = score_flag
        score_g, score_h = self.find_score(start_point, start_point, end_point, 0)
        self.waiting_list.append([start_point, score_h])
        self.waiting_list_score = np.concatenate((self.waiting_list_score, np.array([score_h + score_g])), axis=None)
        direction_list = [np.array([1, 0]), np.array([0, 1]), np.array([1, 1]), np.array([-1, 0]), np.array([0, -1]),
                          np.array([-1, 1]), np.array([-1, -1]), np.array([1, -1])]
        for i in range(0, len(direction_list)):
            direction_list[i] = direction_list[i] * grid_size
        loop_count = 0

        if (not self.map2d.is_blank(end_point[0], end_point[1])) or (
                not self.map2d.is_blank(start_point[0], start_point[1])):
            print("start point or destination not blank, please reset.")
        else:
            self.map2d.set_stat(start_point[0], start_point[1], 3)
            while self.waiting_list:
                loop_count = loop_count + 1
                candidate = self.waiting_list_min()
                candidate_point = candidate[0]
                for direction in direction_list:
                    father_h = candidate[1]
                    next_point = candidate_point + direction
                    if self.map2d.is_blank(next_point[0], next_point[1]):
                        score_g, score_h = self.find_score(candidate_point, next_point, end_point, father_h)
                        self.waiting_list.append([np.copy(next_point), score_h])
                        self.waiting_list_score = np.concatenate(
                            (self.waiting_list_score, np.array([score_h + score_g])), axis=None)
                        self.map2d.set_stat(next_point[0], next_point[1], 3)
                        self.map2d.set_parent(next_point[0], next_point[1], candidate_point)
                        if np.all(np.absolute(next_point - end_point) < np.array([0.001, 0.001])):
                            self.waiting_list = []
                            break
                if visual and loop_count == draw_count:
                    loop_count = 0
                    img_result = self.map2d.render_image()
                    plt.imshow(img_result)
                    plt.show()
            img_result = self.map2d.render_image()
            plt.imshow(img_result)
            plt.show()
            print("astar finished!")

            way_point = [np.copy(end_point)]
            curr_p = np.copy(end_point)
            curr_parent = self.map2d.find_parent(curr_p[0], curr_p[1])
            while not np.all(np.absolute(curr_parent - np.array([-1, -1])) < np.array([0.001, 0.001])):
                self.map2d.set_stat(curr_p[0], curr_p[1], 2)
                way_point.insert(0, curr_parent)
                curr_p = curr_parent
                curr_parent = self.map2d.find_parent(curr_p[0], curr_p[1])
            self.map2d.set_stat(start_point[0], start_point[1], 4)
            self.map2d.set_stat(end_point[0], end_point[1], 4)
            return way_point

    def waiting_list_min(self):
        if self.waiting_list:
            min_index = int(np.argmin(self.waiting_list_score))
            self.waiting_list_score = np.delete(self.waiting_list_score, min_index)
            result = self.waiting_list[min_index]
            self.waiting_list.pop(min_index)
            return result
        else:
            print("waiting list is empty when finding min!")

    def find_score(self, curr_p, next_p, dest_p, father_h):
        h, g = 0, 0
        if self.score_flag == "diagonal":
            g = abs(abs(next_p[0] - dest_p[0]) - abs(dest_p[1] - next_p[1])) \
                + math.sqrt(2) * min(abs(next_p[0] - dest_p[0]), abs(dest_p[1] - next_p[1]))
            h = np.linalg.norm(curr_p - next_p, ord=2) + father_h
        elif self.score_flag == "cartesian":
            g = np.linalg.norm(next_p - dest_p, ord=2)
            h = np.linalg.norm(curr_p - next_p, ord=2) + father_h
        elif self.score_flag == "manhattan":
            g = np.lianlg.norm(next_p - dest_p, ord=1)
            h = np.linalg.norm(curr_p - next_p, ord=1) + father_h
        return g, h
