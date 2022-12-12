"""Total Q -- color map

         STOP1 FRONT1 BEHIND1 LEFT1 RIGHT1 UP1 DOWN1
STOP0
FRONT0
BEHIND0
LEFT0
RIGHT0
UP0
DOWN0
"""
from vedo import *

import numpy as np


def q_matrix(
        data,
        pos,
        title='',
        xtitle='',
        ytitle='',
        # xlabels=('STOP1', 'FRONT1', 'BEHIND1', 'LEFT1', 'RIGHT1', 'UP1', 'DOWN1'),
        # ylabels=('STOP0', 'FRONT0', 'BEHIND0', 'LEFT0', 'RIGHT0', 'UP0', 'DOWN0'),
        xlabels='',
        ylabels='',
        xrotation=0,
        cmap='Reds',
        vmin=None,
        vmax=None,
        value_precision=4,
        font='Theemim',
        scale=0.0015,
        scalarbar=False,
        lc='white',
        lw=1,
        c='black',
        alpha=1,):
    """
    Generate a matrix, or a 2D color-coded plot with bin labels.

    Returns an ``Assembly`` object.

    Parameters
    ----------
    data : list or numpy array
        the input array to visualize

    pos : tuple
        origin of the plot

    title : str
        title of the plot

    xtitle : str
        title of the horizontal colmuns

    ytitle : str
        title of the vertical rows

    xlabels : list
        individual string labels for each column. Must be of length m

    ylabels : list
        individual string labels for each row. Must be of length n

    xrotation : float
        rotation of the horizontal labels

    cmap : str
        color map name

    vmin : float
        minimum value of the colormap range

    vmax : float
        maximum value of the colormap range

    value_precision : int
        number of digits for the matrix entries or bins

    font : str
        font name

    scale : float
        size of the numeric entries or bin values

    scalarbar : bool
        add a scalar bar to the right of the plot

    lc : str
        color of the line separating the bins

    lw : float
        Width of the line separating the bins

    c : str
        text color

    alpha : float
        plot transparency

    .. hint:: examples/pyplot/np_matrix.py
        .. image:: https://vedo.embl.es/images/pyplot/np_matrix.png
    """
    data = np.asarray(data)
    n, m = data.shape
    gr = shapes.Grid(pos=pos, res=[n, m], s=(0.01, 0.01), c=c, alpha=alpha)
    gr.wireframe(False).lc(lc).lw(lw)

    matr = np.flip(np.flip(data), axis=1).ravel(order="C")
    gr.cmap(cmap, matr, on="cells", vmin=vmin, vmax=vmax)
    sbar = None
    if scalarbar:
        gr.add_scalarbar3d(title_font=font, label_font=font)
        sbar = gr.scalarbar
    labs = None
    if scale != 0:
        labs = gr.labels(
            cells=True,
            scale=scale / max(m, n),
            precision=value_precision,
            font=font,
            justify="center",
            c=c,
        )
        labs.z(0.001)
    t = None
    if title:
        if title == "Matrix":
            title += " " + str(n) + "x" + str(m)
        t = shapes.Text3D(title, font=font, s=0.04, justify="bottom-center", c=c)
        t.shift(0, n / (m + n) * 1.05)

    xlabs = None
    if len(xlabels) == m:
        xlabs = []
        jus = "top-center"
        if xrotation > 44:
            jus = "right-center"
        for i in range(m):
            xl = shapes.Text3D(xlabels[i], font=font, s=0.02, justify=jus, c=c).rotate_z(
                xrotation
            )
            xl.shift((2 * i - m + 1) / (m + n), -n / (m + n) * 1.5, 1.05)
            xlabs.append(xl)

    ylabs = None
    if len(ylabels) == n:
        ylabels = list(reversed(ylabels))
        ylabs = []
        for i in range(n):
            yl = shapes.Text3D(
                ylabels[i], font=font, s=0.02, justify="right-center", c=c
            )
            yl.shift(-m / (m + n) * 1.5, (2 * i - n + 1) / (m + n), 1.05)
            ylabs.append(yl)

    xt = None
    if xtitle:
        xt = shapes.Text3D(xtitle, font=font, s=0.035, justify="top-center", c=c)
        xt.shift(0, -n / (m + n) * 1.05)
        if xlabs is not None:
            y0, y1 = xlabs[0].ybounds()
            xt.shift(0, -(y1 - y0) - 0.55 / (m + n))
    yt = None
    if ytitle:
        yt = shapes.Text3D(
            ytitle, font=font, s=0.035, justify="bottom-center", c=c
        ).rotate_z(90)
        yt.shift(-m / (m + n) * 1.05, 0)
        if ylabs is not None:
            x0, x1 = ylabs[0].xbounds()
            yt.shift(-(x1 - x0) - 0.55 / (m + n), 0)
    asse = Assembly(gr, sbar, labs, t, xt, yt, xlabs, ylabs)
    asse.name = "Matrix"
    return asse


def plot_q_discrete(point, q_array):
    mat = q_matrix(q_array, tuple(point))
    return mat


def show_q_value_discrete_mix(left_points, right_points, q_arrays, num, scene, left_act, right_act):
    """

    Args:
        left_points: (num, 3)
        right_points: (num, 3)
        q_arrays: (num, 7, 7)
        num: points num
        scene: dualarm or dualarmrod
        left_act: (num, 1)
        right_act: (num, 1)

    Returns:

    """
    settings.use_depth_peeling = True

    cm = []
    for i in range(num):
        cm.append(plot_q_discrete(left_points[i], q_arrays[i, :, :]))
        cm.append(plot_q_discrete(right_points[i], q_arrays[i, :, :]))

    pts_left = Points(list(map(tuple, left_points)), c='k')
    pts_right = Points(list(map(tuple, right_points)), c='k')
    spl_left = Line(left_points)
    spl_left.linecolor('green')
    spl_right = Line(right_points)
    spl_right.linecolor('green')

    enviroment = []
    if scene == "dualarmrod":
        enviroment.append(Cylinder(pos=[(-0.005, -0.25, 1.055), (-0.005, -0.25, 1.4655)], r=0.0035, axis=(0, 0, 1)))
        enviroment.append(Cylinder(pos=[(0.005, 0.25, 1.055), (0.005,  0.25, 1.4655)], r=0.0035, axis=(0, 0, 1)))
    if scene == "dualarm":
        enviroment.append(Cylinder(pos=[(0, -0.25, 1.055), (0, -0.25, 1.0655)], r=0.025, axis=(0, 0, 1)))
        enviroment.append(Cylinder(pos=[(0, 0.25, 1.055), (0,  0.25, 1.0655)], r=0.025, axis=(0, 0, 1)))

    # 选择 Q 最大的 joint action
    color_list = ['', 'red', 'blue', 'yellow', 'gray', 'brown', 'orange']
    vec_list = [np.array([0., 0., 0.]),
                np.array([1., 0., 0.]),
                np.array([-1., 0., 0.]),
                np.array([0., -1., 0.]),
                np.array([0., 1., 0.]),
                np.array([0., 0., 1.]),
                np.array([0., 0., -1.])]

    arrows = []
    for i in range(num):
        cm_data = q_arrays[i]
        # 获得最大值的下标
        left_index, right_index = np.unravel_index(np.argmax(cm_data, axis=None), cm_data.shape)
        arrows += [Arrow(left_points[i], left_points[i]+vec_list[left_index]/100, c=color_list[left_index]),
                   Arrow(right_points[i], right_points[i]+vec_list[right_index]/100, c=color_list[right_index])]

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
    show(cm,
         pts_left,
         pts_right,
         spl_left,
         spl_right,
         enviroment,
         arrows,
         pts_left_aux,
         pts_right_aux,
         spl_left_aux,
         spl_right_aux,
         arrows_aux,
         __doc__,
         viewup='z',
         axes=dict(c='black', number_of_divisions=10, yzgrid=False),).close()
