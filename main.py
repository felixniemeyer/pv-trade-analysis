import sympy as sp
import matplotlib.pyplot as plt
import colorsys

SAVE_PLOTS = False
SAVE_PREFIX = "plots/"
PLOT_AUTARKY = False
PLOT_RELATIVE = True


def plot_autarky(
    u_pv_exponent,
    u_wine_exponent,
        p_pv_coefficient,
        p_wine_coefficient,
        budget,
        country_code,
        rgb=(0, 0, 0)
):
    # consumed or produced quantity of solar panels
    Q_pv = sp.symbols('Q_pv', positive=True)
    PQ_wine = sp.symbols('PQ_wine', positive=True)  # produced quantity of wine
    CQ_wine = sp.symbols('CQ_wine', positive=True)  # consumed quantity of wine
    # max utility that can be reached for a given budget
    max_utility = sp.symbols('max_utility', positive=True)

    utility = Q_pv**u_pv_exponent * CQ_wine**u_wine_exponent

    production_cost = sp.sqrt((Q_pv*p_pv_coefficient)
                              ** 2 + (PQ_wine*p_wine_coefficient)**2)

    ppf = sp.solve(sp.Eq(production_cost, budget), PQ_wine)[0]

    general_indifference_curve = sp.solve(
        sp.Eq(utility, max_utility), CQ_wine)[0]

    supply_price_ratio = sp.diff(ppf, Q_pv)

    ppf_utility = utility.subs({CQ_wine: ppf})
    ppf_utility_d = sp.diff(ppf_utility, Q_pv)

    optimum = sp.solve([
        ppf_utility_d,
        sp.Eq(ppf, general_indifference_curve)
    ],
        (max_utility, Q_pv)
    )

    (mu, qpv) = optimum[0]

    indifference_curve = general_indifference_curve.subs({max_utility: mu})

    price_line = supply_price_ratio.subs({Q_pv: qpv}) * (Q_pv - qpv) + ppf.subs({Q_pv: qpv})

    # plotting
    def color_gen(rgb, stepfactor=1.2):
        while True:
            yield rgb
            (h, l, s) = colorsys.rgb_to_hls(*rgb)
            rgb = colorsys.hls_to_rgb((h+0.01) % 1, max(0, min(1, stepfactor * l)), s)

    if PLOT_AUTARKY:
        f = (sp.N(supply_price_ratio.subs({Q_pv: qpv})) ** 2 + 1) ** -0.5
        price_line_xrange = 50 * f
        price_line_range = (Q_pv, qpv - price_line_xrange, qpv + price_line_xrange)

        color = color_gen(rgb)

        autarky_plot = sp.plotting.plot(ppf, (Q_pv, 0, 150), show=False,
                                label=country_code + " ppf", line_color=next(color))
        further_plots = [
            sp.plotting.plot(indifference_curve, (
                Q_pv, 0, 150), show=False, label=country_code + " indifference curve", line_color=next(color)),
            sp.plotting.plot(price_line, price_line_range, show=False,
                             label=country_code + " price line", line_color=next(color)),
        ]
        for g in further_plots:
            autarky_plot.extend(g)
        autarky_plot.xlim = (0, 160)
        autarky_plot.ylim = (0, 160)
        autarky_plot.xlabel = "Q_PV"
        autarky_plot.ylabel = "Q_wine"
        autarky_plot.legend = True
        # plot.title = title + "(autarky)"
        if(SAVE_PREFIX != False):
            autarky_plot.save(SAVE_PREFIX + "autarky/" +  country_code + ".png")
    else: 
        autarky_plot = None
            


    # Part Two: RS and RD on Q_pv / Q_wine
    # relative supply
    Q_ratio = sp.symbols('Q_ratio', positive=True) # quantity ratio Q_pv / Q_wine
    
    implied_supply_Q_pv = sp.solve([
        sp.Eq(Q_ratio, Q_pv / PQ_wine),
        sp.Eq(ppf, PQ_wine)
    ], (Q_pv, PQ_wine))[0][0]
    relative_supply = -supply_price_ratio.subs({Q_pv: implied_supply_Q_pv})
    
    demand_price_ratio = sp.diff(indifference_curve, Q_pv)
    implied_demand_Q_pv = sp.solve([
        sp.Eq(Q_ratio, Q_pv / CQ_wine),
        sp.Eq(indifference_curve, CQ_wine)
    ], (Q_pv, CQ_wine))[0][0]
    relative_demand = -demand_price_ratio.subs({Q_pv: implied_demand_Q_pv})
    
    print(implied_supply_Q_pv)
    print(implied_demand_Q_pv)
    
    if PLOT_RELATIVE: 
        plot_range = (0, 7)
        color = color_gen(rgb)
        relative_plot = sp.plotting.plot(relative_supply, (Q_ratio, *plot_range), label=country_code + " RS", show=False, line_color=next(color))
        further_plots = [
            sp.plotting.plot(relative_demand, (Q_ratio, *plot_range), label=country_code + " RD", show=False, line_color=next(color))
        ]
        for p in further_plots: 
            relative_plot.extend(p)
        relative_plot.xlim = plot_range
        relative_plot.ylim = plot_range
        relative_plot.legend = True
    else:
        relative_plot = None

    # relative_supply = sp.solve([
    #     sp.Eq(Q_ratio, Q_pv / PQ_wine),
    #     ppf,
    # ])
    # relative demand

    return ( autarky_plot, relative_plot )


plot_autarky(
    sp.S(1/2),
    sp.S(1/2),
    sp.S(1),
    sp.S(1),
    sp.S(100),
    "initial",
)

eu_plots = plot_autarky(
    sp.S(2),
    sp.S(1/2),
    sp.S(1),
    sp.S(1),
    sp.S(100),
    "EU",
    [0.1, 0.5, 0.8]
)

cn_plots = plot_autarky(
    sp.S(1/2),
    sp.S(1/2),
    sp.S(2/3),
    sp.S(3/2),
    sp.S(100),
    "CN",
    [0.8, 0.0, 0.1]
)

if PLOT_AUTARKY:
    eu_plots[0].extend(cn_plots[0])
    if(SAVE_PLOTS != False):
        eu_plots[0].save(SAVE_PREFIX + "autarky/joint.png")
    eu_plots[0].show()

if PLOT_RELATIVE: 
    eu_plots[1].extend(cn_plots[1])
    if(SAVE_PLOTS != False): 
        eu_plots[0].save(SAVE_PREFIX + "relative/joint.png")
    eu_plots[1].show()