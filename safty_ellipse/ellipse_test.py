from a_star.two_d_map import map2D
from a_star.a_star_solver import aStar
from safty_ellipse.safty_area import safetyEllipse
from safty_ellipse.safty_area import is_same_side
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


def test():
    constraint = np.array([[1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1]])
    constraint = np.array([[9.09090909e-02, - 1.00000000e+00, 6.28388005e+02],
                           [9.09090909e-02, - 1.00000000e+00, 1.95248359e+02],
                           [-1.10000000e+01, - 1.00000000e+00, 7.99779093e+02],
                           [-1.10000000e+01, - 1.00000000e+00, 8.00220907e+02],
                           [-8.69090909e+00, - 1.00000000e+00, 8.85545455e+02]])
    print(is_same_side(constraint, np.array([50, 400]), np.array([35, 415])))


def main():
    test_2d_map = map2D(test_map2)
    # plt_img = test_2d_map.render_image()
    # plt.imshow(plt_img)
    # plt.show()

    path = [np.array([20, 20]),
            np.array([350, 50]),
            np.array([400, 400]),
            np.array([500, 550])]

    path_y = np.array(path).T[0]
    path_x = np.array(path).T[1]
    safety_ellipse = safetyEllipse(test_2d_map, 50)
    cons_list, ellipse_list = safety_ellipse.ellipse_generate(path)
    img_result = safety_ellipse.map2d.render_image()
    plt.imshow(img_result)
    plt.plot(path_x, path_y)
    for elli_stack in ellipse_list:
        for ellipse in elli_stack:
            single_ellipse = safety_ellipse.ellipse_mesh(ellipse)
            plt.plot(single_ellipse[0], single_ellipse[1])
    plt.plot(path_x, path_y)

    plt.ylim(0, 600)
    plt.xlim(0, 600)
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == "__main__":
    # test()
    main()
