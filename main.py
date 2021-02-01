import sympy as sp
import matplotlib.pyplot as plt

from economy import Economy

SAVE_PLOTS = True
SAVE_PREFIX = "plots/"
PLOTS = [
    "autarky", 
    "relative", 
    "trade"
]
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

for plot in PLOTS: 
    eu_plot = None
    cn_plot = None
    if plot == 'autarky':
        lim = (0, 210)
        eu_plot = eu.plot_autarky(lim)
        cn_plot = cn.plot_autarky(lim)
    if plot == 'relative':
        lim = (0, 6)
        rq = sp.symbols('rq', positive=True, real=True) # relative quantity
        rp = sp.symbols('rp', positive=True, real=True) # relative price 
        # world RS
        world_relative_supply = sp.simplify((eu.rp_implied_qx + cn.rp_implied_qx) / (eu.rp_implied_sy + cn.rp_implied_sy))
        world_relative_supply_price = sp.solve(
            rq - world_relative_supply,
            rp
        )[0]
        wrp_plot = sp.plotting.plot(world_relative_supply_price, (rq, *lim), show=False, line_color='black', label='world RS')
        # world RD
        try: 
            world_relative_demand = sp.simplify((eu.demand_rp_implied_qx + cn.demand_rp_implied_qx) / (eu.demand_rp_implied_dy + cn.demand_rp_implied_dy))
            print('w rd', world_relative_demand)
            world_relative_demand_price = sp.solve(
                rq - world_relative_demand,
                rp
            )[0]
            print(world_relative_demand_price)
            wrp_plot.extend(
                sp.plotting.plot(world_relative_demand_price, (rq, *lim), show=False, line_color='grey', label='world RD')   
            ) 
        except:
            print("well, we tried, but honestly: findin the inverse for " + str(world_relative_demand) + " was just too complicated :/")
        eu_plot = eu.plot_relative(lim)
        cn_plot = cn.plot_relative(lim)

    if plot == 'trade':
        lim = (0, 210)
        eu_plot = eu.plot_trade(0.5, lim)
        cn_plot = cn.plot_trade(0.5, lim)

    if eu_plot != None and cn_plot != None:
        if(SAVE_PLOTS != False):
            eu_plot.save(SAVE_PREFIX + plot + "/eu.png")
            cn_plot.save(SAVE_PREFIX + plot + "/cn.png")
        eu_plot.extend(cn_plot)
        if plot == 'relative': 
            eu_plot.extend(wrp_plot)
        if(SAVE_PLOTS != False):
            eu_plot.save(SAVE_PREFIX + plot + "/joint.png")
        eu_plot.show()

            