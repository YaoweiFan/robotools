import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot_env(axes):
    # left hole
    cx, cy, cz = get_cyn_by_axes(offset=[0, -0.25, 0], division=40, main_axis='z', height_end=1.05,
                                 height_start=1, radius=0.025)
    axes.plot_surface(cx, cy, cz, rstride=1, cstride=1, linewidth=0, alpha=0.25, shade=False, color='b')

    cx, cy, cz = get_cyn_by_axes(offset=[0, -0.25, 0], division=40, main_axis='z', height_end=1.05,
                                 height_start=1, radius=0.075)
    axes.plot_surface(cx, cy, cz, rstride=1, cstride=1, linewidth=0, alpha=0.25, color='b')

    # right hole
    cx, cy, cz = get_cyn_by_axes(offset=[0, 0.25, 0], division=40, main_axis='z', height_end=1.05,
                                 height_start=1, radius=0.025)
    axes.plot_surface(cx, cy, cz, rstride=1, cstride=1, linewidth=0, alpha=0.25, shade=False, color='b')
    
    cx, cy, cz = get_cyn_by_axes(offset=[0, 0.25, 0], division=40, main_axis='z', height_end=1.05,
                                 height_start=1, radius=0.075)
    axes.plot_surface(cx, cy, cz, rstride=1, cstride=1, linewidth=0, alpha=0.25, color='b')


def get_cyn_by_axes(radius, height_start, height_end, offset, division, main_axis):

    main_axis = main_axis.lower()

    theta = np.linspace(0, 2*np.pi, division)
    cx = np.array([radius*np.cos(theta)])
    cz = np.array([height_start, height_end])
    cx, cz = np.meshgrid(cx, cz)
    cy = np.array([radius*np.sin(theta)]*2)

    if main_axis == 'z':
        return offset[0]+cx, offset[1]+cy, offset[2]+cz
    elif main_axis == 'y':
        return offset[0]+cx, offset[1]+cz, offset[2]+cy
    elif main_axis == 'x':
        return offset[0]+cz, offset[1]+cy, offset[2]+cx
    else:
        raise ValueError("'x', 'y' or 'z' PLZ")


def set_axes_equal(axes):
    """
    Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      axes: a matplotlib axes, e.g., as output from plt.gca().
    """

    x_limits = axes.get_xlim3d()
    y_limits = axes.get_ylim3d()
    z_limits = axes.get_zlim3d()

    x_range = abs(x_limits[1]-x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1]-y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1]-z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5 * max([x_range, y_range, z_range])

    axes.set_xlim3d([x_middle-plot_radius, x_middle+plot_radius])
    axes.set_ylim3d([y_middle-plot_radius, y_middle+plot_radius])
    axes.set_zlim3d([0.8, 0.8+1.5*plot_radius])


if __name__ == '__main__':
    # 设置图例字号
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()

    # 设置三维图形模式
    ax = fig.gca(projection='3d')

    # 测试数据
    # 0.800 --hole bottom -- 1
    # 0.850 --hole top -- 1.05
    # 0.8775 -- P -- 1.0775
    # 0.8975 -- P
    # P0 = np.array([-0.2, -0.25,  1.045])
    # Q0 = np.array([-0.2,  0.25,  1.045])
    # P1 = np.array([0., -0.25,  1.15])
    # Q1 = np.array([0.,  0.25,  1.15])
    # P2 = np.array([0., -0.25,  1.1])
    # Q2 = np.array([0.,  0.25,  1.1])
    # P3 = np.array([0., -0.25,  1.0575])
    # Q3 = np.array([0.,  0.25,  1.0575])

    P0 = np.array([-0.2, -0.25,  1.055])
    Q0 = np.array([-0.2,  0.25,  1.055])
    P1 = np.array([-0.105, -0.25,  1.6])
    Q1 = np.array([-0.095,  0.25,  1.6])
    P2 = np.array([-0.005, -0.25,  1.485])
    Q2 = np.array([0.005,  0.25,  1.485])
    P3 = np.array([-0.005, -0.25,  1.4655])
    Q3 = np.array([0.005,  0.25,  1.4655])

    # 定义贝塞尔曲线
    def p_bezier(t):
        return (1 - t) ** 2 * P0 + 2 * t * (1 - t) * P1 + t ** 2 * P2

    def q_bezier(t):
        return (1 - t)**2 * Q0 + 2 * t * (1 - t) * Q1 + t**2 * Q2

    # 定义直线
    def p_line(t):
        return (1 - t) * P2 + t * P3

    def q_line(t):
        return (1 - t) * Q2 + t * Q3

    # 在 [0, 1] 范围内的 50 个点上验证贝塞尔曲线
    p_points = np.concatenate((np.array([p_bezier(t) for t in np.linspace(0, 1, 85)]),
                              np.array([p_line(t) for t in np.linspace(0, 1, 15)])))
    q_points = np.concatenate((np.array([q_bezier(t) for t in np.linspace(0, 1, 85)]),
                              np.array([q_line(t) for t in np.linspace(0, 1, 15)])))

    # 分别获取点的 x 坐标和 y 坐标和 z 坐标
    Px, Py, Pz = p_points[:, 0], p_points[:, 1], p_points[:, 2]
    Qx, Qy, Qz = q_points[:, 0], q_points[:, 1], q_points[:, 2]

    # 保存数据
    dataframe = pd.DataFrame({'Px': Px, 'Py': Py, 'Pz': Pz, 'Qx': Qx, 'Qy': Qy, 'Qz': Qz})
    # dataframe.to_csv("../data/trajectory.csv")
    # dataframe.to_csv("../data/rod_trajectory.csv")

    # 绘制图形
    plot_env(ax)
    ax.plot(Px, Py, Pz, label='robot0_eef_trajectory')
    ax.plot(Qx, Qy, Qz, label='robot1_eef_trajectory')
    
    # 显示图例、坐标名称
    ax.legend()
    set_axes_equal(ax)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    # 显示图形
    plt.show()
