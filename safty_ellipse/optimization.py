import numpy as np
import math


class quadraticOptimization:

    def genHessenberg(self, input_time):
        result = np.zeros((10 * len(input_time), 10 * len(input_time)))
        for i in range(input_time):
            result[i][i] = input_time[i]
            result[i + 1][i + 1] = input_time[i] * 0.0000001
            result[i + 2][i + 2] = input_time[i] * 0.0000001
            result[i + 3][i + 3] = input_time[i] * 0.0000001
            result[i + 4][i + 4] = input_time[i] * 0.0000001
            result[i + 5][i + 5] = input_time[i]
            result[i + 6][i + 6] = input_time[i] * 0.0000001
            result[i + 7][i + 7] = input_time[i] * 0.0000001
            result[i + 8][i + 8] = input_time[i] * 0.0000001
            result[i + 9][i + 9] = input_time[i] * 0.0000001
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
