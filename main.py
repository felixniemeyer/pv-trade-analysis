import sympy as sp
import matplotlib.pyplot as plt

from economy import Economy

SAVE_PLOTS = True
SAVE_PREFIX = "plots/"
PLOT_AUTARKY = True
PLOT_RELATIVE = True
DO_EXAMPLE = False

(q_pv, q_wine) = sp.symbols(['qx', 'qy'], positive=True)

if DO_EXAMPLE:
    example = Economy(
        'Honolulu',  # name of the trading agent
        'pv', 'wine',  # name of goods
        q_pv ** (1/2) * q_wine ** (1/2),  # utility
        sp.sqrt(q_pv ** 2 + q_wine ** 2),  # production_cost
        100,  # budget
    )
    example.plot_autarky().show()

eu = Economy(
    'EU',  
    'pv', 'wine',  
    q_pv ** (2) * q_wine ** (1/2),  
    sp.sqrt(q_pv ** 2 + q_wine ** 2),  
    100,  
    [0.1, 0.5, 0.8]
)

cn = Economy(
    'CN',  
    'pv', 'wine',  
    q_pv ** (1/2) * q_wine ** (1/2),  
    sp.sqrt((q_pv/2) ** 2 + (q_wine) ** 2), 
    100,  
    [0.8, 0.0, 0.1]
)

if PLOT_AUTARKY:
    lim = (0, 200)
    eu_plot = eu.plot_autarky(lim)
    cn_plot = cn.plot_autarky(lim)
    if(SAVE_PLOTS != False):
        eu_plot.save(SAVE_PREFIX + "autarky/eu.png")
        cn_plot.save(SAVE_PREFIX + "autarky/cn.png")
    eu_plot.extend(cn_plot)
    if(SAVE_PLOTS != False):
        eu_plot.save(SAVE_PREFIX + "autarky/joint.png")
    eu_plot.show()

if PLOT_RELATIVE:
    lim = (0, 6)
    eu_plot = eu.plot_relative(lim)
    cn_plot = cn.plot_relative(lim)
    if(SAVE_PLOTS != False):
        eu_plot.save(SAVE_PREFIX + "relative/eu.png")
        cn_plot.save(SAVE_PREFIX + "relative/cn.png")
    eu_plot.extend(cn_plot)
    if(SAVE_PLOTS != False):
        eu_plot.save(SAVE_PREFIX + "relative/joint.png")
    eu_plot.show()
