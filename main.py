import sympy as sp
import matplotlib.pyplot as plt

from economy import Economy 
from symbols import qx, dy, sy, rp, rq, q_pv, q_wine

SAVE_PLOTS = True
SAVE_PREFIX = "plots/"
DO_EXAMPLE = False 
TRY_INVERSE_WORLD_RD = True
PLOTS = [
#    "autarky",
#    "relative",
    "trade"
]
SKIP_TOT_CALCULATION = False
CLOSEUP_RELATIVE = True

if DO_EXAMPLE:
    example = Economy(
        'Honolulu',  # name of the trading agent
        'pv', 'wine',  # name of goods (x, y)
        q_pv ** (1/2) * q_wine ** (1/2),  # utility
        sp.sqrt(q_pv ** 2 + q_wine ** 2),  # production_costs
        100,  # budget
    )
    
    example.plot_autarky((0,200)).show()

    utility_plot = sp.plotting.plot3d(example.utility, (qx, 0, 200), (dy, 0, 200), show=False)
    utility_plot.save('plots/example/utility.png')
    utility_plot.show()

    production_costs_plot = sp.plotting.plot3d(example.production_costs, (qx, 0, 200), (sy, 0, 200), show=False)
    production_costs_plot.save('plots/example/production_costs.png')
    production_costs_plot.show()
    
    exit()

eu = Economy(
    'EU',
    'pv', 'wine',
    q_pv ** (2/3) * q_wine ** (1/3),
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
    eu_plot.show()

# world RS
world_relative_supply = sp.simplify(
    (eu.rp_implied_qx + cn.rp_implied_qx) / (eu.rp_implied_sy + cn.rp_implied_sy))
world_relative_supply_price = sp.solve(
    sp.Eq(rq, world_relative_supply), 
    rp
)[0]

print(sp.latex(world_relative_supply_price))

if SKIP_TOT_CALCULATION: 
    world_equi_rp = 0.8
else: 
    world_relative_demand = sp.simplify(
        (eu.demand_rp_implied_qx + cn.demand_rp_implied_qx) / (eu.demand_rp_implied_dy + cn.demand_rp_implied_dy))

    world_equi_rp = sp.nsolve(sp.Eq(world_relative_supply, world_relative_demand), 1)
    print(f'world trade equilibrium relative price: {world_equi_rp}')

if 'relative' in PLOTS:
    lim = (0, 3)
    wrp_plot = sp.plotting.plot(
        world_relative_supply_price, (rq, *lim), show=False, line_color='black', label='world RS')
    if TRY_INVERSE_WORLD_RD:
        try:
            print('w rd', world_relative_demand)
            world_relative_demand_price = sp.solve(
                rq - world_relative_demand,
                rp
            )[0]
            print(world_relative_demand_price)
            wrp_plot.extend(
                sp.plotting.plot(world_relative_demand_price, (rq, *lim),
                                 show=False, line_color='grey', label='world RD')
            )
            print("it worked! wow, can plot world relative demand")
        except:
            print("well, we tried to inverse world relative demand, but honestly: findin the inverse for " +
              str(world_relative_demand) + " was just too complicated :/ ... for now ...")
    eu_plot = eu.plot_relative(lim)
    cn_plot = cn.plot_relative(lim)

    if(SAVE_PLOTS != False):
        eu_plot.save(SAVE_PREFIX + "relative/eu.png")
        cn_plot.save(SAVE_PREFIX + "relative/cn.png")
    eu_plot.extend(cn_plot)
    eu_plot.extend(wrp_plot)
    if(SAVE_PLOTS != False):
        eu_plot.save(SAVE_PREFIX + "relative/joint.png")
    if CLOSEUP_RELATIVE: 
        eu_plot.ylim = (0, 2.0)
        eu_plot.save(SAVE_PREFIX + "relative/joint-closeup.png")
    eu_plot.show()

if 'trade' in PLOTS:
    lim = (0, 210)
    eu_plot = eu.plot_trade(world_equi_rp, lim)
    cn_plot = cn.plot_trade(world_equi_rp, lim)

    if(SAVE_PLOTS != False):
        eu_plot.save(SAVE_PREFIX + "trade/eu.png")
        cn_plot.save(SAVE_PREFIX + "trade/cn.png")
    eu_plot.extend(cn_plot)
    if(SAVE_PLOTS != False):
        eu_plot.save(SAVE_PREFIX + "trade/joint.png")
    eu_plot.show()
