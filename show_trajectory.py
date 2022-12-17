from vedo import *


def show_trajectory_discrete(left_points_ref, right_points_ref, left_points, right_points, num, scene, left_act, right_act):
    """

    Args:
        left_points_ref: (100, 3)
        right_points_ref: (100, 3)
        left_points: (num, 3)
        right_points: (num, 3)
        num: points num
        scene: dualarm or dualarmrod
        left_act: (num, 1)
        right_act: (num, 1)

    Returns:

    """
    settings.use_depth_peeling = True

    # display reference trajectory
    pts_left_ref = Points(list(map(tuple, left_points_ref)), c='g')  # 黑色轨迹点--左
    pts_right_ref = Points(list(map(tuple, right_points_ref)), c='g')  # 黑色轨迹点--右
    spl_left_ref = Line(pts_left_ref)
    spl_left_ref.linecolor('green')
    spl_right_ref = Line(pts_right_ref)
    spl_right_ref.linecolor('green')

    # display enviroment
    enviroment = []
    if scene == "dualarmrod":
        enviroment.append(Cylinder(pos=[(-0.005, -0.25, 1.055), (-0.005, -0.25, 1.4655)], r=0.0035, axis=(0, 0, 1)))
        enviroment.append(Cylinder(pos=[(0.005, 0.25, 1.055), (0.005,  0.25, 1.4655)], r=0.0035, axis=(0, 0, 1)))
    if scene == "dualarm":
        enviroment.append(Cylinder(pos=[(0, -0.25, 1.055), (0, -0.25, 1.0655)], r=0.025, axis=(0, 0, 1)))
        enviroment.append(Cylinder(pos=[(0, 0.25, 1.055), (0,  0.25, 1.0655)], r=0.025, axis=(0, 0, 1)))

    # display trajectory and action
    color_list = ['', 'red', 'blue', 'yellow', 'gray', 'brown', 'orange']
    vec_list = [np.array([0., 0., 0.]),
                np.array([1., 0., 0.]),
                np.array([-1., 0., 0.]),
                np.array([0., -1., 0.]),
                np.array([0., 1., 0.]),
                np.array([0., 0., 1.]),
                np.array([0., 0., -1.])]

    pts_left = Points(list(map(tuple, left_points)), c='k')
    pts_right = Points(list(map(tuple, right_points)), c='k')
    spl_left = Line(left_points)
    spl_left.linecolor('black')
    spl_right = Line(right_points)
    spl_right.linecolor('black')

    arrows = []
    for i in range(num):
        arrows += [Arrow(left_points[i],
                             left_points[i]+vec_list[left_act[i]]/100, c=color_list[left_act[i]]),
                       Arrow(right_points[i],
                             right_points[i]+vec_list[right_act[i]]/100, c=color_list[right_act[i]])]

    # By specifying axes in show(), new axes are created which span the whole bounding box.
    # Options are passed through a dictionary
    return spl_left_ref, spl_right_ref, enviroment, pts_left, pts_right, spl_left, spl_right, arrows


def show_trajectory_continuous(left_points_ref, right_points_ref, left_points, right_points, num, scene, left_act, right_act):
    """

    Args:
        left_points_ref: (100, 3)
        right_points_ref: (100, 3)
        left_points: (num, 3)
        right_points: (num, 3)
        num: points num
        scene: dualarm or dualarmrod
        left_act: (num, 3)
        right_act: (num, 3)

    Returns:

    """
    settings.use_depth_peeling = True

    # display reference trajectory
    pts_left_ref = Points(list(map(tuple, left_points_ref)), c='g')  # 黑色轨迹点--左
    pts_right_ref = Points(list(map(tuple, right_points_ref)), c='g')  # 黑色轨迹点--右
    spl_left_ref = Line(pts_left_ref)
    spl_left_ref.linecolor('green')
    spl_right_ref = Line(pts_right_ref)
    spl_right_ref.linecolor('green')

    # display enviroment
    enviroment = []
    if scene == "dualarmrod":
        enviroment.append(Cylinder(pos=[(-0.005, -0.25, 1.055), (-0.005, -0.25, 1.4655)], r=0.0035, axis=(0, 0, 1)))
        enviroment.append(Cylinder(pos=[(0.005, 0.25, 1.055), (0.005,  0.25, 1.4655)], r=0.0035, axis=(0, 0, 1)))
    if scene == "dualarm":
        enviroment.append(Cylinder(pos=[(0, -0.25, 1.055), (0, -0.25, 1.0655)], r=0.025, axis=(0, 0, 1)))
        enviroment.append(Cylinder(pos=[(0, 0.25, 1.055), (0,  0.25, 1.0655)], r=0.025, axis=(0, 0, 1)))

    # display trajectory and action
    pts_left = Points(list(map(tuple, left_points)), c='k')
    pts_right = Points(list(map(tuple, right_points)), c='k')
    spl_left = Line(left_points)
    spl_left.linecolor('black')
    spl_right = Line(right_points)
    spl_right.linecolor('black')

    arrows = []
    for i in range(num):
        arrows += [Arrow(left_points[i], left_points[i]+left_act[i]/100, c="orange"), Arrow(right_points[i], right_points[i]+right_act[i]/100, c="orange")]

    # By specifying axes in show(), new axes are created which span the whole bounding box.
    # Options are passed through a dictionary
    return spl_left_ref, spl_right_ref, enviroment, pts_left, pts_right, spl_left, spl_right, arrows

