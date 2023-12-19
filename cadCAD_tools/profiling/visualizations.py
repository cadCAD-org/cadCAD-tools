from tqdm.auto import tqdm # type: ignore
import pandas as pd # type: ignore
import plotly.express as px # type: ignore
import numpy as np


def visualize_elapsed_time_per_ts(df: pd.DataFrame, relative=False):
    indexes = ['simulation', 'run', 'timestep', 'substep']

    z_df = df.set_index(indexes)
    first_time = z_df.query(
        'timestep == 1 & substep == 1').reset_index([-1, -2]).run_time
    s = (z_df.run_time - first_time)
    s.name = 'time_since_start'

    z_df = z_df.join(s)
    s = z_df.groupby(indexes[:-1]).time_since_start.max()

    fig_df = s.reset_index()
    if relative is True:
        s = fig_df.groupby(indexes[:-2]).time_since_start.diff()
        s.name = 'psub_duration'
        fig_df = fig_df.join(s)

        y_col = 'psub_duration'
    else:
        y_col = 'time_since_start'
        
    fig = px.box(fig_df,
                x='timestep',
                y=y_col)

    return fig


def visualize_substep_impact(df: pd.DataFrame, relative=True, **kwargs):
    indexes = ['simulation', 'subset', 'run', 'timestep', 'substep']

    new_df = df.copy()
    new_df = new_df.assign(psub_time=np.nan).set_index(indexes)

    # Calculate the run time associated with PSUBs
    for ind, gg_df in tqdm(df.query('substep > 0').groupby(indexes[:-1])):
        g_df = gg_df.reset_index()
        N_rows = len(g_df)
        substep_rows = list(range(N_rows))[1:-1:2]

        for substep_row in substep_rows:
            t1 = g_df.run_time[substep_row - 1]
            t2 = g_df.run_time[substep_row + 1]
            dt = t2 - t1
            g_df.loc[substep_row, 'psub_time'] = dt
        g_df = g_df.set_index(indexes)
        new_df.loc[g_df.index, 'psub_time'] = g_df.psub_time

    fig_df = new_df.reset_index().dropna(subset=['psub_time'])


    if 'substep_label' in fig_df.columns:
        x_col = 'substep_label'
    else:
        x_col = 'substep'
        fig_df[x_col] = fig_df[x_col] / 2

    if relative is True:
        time_per_psub = fig_df.groupby(indexes[:-1]).psub_time.apply(lambda x: x / x.sum())
        fig_df = fig_df.set_index(indexes).assign(relative_psub_time=time_per_psub.values).reset_index()
        y_col = 'relative_psub_time'
    else:
        y_col = 'psub_time'

    inds = fig_df[y_col] < fig_df[y_col].quantile(0.95)
    inds &= fig_df[y_col] > fig_df[y_col].quantile(0.05)

    fig = px.box(fig_df[inds],
                 x=x_col,
                 y=y_col,
                 **kwargs)
    
    if relative is True:
        fig.update_yaxes(tickformat=".1%")

    return fig
