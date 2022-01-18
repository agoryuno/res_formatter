from copy import copy
from textwrap import wrap

from tabulate import tabulate

import pandas as pd
import numpy as np


def build_params_col(res, fp, linebreak, sep=None):

    params_vals = {name : f"{res.params[name]:.{fp}f}"
                   for name in res.params.index}
    if sep is not None:
        params_vals = {name : val.replace(".", sep)
                       for name, val in params_vals.items()}
    def pvalue(val):
        if val <= 0.01:
            return "***"
        if val <= 0.05:
            return "**"
        if val <= 0.1:
            return "*"
        return ""

    params_pvals = {name : pvalue(res.pvalues[name]) for name in res.pvalues.index}
    params_se = {name : f"({res.bse[name]:.3f})".replace(".", ",")
                 for name in res.pvalues.index}

    col = {k : f"{params_vals[k]}{params_pvals[k]}{linebreak}{params_se[k]}"
           for k in params_vals.keys()}
    col["$R^2$"] = f"{res.rsquared_adj:.2f}".replace(".", ",")
    col["Кол-во наблюдений"] = f"{int(res.nobs)}"
    col["AIC"] = f"{res.aic:.1f}".replace(".", ",")
    return col


def build_params_tab(res_list, par_names=None, name_map=None,
                     line_len=30, sep=None, fp=3,
                     **kwargs):
    """
    Returns a pandas dataframe containing formmated results.

    res_list:  an iterable containing statsmodels Results objects;
    par_names: an iterable containing names of exogenous variables
               contained in objects from res_list;
    name_map:  a dictionary with keys corresponding to elements in
               *par_names* and values containing strings to be used
               instead of variable names (any variables not in;
               *name_map* will be included in the resulting table as-is)
    line_len:  maximum number of characters per line in the variable
               description/name column (default 30);
    sep:       character to be used as decimal separator (default ".");
    fp:        number of digits after the decimal point (default 3).

    Additional keyword arguments:

    r2_name:   how to denote R squared (default "R^2");
    tablefmt:  one of formats supported by the tabulate library
               (see: https://pypi.org/project/tabulate/), 'plain' by default;
    linebreak: character to use to break up lines in multiline cells (default 
               is '\\n'). Use '<br>' as the value for this argument if you plan
               to display the resulting Dataframe in a Jupiter notebook*


    * - to display the resulting Dataframe in a Jupiter notebook you can do
        something like:

        '
        from IPython.display import Markdown

        df = build_params_tab(results, linebreak="<br>")
        display(Markdown(df.to_markdown(numalign="center")))
        '

    """

    if par_names is None:
        par_names = list({n for res in res_list
                          for n in res.params.index.to_list()})

    if name_map is not None:
        params_order = {n : i for i, n in enumerate(name_map.keys())}
        def _(par):
            if par in params_order:
                return params_order[par]
            return np.inf

        par_names = sorted(par_names, key=_)


    par_names += [kwargs.get('r2_name', "$R^2$"),
                  "No. observations"]
    if kwargs.get("aic"):
        par_names += ["AIC"]

    cols = [build_params_col(n, fp, kwargs.get('linebreak', '\n'), sep) 
            for n in res_list]
    pcols = [[] for col in cols]
    for name in par_names:
        for i, col in enumerate(cols):
            if name in col:
                pcols[i].append(col[name])
            else:
                pcols[i].append("-")
    if name_map is not None:
        new_names = [name_map.get(name, name) for name in par_names]
        par_names = new_names
    if line_len is not None:
        par_names = ["<br>".join(wrap(name, line_len))
                     for name in copy(par_names)]
    tab = pd.DataFrame({**{"params" : par_names},
                        **{f"m{i}" : pcols[i] for i in range(len(pcols))}
                       })
    tab = tab.set_index("params", drop=True)
    return tab
