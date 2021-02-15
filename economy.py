import sympy as sp
import colorsys

from symbols import qx, qy, sy, dy, max_utility, rp, rq

class Economy:
    def __init__(
        self,
        name,
        product_x, product_y,
        utility_function,
        production_costs_function,
        budget,
        rgb=(0, 0, 0)
    ):
        self.name = name
        self.product_x = product_x
        self.product_y = product_y
        self.rgb = rgb

        # ppf, indifference curve, price line
        self.utility = utility_function.subs({qy: dy})
        self.production_costs = production_costs_function.subs({qy: sy})

        self.ppf = sp.solve(sp.Eq(self.production_costs, budget), sy)[0]

        self.general_indifference_curve = sp.solve(
            sp.Eq(self.utility, max_utility), dy)[0]

        self.supply_price_ratio = sp.diff(self.ppf, qx)

        self.ppf_utility = self.utility.subs({dy: self.ppf})
        self.ppf_utility_d = sp.diff(self.ppf_utility, qx)

        self.optimum = sp.solve([
            self.ppf_utility_d,
            sp.Eq(self.ppf, self.general_indifference_curve)
        ],
            (qx, max_utility)
        )

        (self.qpv, self.mu) = self.optimum[0]

        self.indifference_curve = self.general_indifference_curve.subs(
            {max_utility: self.mu})

        self.price_line = self.supply_price_ratio.subs(
            {qx: self.qpv}) * (qx - self.qpv) + self.ppf.subs({qx: self.qpv})


        self.rq_implied_supply = sp.solve([
            sp.Eq(rq, qx / sy),
            sp.Eq(self.ppf, sy)
        ], (qx, sy))[0]
        self.relative_supply = - \
            self.supply_price_ratio.subs({qx: self.rq_implied_supply[0]})

        self.demand_price_ratio = sp.diff(self.indifference_curve, qx)
        self.rq_implied_demand = sp.solve([
            sp.Eq(rq, qx / dy),
            sp.Eq(self.indifference_curve, dy)
        ], (qx, dy))[0]
        self.relative_demand = - \
            self.demand_price_ratio.subs({qx: self.rq_implied_demand[0]})

        self.rp_implied_qx = sp.solve(
            self.supply_price_ratio + rp,  # rp is stated positive, the actual slope is negative
            qx
        )[0]

        self.rp_implied_sy = self.ppf.subs({qx: self.rp_implied_qx})

        self.demand_rp_implied_qx = sp.solve(
            self.demand_price_ratio + rp,
            qx
        )[0]

        self.demand_rp_implied_dy = self.indifference_curve.subs(
            {qx: self.demand_rp_implied_qx})

    # plotting
    def color_gen(self, rgb, difference=1.2):
        while True:
            yield rgb
            (h, l, s) = colorsys.rgb_to_hls(*rgb)
            rgb = colorsys.hls_to_rgb(
                (h + (difference-1.0) * 0.1) % 1, max(0, min(1, difference * l)), s)
            
    def brighten_color(self, rgb):
        (h, l, s) = colorsys.rgb_to_hls(*rgb)
        return colorsys.hls_to_rgb(
            h, 1 - (1 - l) * 0.33, s)
            
    def plot_autarky(self, lim=(0, 1)):
        # draw price lines only around the tanget spot
        price_line_length_per_x = (sp.N(self.supply_price_ratio.subs(
            {qx: self.qpv})) ** 2 + 1) ** 0.5
        price_line_xrange = lim[1] / 3 / price_line_length_per_x
        price_line_range = (qx, self.qpv - price_line_xrange,
                            self.qpv + price_line_xrange)

        color = self.color_gen(self.rgb)

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
        color = self.color_gen(self.rgb, 1.6)
        relative_plot = sp.plotting.plot(self.relative_supply, (rq, *lim),
                                         label=self.name + " RS " + self.product_x, show=False, line_color=next(color))
        further_plots = [
            sp.plotting.plot(self.relative_demand, (rq, *lim),
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

    def plot_trade(self, price_ratio, lim=(0, 1)):
        qx_under_trade = sp.solve(
            sp.Eq(self.supply_price_ratio, - price_ratio),
            qx
        )[0]
        qy_under_trade = self.ppf.subs({qx: qx_under_trade})

        trade_line = - price_ratio * (qx - qx_under_trade) + qy_under_trade
        
        # look for qy and utility 
        trade_optimum = sp.solve([
            sp.Eq(self.general_indifference_curve, trade_line), 
            sp.diff(self.general_indifference_curve, qx) + price_ratio, # negate price ratio
        ], (qx, max_utility))[0]
        
        trade_indifference_line = self.general_indifference_curve.subs({
            max_utility: trade_optimum[1]
        })
        

        color = self.color_gen(self.rgb)

        impx, impy = sp.symbols(['impx', 'impy'])
        
        # values for trade triangle
        (l, r) = (qx_under_trade, trade_optimum[0]) if qx_under_trade < trade_optimum[0] else (trade_optimum[0], qx_under_trade)
        bottom = sp.N(trade_line.subs({qx: r}))
        print(f"{self.name} trade {self.product_x} = {r - l}")

        # trade_plot = self.plot_autarky(lim)
        trade_plot = sp.plotting.plot(self.ppf, (qx, *lim), show=False,
                                      label=self.name + " ppf", line_color=next(color))
        further_plots = [
            sp.plotting.plot(trade_line, (qx, *lim), show=False,
                             label=self.name + " trade price line", line_color=next(color)),
            sp.plotting.plot(trade_indifference_line, (qx, trade_optimum[0] - lim[1]/5, trade_optimum[0] + lim[1]/5), show=False,
                                         label=self.name + " trade indifference curve", line_color=next(color)),
            sp.plotting.plot_implicit(sp.And(impx >= l, impx <= r, impy >= bottom, impy <= trade_line.subs({qx: impx})), x_var=(impx, *lim), y_var=(impy, *lim), show=False, line_color=self.brighten_color(self.rgb))
        ]
        
        for g in further_plots:
            trade_plot.extend(g)

        trade_plot.xlim = lim
        trade_plot.ylim = lim
        trade_plot.xlabel = "Q_" + self.product_x
        trade_plot.ylabel = "Q_" + self.product_y
        trade_plot.legend = True

        return trade_plot
