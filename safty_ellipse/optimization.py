import numpy as np
import math


class quadraticOptimization:

    def genHessenberg(self, input_time, minimize_param=0.0000001):
        result = np.zeros((10 * len(input_time), 10 * len(input_time)))
        for i in range(input_time):
            result[i][i] = input_time[i]
            result[i + 1][i + 1] = input_time[i] * minimize_param
            result[i + 2][i + 2] = input_time[i] * minimize_param
            result[i + 3][i + 3] = input_time[i] * minimize_param
            result[i + 4][i + 4] = input_time[i] * minimize_param
            result[i + 5][i + 5] = input_time[i]
            result[i + 6][i + 6] = input_time[i] * minimize_param
            result[i + 7][i + 7] = input_time[i] * minimize_param
            result[i + 8][i + 8] = input_time[i] * minimize_param
            result[i + 9][i + 9] = input_time[i] * minimize_param
        return result

    def find_time(self, start, dest, amax, vmax):
        lim = math.pow(vmax, 2) / amax
        dist = np.linalg.norm(start - dest, ord=2)
        if dist < lim:
            return 2 * math.sqrt(dist / amax)
        else:
            return 2 * vmax / amax + (dist - lim) / vmax

    def split_constraint(self, constraint, center):
        ctr = np.array([[center[0], center[1], 1]])
        res = np.matmul(constraint, ctr.T) <= 0
        temp = res - 1
        res = res + temp
        res = np.array([res, res, res])
        modified = constraint * res
        b = modified[:, 3] - 1
        modified = modified[:, 1:2]
        return modified, b

    def constrain_2_A(self, constraint, order, t, num_of_path_segregate, num_seg):
        c1 = np.repeat(constraint[:, 0], order, axis=1)
        c2 = np.repeat(constraint[:, 1], order, axis=1)
        t1 = np.zeros((len(constraint), order))
        for i in range(order):
            for j in range(len(constraint)):
                t1[j, i] = math.pow(t, order - i)
        cons = np.concatenate((c1, c2), axis=1)
        tr = np.concatenate((t1, t1), axis=1)
        context = cons * tr

    def genBeqInitState(self, input_path, init_state):
        if len(input_path) < 3:
            print("Length of the input path should be greater than 2, your input {}".format(len(input_path)))
        else:
            total_length = (len(input_path) - 2) * 8 + 4 + 2
            result = np.zeros(total_length, 1)
            # first point position constraints
            first_point = input_path[0]
            result[0] = first_point[0]
            result[1] = first_point[1]
            # last point position constraints
            last_point = input_path[-1]
            result[2] = last_point[0]
            result[3] = last_point[1]
            # first point speed constraints
            result[4] = init_state[0]
            result[5] = init_state[1]
            return result

    def genBeq(self, input_path):
        if len(input_path) < 3:
            print("Length of the input path should be greater than 2, your input {}".format(len(input_path)))
        else:
            total_length = (len(input_path) - 2) * 8 + 4 + 4
            result = np.zeros((total_length, 1))
            # first point position constraints
            first_point = input_path[0]
            result[0] = first_point[0]
            result[1] = first_point[1]
            # last point position constraints
            last_point = input_path[-1]
            result[2] = last_point[0]
            result[3] = last_point[1]
            return result

    def genAeqInitState(self, input_time):
        last_time = input_time[-1]
        length = len(input_time)
        hard_code_constraints = np.zeros((6, 10 * length))
        # start position
        hard_code_constraints[4, 3] = 1
        hard_code_constraints[5, 8] = 1
        # start position
        hard_code_constraints[0, 4] = 1
        hard_code_constraints[1, 9] = 1
        # end point constraints
        hard_code_constraints[2, 5 * 2 * (length - 1)] = math.pow(last_time, 4)
        hard_code_constraints[2, 5 * 2 * (length - 1) + 1] = math.pow(last_time, 3)
        hard_code_constraints[2, 5 * 2 * (length - 1) + 2] = math.pow(last_time, 2)
        hard_code_constraints[2, 5 * 2 * (length - 1) + 3] = math.pow(last_time, 1)
        hard_code_constraints[2, 5 * 2 * (length - 1) + 4] = 1
        hard_code_constraints[3, 5 * 2 * (length - 1) + 5] = math.pow(last_time, 4)
        hard_code_constraints[3, 5 * 2 * (length - 1) + 6] = math.pow(last_time, 3)
        hard_code_constraints[3, 5 * 2 * (length - 1) + 7] = math.pow(last_time, 2)
        hard_code_constraints[3, 5 * 2 * (length - 1) + 8] = math.pow(last_time, 1)
        hard_code_constraints[3, 5 * 2 * (length - 1) + 9] = 1
        flex_constraints = np.array([])
        for i in range(1, length):
            t = input_time[i - 1]
            temp_four_order_constraints = np.array([])
            for j in range(1, length + 1):
                if i == j:
                    temp = np.array([pow(t, 4), pow(t, 3), pow(t, 2), pow(t, 1)])

    def quadratic_optimization(self, constraints, path, amax, vmax, find_time=True, uniform_time=5, max_iter=10000):
        num_of_total_seg = len(path) - 1
        print("Segment number: {}".format(num_of_total_seg))

        if not len(constraints) == num_of_total_seg:
            print("Constraints size and path size not matched.\nconstraints size = path size + 1")
            print("Your input information:\nsize of constraints: {}. size of path: {}"
                  .format(len(constraints), len(path)))
        else:
            time = []
            if find_time:
                for i in range(num_of_total_seg):
                    time.append(self.find_time(path[i], path[i + 1], amax, vmax))
            else:
                time = np.full(num_of_total_seg, uniform_time)
            A = np.array([])
            B = np.array([])
            for i in range(num_of_total_seg):
                cons = constraints[i]
                ctr = (path[i] + path[i + 1]) / 2
                m, b = self.split_constraint(cons, ctr)
                A_temp = np.array([])
                B_temp = np.array([])
