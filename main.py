import sympy as sp
import matplotlib.pyplot as plt

from economy import Economy

SAVE_PLOTS = True
SAVE_PREFIX = "plots/"
PLOT_AUTARKY = False
PLOT_RELATIVE = True

(q_pv, q_wine) = sp.symbols(['qx', 'qy'])

example = Economy(
    'Honolulu', # name of the trading agent
    'pv', 'wine', # name of goods 
    q_pv** (1/2) * q_wine ** (1/2), # utility 
    sp.sqrt(q_pv ** 2 + q_wine ** 2), # production_cost
    100, # budget
)

example.plot_autarky().show()

# eu = Economy(
#     sp.S(2),
#     sp.S(1/2),
#     sp.S(1),
#     sp.S(1),
#     sp.S(100),
#     "EU",
#     [0.1, 0.5, 0.8]
# )
# 
# cn = Economy(
#     sp.S(1/2),
#     sp.S(1/2),
#     sp.S(2/3),
#     sp.S(3/2),
#     sp.S(100),
#     "CN",
#     [0.8, 0.0, 0.1]
# )
# 
# if PLOT_AUTARKY:
#     eu_plot = eu.plot_autarky()
#     cn_plot = cn.plot_autarky()
#     if(SAVE_PLOTS != False):
#         eu_plot.save(SAVE_PREFIX + "autarky/eu.png")
#         cn_plot.save(SAVE_PREFIX + "autarky/cn.png")
#     eu_plot.extend(cn_plot)
#     if(SAVE_PLOTS != False):
#         eu_plot.save(SAVE_PREFIX + "autarky/joint.png")
#     eu_plot.show()
#     
# if PLOT_RELATIVE: 
#     eu_plot = eu.plot_relative()
#     cn_plot = cn.plot_relative()
#     if(SAVE_PLOTS != False):
#         eu_plot.save(SAVE_PREFIX + "relative/eu.png")
#         cn_plot.save(SAVE_PREFIX + "relative/cn.png")
#     eu_plot.extend(cn_plot)
#     if(SAVE_PLOTS != False):
#         eu_plot.save(SAVE_PREFIX + "relative/joint.png")
#     eu_plot.show()
# 