import sympy as sp
import matplotlib.pyplot as plt
import time

from economy import Economy
from symbols import qx, dy, sy, rp, rq, q_pv, q_wine

SAVE_PLOTS = True
SAVE_PREFIX = "plots/"
DO_EXAMPLE = False 
PLOTS = [
    "autarky",
    "relative",
    "trade"
]
CLOSEUP_RELATIVE = True
SHOW_GRAPHS = False

if DO_EXAMPLE:
    example = Economy(
        'Honolulu',  # name of the trading agent
        'pv', 'wine',  # name of goods (x, y)
        q_pv ** (1/2) * q_wine ** (1/2),  # utility
        sp.sqrt(q_pv ** 2 + q_wine ** 2),  # production_costs
        100,  # budget
    )
    
    autarky_plot = example.plot_autarky((0,200))
    if SHOW_GRAPHS: autarky_plot.show()

    utility_plot = sp.plotting.plot3d(example.utility, (qx, 0, 200), (dy, 0, 200), show=False)
    utility_plot.save('plots/example/utility.png')
    if SHOW_GRAPHS: utility_plot.show()

    production_costs_plot = sp.plotting.plot3d(example.production_costs, (qx, 0, 200), (sy, 0, 200), show=False)
    production_costs_plot.save('plots/example/production_costs.png')
    if SHOW_GRAPHS: production_costs_plot.show()
    
    exit()

eu = Economy(
    'EU',
    'pv', 'wine',
    q_pv ** (2/3) * q_wine ** (1/3),
    sp.sqrt((q_pv) ** 2 + q_wine ** 2),
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

if 'autarky' in PLOTS: 
    lim = (0, 210)
    eu_plot = eu.plot_autarky(lim)
    cn_plot = cn.plot_autarky(lim)

    if(SAVE_PLOTS != False):
        eu_plot.save(SAVE_PREFIX + "autarky/eu.png")
        cn_plot.save(SAVE_PREFIX + "autarky/cn.png")
    eu_plot.extend(cn_plot)
    if(SAVE_PLOTS != False): 
        eu_plot.save(SAVE_PREFIX + "autarky/joint.png")
    if SHOW_GRAPHS: eu_plot.show()

class Clock:
    def __init__(self): 
        self.clock = time.perf_counter()

    def tick(self, msg): 
        diff = time.perf_counter() - self.clock
        print(f'{msg}\nfinished in {diff:.4f}s\n')
        self.clock = time.perf_counter()
    
c = Clock()
world_relative_supply = (eu.supply_rp_implied_qx + cn.supply_rp_implied_qx) / (eu.supply_rp_implied_sy + cn.supply_rp_implied_sy)
c.tick(f'world relative supply =\n{world_relative_supply}')

world_relative_demand = (eu.demand_rp_implied_qx + cn.demand_rp_implied_qx) / (eu.demand_rp_implied_dy + cn.demand_rp_implied_dy)
c.tick(f'world relative demand =\n{world_relative_demand}')

world_equilibrium_rp = sp.nsolve(sp.Eq(world_relative_supply, world_relative_demand), 1)
c.tick(f'world trade equilibrium relative price: \n{world_equilibrium_rp}')

if 'relative' in PLOTS:
    lim = (0, 3)
    wrs_plot = sp.plotting.plot_parametric(world_relative_supply, rp, (rp, *lim), show=False, line_color='black', label='world RS')
    wrd_plot = sp.plotting.plot_parametric(world_relative_demand, rp, (rp, 0.2, lim[1]), show=False, line_color='black', label='world RD')
    eu_plot = eu.plot_relative(lim)
    cn_plot = cn.plot_relative(lim)
    if(SAVE_PLOTS != False):
        eu_plot.save(SAVE_PREFIX + "relative/eu.png")
        cn_plot.save(SAVE_PREFIX + "relative/cn.png")

    eu_plot.extend(cn_plot)
    eu_plot.extend(wrs_plot)
    eu_plot.extend(wrd_plot)
    if(SAVE_PLOTS != False):
        eu_plot.save(SAVE_PREFIX + "relative/joint.png")

    if CLOSEUP_RELATIVE: 
        eu_plot.ylim = (0, 2.0)
        eu_plot.save(SAVE_PREFIX + "relative/joint-closeup.png")
    if SHOW_GRAPHS: eu_plot.show()

if 'trade' in PLOTS:
    lim = (0, 210)
    eu_plot = eu.plot_trade(world_equilibrium_rp, lim)
    cn_plot = cn.plot_trade(world_equilibrium_rp, lim)

    if(SAVE_PLOTS != False):
        eu_plot.save(SAVE_PREFIX + "trade/eu.png")
        cn_plot.save(SAVE_PREFIX + "trade/cn.png")
    eu_plot.extend(cn_plot)
    if(SAVE_PLOTS != False):
        eu_plot.save(SAVE_PREFIX + "trade/joint.png")
    if SHOW_GRAPHS: eu_plot.show()
