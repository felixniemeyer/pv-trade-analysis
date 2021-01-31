import sympy as sp
import matplotlib.pyplot as plt

SAVE_PLOTS = False
SAVE_PREFIX = "plots/"
PLOT_AUTARKY = False
PLOT_RELATIVE = True

from economy import Economy

example = Economy(
    sp.S(1/2),
    sp.S(1/2),
    sp.S(1),
    sp.S(1),
    sp.S(100),
    "initial",
)

eu = Economy(
    sp.S(2),
    sp.S(1/2),
    sp.S(1),
    sp.S(1),
    sp.S(100),
    "EU",
    [0.1, 0.5, 0.8]
)

cn = Economy(
    sp.S(1/2),
    sp.S(1/2),
    sp.S(2/3),
    sp.S(3/2),
    sp.S(100),
    "CN",
    [0.8, 0.0, 0.1]
)

if PLOT_AUTARKY:
    eu = eu.plot_autarky()
    cn = cn.plot_autarky()
    if(SAVE_PLOTS != False):
        eu.save(SAVE_PREFIX + "autarky/eu.png")
        cn.save(SAVE_PREFIX + "autarky/cn.png")
    eu.extend(cn)
    if(SAVE_PLOTS != False):
        eu.save(SAVE_PREFIX + "autarky/joint.png")
    eu.show()

if PLOT_RELATIVE: 
    eu = eu.plot_relative()
    cn = cn.plot_relative()
    if(SAVE_PLOTS != False):
        eu.save(SAVE_PREFIX + "relative/eu.png")
        cn.save(SAVE_PREFIX + "relative/cn.png")
    eu.extend(cn)
    if(SAVE_PLOTS != False):
        eu.save(SAVE_PREFIX + "relative/joint.png")
    eu.show()