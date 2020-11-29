#!/usr/bin/python3
from random import random

import numpy as np
import math
import matplotlib.pyplot as plt
import copy


class RRT_solver:

    def __init__(self, map2d, discrete_num=5):
        self.map2d = map2d
        self.discrete_num = discrete_num

    def path_plan(self, start_point, end_point, num_vertices, incremental_distance, tol_dist):
        for k in range(num_vertices):
            candidate = self.single_find()

    def single_find(self, from_point, dist):
        while True:
            rand_vec = np.array([random(), random()])
            q_rand = rand_vec / np.linalg.norm(rand_vec) * dist
            dest = np.floor(from_point + q_rand)
            if self.valid_path(from_point, dest):
                return dest

    def valid_path(self, start, end):
        direction = (end - start) / (self.discrete_num + 1.0)
        for k in range(self.discrete_num + 1):
            pt = start + direction * (k + 1)
            if not self.map2d.is_blank(pt[0], pt[1]):
                return False
        return True
