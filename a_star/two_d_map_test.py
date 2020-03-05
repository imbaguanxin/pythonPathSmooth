from a_star.two_d_map import map2D
from a_star.a_star_solver import aStar
import numpy as np
import matplotlib.pyplot as plt

test_map = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                     [1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                     [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
                     [1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
                     [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

test_map2 = np.zeros((600, 600))
test_map2[0, :] = 1
test_map2[599, :] = 1
test_map2[:, 0] = 1
test_map2[:, 599] = 1
test_map2[400:500, 100:200] = 1
test_map2[450:550, 350:450] = 1
test_map2[200:300, 200:300] = 1
test_map2[50:150, 50:150] = 1
test_map2[100:320, 500:600] = 1


def main():
    test_2d_map = map2D(test_map2)
    plt_img = test_2d_map.render_image()

    plt.imshow(plt_img)
    plt.show()

    astar_solver = aStar(test_2d_map)
    start_p = np.array([20, 20])
    end_p = np.array([570, 570])
    path = np.array(astar_solver.path_plan(start_p, end_p, visual=False))

    filter_path = np.array(astar_solver.line_fitter(path))

    path_y = filter_path.T[0]
    path_x = filter_path.T[1]
    img_result = astar_solver.map2d.render_image()
    plt.imshow(img_result)
    plt.plot(path_x, path_y)
    plt.show()

    print(filter_path)


if __name__ == "__main__":
    main()
