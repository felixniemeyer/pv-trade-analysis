import sympy as sp

import colorsys

def color_gen(rgb, stepfactor=1.2):
    while True:
        yield rgb
        (h, l, s) = colorsys.rgb_to_hls(*rgb)
        rgb = colorsys.hls_to_rgb((h+0.01) % 1, max(0, min(1, stepfactor * l)), s)

class Economy: 
    def __init__(
        self,
        u_pv_exponent,
        u_wine_exponent,
        p_pv_coefficient,
        p_wine_coefficient,
        budget,
        country_code,
        rgb=(0, 0, 0)
    ):
        self.rgb = rgb
        self.country_code = country_code

        # symbols
        self.Q_pv = sp.symbols('Q_pv', positive=True) # consumed or produced quantity of solar panels
        self.PQ_wine = sp.symbols('PQ_wine', positive=True)  # produced quantity of wine
        self.CQ_wine = sp.symbols('CQ_wine', positive=True)  # consumed quantity of wine
        self.max_utility = sp.symbols('max_utility', positive=True) # max utility that can be reached for a given budget

        # ppf, indifference curve, price line
        self.utility = self.Q_pv**u_pv_exponent * self.CQ_wine**u_wine_exponent

        self.production_cost = sp.sqrt((self.Q_pv*p_pv_coefficient)
                                  ** 2 + (self.PQ_wine*p_wine_coefficient)**2)

        self.ppf = sp.solve(sp.Eq(self.production_cost, budget), self.PQ_wine)[0]

        self.general_indifference_curve = sp.solve(
            sp.Eq(self.utility, self.max_utility), self.CQ_wine)[0]

        self.supply_price_ratio = sp.diff(self.ppf, self.Q_pv)

        self.ppf_utility = self.utility.subs({self.CQ_wine: self.ppf})
        self.ppf_utility_d = sp.diff(self.ppf_utility, self.Q_pv)

        self.optimum = sp.solve([
            self.ppf_utility_d,
            sp.Eq(self.ppf, self.general_indifference_curve)
        ],
            (self.max_utility, self.Q_pv)
        )

        (self.mu, self.qpv) = self.optimum[0]

        self.indifference_curve = self.general_indifference_curve.subs({self.max_utility: self.mu})

        self.price_line = self.supply_price_ratio.subs({self.Q_pv: self.qpv}) * (self.Q_pv - self.qpv) + self.ppf.subs({self.Q_pv: self.qpv})

        # RS and RD 
        self.Q_ratio = sp.symbols('Q_ratio', positive=True) # quantity ratio Q_pv / Q_wine
        
        self.implied_supply_Q_pv = sp.solve([
            sp.Eq(self.Q_ratio, self.Q_pv / self.PQ_wine),
            sp.Eq(self.ppf, self.PQ_wine)
        ], (self.Q_pv, self.PQ_wine))[0][0]
        self.relative_supply = -self.supply_price_ratio.subs({self.Q_pv: self.implied_supply_Q_pv})
        
        self.demand_price_ratio = sp.diff(self.indifference_curve, self.Q_pv)
        self.implied_demand_Q_pv = sp.solve([
            sp.Eq(self.Q_ratio, self.Q_pv / self.CQ_wine),
            sp.Eq(self.indifference_curve, self.CQ_wine)
        ], (self.Q_pv, self.CQ_wine))[0][0]
        self.relative_demand = -self.demand_price_ratio.subs({self.Q_pv: self.implied_demand_Q_pv})

    def plot_autarky(self): 
        f = (sp.N(self.supply_price_ratio.subs({self.Q_pv: self.qpv})) ** 2 + 1) ** -0.5
        price_line_xrange = 50 * f
        price_line_range = (self.Q_pv, self.qpv - price_line_xrange, self.qpv + price_line_xrange)

        color = color_gen(self.rgb)

        autarky_plot = sp.plotting.plot(self.ppf, (self.Q_pv, 0, 150), show=False,
                                label=self.country_code + " ppf", line_color=next(color))
        further_plots = [
            sp.plotting.plot(self.indifference_curve, (
                self.Q_pv, 0, 150), show=False, label=self.country_code + " indifference curve", line_color=next(color)),
            sp.plotting.plot(self.price_line, price_line_range, show=False,
                             label=self.country_code + " price line", line_color=next(color)),
        ]
        for g in further_plots:
            autarky_plot.extend(g)
        autarky_plot.xlim = (0, 160)
        autarky_plot.ylim = (0, 160)
        autarky_plot.xlabel = "Q_PV"
        autarky_plot.ylabel = "Q_wine"
        autarky_plot.legend = True
        # plot.title = title + "(autarky)"
                
        return autarky_plot
    
    def plot_relative(self): 
        print(self.implied_supply_Q_pv)
        print(self.implied_demand_Q_pv)
        
        plot_range = (0, 6)
        color = color_gen(self.rgb)
        relative_plot = sp.plotting.plot(self.relative_supply, (self.Q_ratio, *plot_range), label=self.country_code + " RS", show=False, line_color=next(color))
        further_plots = [
            sp.plotting.plot(self.relative_demand, (self.Q_ratio, *plot_range), label=self.country_code + " RD", show=False, line_color=next(color))
        ]
        for p in further_plots: 
            relative_plot.extend(p)
        relative_plot.xlim = plot_range
        relative_plot.ylim = plot_range
        relative_plot.legend = True

        # relative_supply = sp.solve([
        #     sp.Eq(Q_ratio, Q_pv / PQ_wine),
        #     ppf,
        # ])
        # relative demand

        return relative_plot