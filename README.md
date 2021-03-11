# cadCAD-tools

Tools for improving the cadCAD user experience. This library contains
wrappers for executing simulations easily as well as tools for profiling and
typing.

## How to use

The best way is by looking into the example notebooks on the `notebooks/` folder


## Setup

Just use pip.

`python -m pip install cadCAD-tools`

## Features

### Easy execution of cadCAD models

Easy enough:

```python
from cadCAD_tools import easy_run

df = easy_run(initial_conditions,
              params,
              partial_state_update_blocks,
              TIMESTEPS,
              SAMPLES,
              use_labels=True,
              assign_params=True,
              drop_substeps=False)
```
### cadCAD specific types


```python
from cadCAD_tools.types import StateVariable, Parameter, StateUpdateBlock

```

### Profiling tools & visualizations

cadCAD-tools includes wrappers for automatically decorating the PSUBs
with time measuring functions. Through the usage of metadata, it is possible
to obtain a clear view of what SUBs are being more expensive.

```python
from cadCAD_tools import profile_run

df = profile_run(initial_conditions,
              params,
              partial_state_update_blocks,
              TIMESTEPS,
              SAMPLES,
              use_labels=True,
              assign_params=True)
```

```python
from cadCAD_tools.profiling.visualizations import visualize_substep_impact

visualize_substep_impact(df, relative=True)
```

![](https://i.imgur.com/50BUEA7.png)


```python
from cadCAD_tools.profiling.visualizations import visualize_elapsed_time_per_ts

visualize_elapsed_time_per_ts(df, relative=False)
```

![](https://i.imgur.com/pOBsQoL.png)
