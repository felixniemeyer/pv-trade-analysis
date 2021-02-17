import sympy as sp
import matplotlib.pyplot as plt
import time
import os

from economy import Economy
from symbols import * #qx, dy, sy, rp, rq, q_pv, q_wine

q_pv = qx
q_wine = qy

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

def make_ellipsoid_ppf(max_pv, max_wine):
    general_ppf = sp.solve(
        sp.Eq(sp.sqrt((q_pv/max_pv) ** sp.Rational(2,1) + (q_wine/max_wine) ** sp.Rational(2,1)), 1),
        q_wine
    )[0]
    print(general_ppf)
    return general_ppf

if DO_EXAMPLE:
    save_dir = SAVE_PREFIX + "example/"
    if SAVE_PLOTS: os.makedirs(save_dir, exist_ok=True)
    example = Economy(
        'Honolulu',  # name of the trading agent
        'pv', 'wine',  # name of goods (x, y)
        q_pv ** sp.Rational(1,2) * q_wine ** (sp.Rational(1,2)),  # utility
        make_ellipsoid_ppf(170,170), # ppf
        [0.2, 0.2, 0.2] # color for plotting
    )
    
    autarky_plot = example.plot_autarky((0,200))
    if SHOW_GRAPHS: autarky_plot.show()

    utility_plot = sp.plotting.plot3d(example.utility, (qx, 0, 200), (dy, 0, 200), show=False)
    utility_plot.save(save_dir+'utility.png')
    if SHOW_GRAPHS: utility_plot.show()

    production_costs_plot = sp.plotting.plot(example.ppf, (qx, 0, 200), show=False)
    production_costs_plot.save(save_dir + 'ppf.png')
    if SHOW_GRAPHS: production_costs_plot.show()
    
    exit()
    
eu = Economy(
    'EU',
    'pv', 'wine',
    q_pv ** sp.Rational(1, 2) * q_wine ** sp.Rational(1, 2),
    make_ellipsoid_ppf(100,100),
    [0.1, 0.5, 0.8]
)

cn = Economy(
    'CN',
    'pv', 'wine',
    q_pv ** sp.Rational(1, 2) * q_wine ** sp.Rational(1, 2),
    make_ellipsoid_ppf(200,100),
    [0.8, 0.0, 0.1]
)

lim = (0, 210) # set the area that should be plotted

if 'autarky' in PLOTS: 
    save_dir = SAVE_PREFIX + 'autarky/'
    if SAVE_PLOTS: os.makedirs(save_dir, exist_ok=True)
    eu_plot = eu.plot_autarky(lim)
    cn_plot = cn.plot_autarky(lim)

    if(SAVE_PLOTS != False):
        eu_plot.save(save_dir + "eu.png")
        cn_plot.save(save_dir + "cn.png")
    eu_plot.extend(cn_plot)
    if(SAVE_PLOTS != False): 
        eu_plot.save(save_dir + "joint.png")
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

world_equilibrium_rq = sp.N(world_relative_supply.subs({rp: world_equilibrium_rp}))
c.tick(f'world trade equilibrium relative quantity: \n{world_equilibrium_rq}')

if 'relative' in PLOTS:
    save_dir = SAVE_PREFIX + 'relative/'
    if SAVE_PLOTS: os.makedirs(save_dir, exist_ok=True)

    limx = (0, float(2.3 * world_equilibrium_rq))
    limy = (0, float(2.3 * world_equilibrium_rp))
    wrs_plot = sp.plotting.plot_parametric(world_relative_supply, rp, (rp, *limy), show=False, line_color='black', label='world RS')
    wrd_plot = sp.plotting.plot_parametric(world_relative_demand, rp, (rp, 0.2, limy[1]), show=False, line_color='black', label='world RD')
    eu_plot = eu.plot_relative(limx, limy)
    cn_plot = cn.plot_relative(limx, limy)
    if(SAVE_PLOTS != False):
        eu_plot.save(save_dir + "eu.png")
        cn_plot.save(save_dir + "cn.png")

    eu_plot.extend(cn_plot)
    eu_plot.extend(wrs_plot)
    eu_plot.extend(wrd_plot)
    if(SAVE_PLOTS != False):
        eu_plot.save(save_dir + "joint.png")

    if SHOW_GRAPHS: eu_plot.show()

if 'trade' in PLOTS:
    save_dir = SAVE_PREFIX + 'trade/'
    if SAVE_PLOTS: os.makedirs(save_dir, exist_ok=True)

    eu_plot = eu.plot_trade(world_equilibrium_rp, lim)
    cn_plot = cn.plot_trade(world_equilibrium_rp, lim)

    if(SAVE_PLOTS != False):
        eu_plot.save(save_dir + "eu.png")
        cn_plot.save(save_dir + "cn.png")
    eu_plot.extend(cn_plot)
    if(SAVE_PLOTS != False):
        eu_plot.save(save_dir + "joint.png")
    if SHOW_GRAPHS: eu_plot.show()
