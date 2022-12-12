import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import os.path as osp
import numpy as np

DIV_LINE_WIDTH = 50

# Global vars for tracking and labeling data at load time.
units = dict()

def plot_data(data, performance, condition, smooth, estimator):
    if smooth > 1:
        """
        smooth data with moving window average.
        that is,
            smoothed_y[t] = average(y[t-k], y[t-k+1], ..., y[t+k-1], y[t+k])
        where the "smooth" param is width of that window (2k+1)
        """
        y = np.ones(smooth)
        for datum in data:
            x = np.asarray(datum[performance])
            z = np.ones(len(x))
            smoothed_x = np.convolve(x,y,'same') / np.convolve(z,y,'same')
            datum[performance] = smoothed_x

    if isinstance(data, list):
        data = pd.concat(data, ignore_index=True)
    sns.set(style="darkgrid", font_scale=1.5)
    sns.tsplot(data=data, time='steps', value=performance, unit="Unit", condition=condition, ci='sd', estimator=estimator)
    """
    If you upgrade to any version of Seaborn greater than 0.8.1, switch from 
    tsplot to lineplot replacing L29 with:
        sns.lineplot(data=data, x='steps', y=performance, hue=condition, ci='sd', estimator=estimator)
    Changes the colorscheme and the default legend style, though.
    """
    plt.legend(loc='best').set_draggable(True)
    #plt.legend(loc='upper center', ncol=3, handlelength=1,
    #           borderaxespad=0., prop={'size': 13})

    """
    For the version of the legend used in the Spinning Up benchmarking page, 
    swap L38 with:
    plt.legend(loc='upper center', ncol=6, handlelength=1,
               mode="expand", borderaxespad=0., prop={'size': 13})
    """

    xscale = np.max(np.asarray(data['steps'])) > 5e3
    if xscale:
        # Just some formatting niceness: x-axis scale in scientific notation if max x is large
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    plt.tight_layout(pad=0.5)
    plt.xlim(0, 25e6)
    plt.ylim(0, 900)

def get_datasets(logdir, performance):
    """
    Recursively look through logdir for output files produced by
    spinup.logx.Logger. 
    Assumes that any file "progress.txt" is a valid hit. 
    """
    global units
    datasets = []
    for root, _, files in os.walk(logdir):
        if 'config.json' in files:
            exp_name = None
            try:
                config_path = open(os.path.join(root,'config.json'))
                config = json.load(config_path)
                if 'exp_name' in config:
                    exp_name = config['exp_name']
            except:
                print('No file named config.json')

            # condition1 对于同一种算法的不同实验取平均值
            condition1 = exp_name
            # condition2 对于同一种算法的不同实验都绘制一条曲线
            if exp_name not in units:
                units[condition1] = 0
            units[exp_name] += 1
            condition2 = exp_name + '-' + str(units[exp_name])

            exp_data = pd.read_csv(os.path.join(root, performance+'.csv'))

            exp_data.insert(len(exp_data.columns), 'Unit', units[exp_name])
            exp_data.insert(len(exp_data.columns), 'Condition1', condition1)
            exp_data.insert(len(exp_data.columns), 'Condition2', condition2)
            exp_data.insert(len(exp_data.columns), 'steps', exp_data['Step'])
            exp_data.insert(len(exp_data.columns), performance, exp_data['Value'])
            datasets.append(exp_data)
            
    return datasets


def get_all_datasets(all_logdirs, performance, select, exclude):
    """
    For every entry in all_logdirs,
        1) check if the entry is a real directory and if it is, 
           pull data from it; 
        2) if not, check to see if the entry is a prefix for a 
           real directory, and pull data from that.
    """
    logdirs = []
    for logdir in all_logdirs:
        if osp.isdir(logdir) and logdir[-1]==os.sep:
            logdirs += [logdir]
        else:
            basedir = osp.dirname(logdir)
            fulldir = lambda x : osp.join(basedir, x)
            prefix = logdir.split(os.sep)[-1]
            listdir= os.listdir(basedir)
            logdirs += sorted([fulldir(x) for x in listdir if prefix in x])

    """
    Enforce selection rules, which check logdirs for certain substrings.
    Makes it easier to look at graphs from particular ablations, if you
    launch many jobs at once with similar names.
    """
    if select is not None:
        logdirs = [log for log in logdirs if all(x in log for x in select)]
    if exclude is not None:
        logdirs = [log for log in logdirs if all(not(x in log) for x in exclude)]

    # Verify logdirs
    print('Plotting from...\n' + '='*DIV_LINE_WIDTH + '\n')
    for logdir in logdirs:
        print(logdir)
    print('\n' + '='*DIV_LINE_WIDTH)

    # Load data from logdirs
    data = []
    for log in logdirs:
        data += get_datasets(log, performance)
    return data


def make_plots(all_logdirs, performance, condition, smooth, select, exclude, estimator):
    data = get_all_datasets(all_logdirs, performance, select, exclude)
    estimator = getattr(np, estimator)      # choose what to show on main curve: mean? max? min?
    plt.figure()
    plot_data(data, performance, condition, smooth, estimator)
    plt.show()


if __name__ == "__main__":
    """
        all_logdirs (string list): As many log directories (or prefixes to log 
            directories, which the plotter will autocomplete internally) as 
            you'd like to plot from.
        performance (string): 'reward' or 'success_rate'
        condition: Optional flag. By default, the plotter shows y-values which
            are averaged across all results that share an ``exp_name``, 
            which is typically a set of identical experiments that only vary
            in random seed. But if you'd like to see all of those curves 
            separately, use the ``--condition`` flag.
        smooth (int): Smooth data by averaging it over a fixed window. This 
            parameter says how wide the averaging window will be.
        select (strings): Optional selection rule: the plotter will only show
            curves from logdirs that contain all of these substrings.
        exclude (strings): Optional exclusion rule: plotter will only show 
            curves from logdirs that do not contain these substrings.
    """

    make_plots(all_logdirs=["/mnt/c/Users/33136/Documents/mydocuments/data/assemble"],  
               performance='reward',
               condition='Condition2', 
               smooth=1, 
               select=None, 
               exclude=None,
               estimator='mean')
