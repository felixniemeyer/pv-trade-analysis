import sympy as sp

import colorsys


def color_gen(rgb, difference=1.2):
    while True:
        yield rgb
        (h, l, s) = colorsys.rgb_to_hls(*rgb)
        rgb = colorsys.hls_to_rgb(
            (h + (difference-1.0) * 0.1) % 1, max(0, min(1, difference * l)), s)


class Economy:
    def __init__(
        self,
        name,
        product_x, product_y,
        utility_function,
        production_cost_function,
        budget,
        rgb=(0, 0, 0)
    ):
        self.name = name
        self.product_x = product_x
        self.product_y = product_y
        self.rgb = rgb

        # symbols
        qx = sp.symbols('qx', positive=True)  # quantity of good x
        qy = sp.symbols('qy', positive=True)  # quantity of good x
        sq = sp.symbols('sy', positive=True)  # supply of good y
        dq = sp.symbols('dy', positive=True)  # demand of good y
        # max utility that can be reached for a given budget
        max_utility = sp.symbols('max_utility', positive=True)

        # ppf, indifference curve, price line
        self.utility = utility_function.subs({qy: dq})
        self.production_cost = production_cost_function.subs({qy: sq})

        self.ppf = sp.solve(sp.Eq(self.production_cost, budget), sq)[0]

        self.general_indifference_curve = sp.solve(
            sp.Eq(self.utility, max_utility), dq)[0]

        self.supply_price_ratio = sp.diff(self.ppf, qx)

        self.ppf_utility = self.utility.subs({dq: self.ppf})
        self.ppf_utility_d = sp.diff(self.ppf_utility, qx)

        self.optimum = sp.solve([
            self.ppf_utility_d,
            sp.Eq(self.ppf, self.general_indifference_curve)
        ],
            (max_utility, qx)
        )

        (self.mu, self.qpv) = self.optimum[0]

        self.indifference_curve = self.general_indifference_curve.subs(
            {max_utility: self.mu})

        self.price_line = self.supply_price_ratio.subs(
            {qx: self.qpv}) * (qx - self.qpv) + self.ppf.subs({qx: self.qpv})

        # RS and RD of good x
        # the following works only if supply is convex and demand is concave

        q_ratio = sp.symbols('Q_ratio', positive=True)

        self.price_implied_supply = sp.solve([
            sp.Eq(q_ratio, qx / sq),
            sp.Eq(self.ppf, sq)
        ], (qx, sq))[0]
        self.relative_supply = - \
            self.supply_price_ratio.subs({qx: self.price_implied_supply[0]})

        self.price_implied_demand = sp.diff(self.indifference_curve, qx)
        self.implied_demand_Q_pv = sp.solve([
            sp.Eq(q_ratio, qx / dq),
            sp.Eq(self.indifference_curve, dq)
        ], (qx, dq))[0]
        self.relative_demand = - \
            self.price_implied_demand.subs({qx: self.implied_demand_Q_pv[0]})

    def plot_autarky(self, lim=(0, 1)):
        qx = sp.symbols('qx', positive=True)  # quantity of good x

        f = (sp.N(self.supply_price_ratio.subs(
            {qx: self.qpv})) ** 2 + 1) ** -0.5
        price_line_xrange = lim[1] / 3 * f
        price_line_range = (qx, self.qpv - price_line_xrange,
                            self.qpv + price_line_xrange)

        color = color_gen(self.rgb)

        autarky_plot = sp.plotting.plot(self.ppf, (qx, *lim), show=False,
                                        label=self.name + " ppf", line_color=next(color))
        further_plots = [
            sp.plotting.plot(self.indifference_curve, price_line_range, show=False,
                             label=self.name + " indifference curve", line_color=next(color)),
            sp.plotting.plot(self.price_line, price_line_range, show=False,
                             label=self.name + " price line", line_color=next(color)),
        ]
        for g in further_plots:
            autarky_plot.extend(g)

        autarky_plot.xlim = lim
        autarky_plot.ylim = lim
        autarky_plot.xlabel = "Q_" + self.product_x
        autarky_plot.ylabel = "Q_" + self.product_y
        autarky_plot.legend = True
        # plot.title = title + "(autarky)"

        return autarky_plot

    def plot_relative(self, lim=(0, 6)):
        q_ratio = sp.symbols('Q_ratio', positive=True)

        color = color_gen(self.rgb, 1.6)
        relative_plot = sp.plotting.plot(self.relative_supply, (q_ratio, *lim),
                                         label=self.name + " RS " + self.product_x, show=False, line_color=next(color))
        further_plots = [
            sp.plotting.plot(self.relative_demand, (q_ratio, *lim),
                             label=self.name + " RD " + self.product_x, show=False, line_color=next(color))
        ]
        for p in further_plots:
            relative_plot.extend(p)
        relative_plot.xlim = lim
        relative_plot.ylim = lim
        relative_plot.xlabel = "Q_" + self.product_x + " / Q_" + self.product_y
        relative_plot.ylabel = "p_" + self.product_x + " / p_" + self.product_y

        relative_plot.legend = True

        # relative_supply = sp.solve([
        #     sp.Eq(Q_ratio, Q_pv / PQ_wine),
        #     ppf,
        # ])
        # relative demand

        return relative_plot
