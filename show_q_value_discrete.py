"""Local Q"""
from vedo import *


def plot_q_discrete(point, q_array):
    # 低于 Q 平均值的方向的箭头不画
    for i in range(1, 7):
        if q_array[i] < 0:
            q_array[i] = 0
    # 如果 STOP 的值最大，就不画箭头
    if np.argmax(q_array) == 0:
        q_array = np.zeros(7)

    vec = np.array([[q_array[1], 0, 0],
                    [-q_array[2], 0, 0],
                    [0, -q_array[3], 0],
                    [0, q_array[4], 0],
                    [0, 0, q_array[5]],
                    [0, 0, -q_array[6]]])

    arrow = [Arrow(point, point + vec[0], c='red'),
             Arrow(point, point + vec[1], c='blue'),
             Arrow(point, point + vec[2], c='yellow'),
             Arrow(point, point + vec[3], c='gray'),
             Arrow(point, point + vec[4], c='brown'),
             Arrow(point, point + vec[5], c='orange')]

    return arrow


def show_q_value_discrete(left_points, right_points, left_q, right_q, num, scene, left_act, right_act):
    """

    Args:
        left_points: (num, 3)
        right_points: (num, 3)
        left_q: (num, 7)
        right_q: (num, 7)
        num: points num
        scene: dualarm or dualarmrod
        left_act: (num, 1)
        right_act: (num, 1)

    Returns:

    """
    settings.use_depth_peeling = True

    arrows = []
    for i in range(num):
        arrows += plot_q_discrete(left_points[i], (left_q[i] - left_q[i].mean()) / left_q[i].std() / 100)
        arrows += plot_q_discrete(right_points[i], (right_q[i] - right_q[i].mean()) / right_q[i].std() / 100)

    pts_left = Points(list(map(tuple, left_points)), c='k')  # 黑色轨迹点--左
    pts_right = Points(list(map(tuple, right_points)), c='k')  # 黑色轨迹点--右
    spl_left = Line(pts_left)
    spl_left.linecolor('green')
    spl_right = Line(pts_right)
    spl_right.linecolor('green')

    enviroment = []
    if scene == "dualarmrod":
        enviroment.append(Cylinder(pos=[(-0.005, -0.25, 1.055), (-0.005, -0.25, 1.4655)], r=0.0035, axis=(0, 0, 1)))
        enviroment.append(Cylinder(pos=[(0.005, 0.25, 1.055), (0.005,  0.25, 1.4655)], r=0.0035, axis=(0, 0, 1)))
    if scene == "dualarm":
        enviroment.append(Cylinder(pos=[(0, -0.25, 1.055), (0, -0.25, 1.0655)], r=0.025, axis=(0, 0, 1)))
        enviroment.append(Cylinder(pos=[(0, 0.25, 1.055), (0,  0.25, 1.0655)], r=0.025, axis=(0, 0, 1)))

    color_list = ['', 'red', 'blue', 'yellow', 'gray', 'brown', 'orange']
    vec_list = [np.array([0., 0., 0.]),
                np.array([1., 0., 0.]),
                np.array([-1., 0., 0.]),
                np.array([0., -1., 0.]),
                np.array([0., 1., 0.]),
                np.array([0., 0., 1.]),
                np.array([0., 0., -1.])]

    # display action
    left_points_aux = left_points + np.array([0, 0.1, 0])
    right_points_aux = right_points - np.array([0, 0.1, 0])
    pts_left_aux = Points(list(map(tuple, left_points_aux)), c='k')
    pts_right_aux = Points(list(map(tuple, right_points_aux)), c='k')
    spl_left_aux = Line(left_points_aux)
    spl_left_aux.linecolor('green')
    spl_right_aux = Line(right_points_aux)
    spl_right_aux.linecolor('green')

    arrows_aux = []
    for i in range(num):
        arrows_aux += [Arrow(left_points_aux[i],
                             left_points_aux[i]+vec_list[left_act[i]]/100, c=color_list[left_act[i]]),
                       Arrow(right_points_aux[i],
                             right_points_aux[i]+vec_list[right_act[i]]/100, c=color_list[right_act[i]])]

    # By specifying axes in show(), new axes are created which span the whole bounding box.
    # Options are passed through a dictionary
    show(arrows,
         pts_left,
         pts_right,
         spl_left,
         spl_right,
         enviroment,
         pts_left_aux,
         pts_right_aux,
         spl_left_aux,
         spl_right_aux,
         arrows_aux,
         __doc__,
         viewup='z',
         axes=dict(c='black', number_of_divisions=10, yzgrid=False),).close()
