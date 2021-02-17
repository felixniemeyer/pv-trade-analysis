import sympy as sp
import colorsys
import time

from symbols import *

def measure(func):
    def wrapper(*args, **kwargs): 
        print(f'starting calculation {func.__name__!r}')
        clockStart = time.perf_counter()
        val = func(*args, **kwargs)
        elapsedSeconds = time.perf_counter() - clockStart
        print(f'finished {func.__name__!r} in {elapsedSeconds:.4f} seconds \n')
        return val
    return wrapper

class Economy:
    def __init__(
        self,
        name,
        product_x, product_y,
        utility_function,
        ppf,
        rgb=(0, 0, 0)
    ):
        self.name = name
        self.product_x = product_x
        self.product_y = product_y
        self.rgb = rgb

        # ppf, indifference curve, price line
        self.utility = utility_function.subs({qy: dy})
        self.ppf = ppf

        # the following calculations rely on each other and need to be in order
        self.calc_ppf_slope()
        self.calc_autarky_optimum() 
        self.calc_indifference_curve()
        self.calc_relative_supply()
        self.calc_relative_demand()
        self.calc_relative_price_implied_quantities()

    @measure
    def calc_ppf_slope(self): 
        self.ppf_slope = sp.diff(self.ppf, qx)

    @measure
    def calc_autarky_optimum(self): 
        self.ppf_utility = self.utility.subs({dy: self.ppf})
        print(f"ppf_utility =\n{self.ppf_utility}")
        self.ppf_utility_slope = sp.diff(self.ppf_utility, qx)
        print(f"ppf_utility =\n{self.ppf_utility_slope}")
        self.autarky_qx = sp.solve(
            self.ppf_utility_slope, 
            qx
        )[0]
        self.autarky_qy = self.ppf.subs({qx: self.autarky_qx})
        print(f"autarky optimal quantities: qx, qy =\n{self.autarky_qx}, {self.autarky_qy}")
        self.autarky_price_line = self.ppf_slope.subs(
            {qx: self.autarky_qx}) * (qx - self.autarky_qx) + self.ppf.subs({qx: self.autarky_qx})
        self.autarky_max_utility = self.utility.subs({
            qx: self.autarky_qx, 
            dy: self.autarky_qy
        })
        
    @measure
    def calc_indifference_curve(self): 
        self.general_indifference_curve = sp.solve(
            sp.Eq(self.utility, max_utility), dy)[0]

        self.indifference_curve = self.general_indifference_curve.subs(
            {max_utility: self.autarky_max_utility})
        print("indifference curve =\n", self.indifference_curve)


    @measure
    def calc_relative_supply(self): 
        self.rq_implied_supply = sp.solve([
            sp.Eq(rq, qx / self.ppf)
        ], qx)[0][0]
        print("rq implied supply =\n", self.rq_implied_supply)
        self.relative_supply = - \
            self.ppf_slope.subs({qx: self.rq_implied_supply})
        print("relative supply =\n", self.relative_supply)
        
    @measure 
    def calc_relative_demand(self): 
        self.indifference_curve_slope = sp.diff(self.indifference_curve, qx)
        self.rq_implied_demand = sp.solve([
            sp.Eq(rq, qx / self.indifference_curve)
        ], qx)[0][0]
        print("rq implied demand =\n", self.rq_implied_demand)
        self.relative_demand = - \
            self.indifference_curve_slope.subs({qx: self.rq_implied_demand})
        print("relative demand =\n", self.relative_demand) 
        
    @measure
    def calc_relative_price_implied_quantities(self): 
        self.supply_rp_implied_qx = sp.solve(
            sp.Eq(self.ppf_slope, - rp),  
            qx
        )[0]
        print("supply relative price implied qx =\n", self.supply_rp_implied_qx)
        self.supply_rp_implied_sy = self.ppf.subs({qx: self.supply_rp_implied_qx})
        print("supply relative price implied sy =\n", self.supply_rp_implied_sy)

        self.demand_rp_implied_qx = sp.solve(
            sp.Eq(self.indifference_curve_slope, - rp), 
            qx
        )[0]
        print("demand relative price implied qx =\n", self.demand_rp_implied_qx)
        self.demand_rp_implied_dy = self.indifference_curve.subs({qx: self.demand_rp_implied_qx})
        print("demand relative price implied dy =\n", self.demand_rp_implied_dy)

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
        # draw price lines only around the tangent spot
        price_line_length_per_x = (sp.N(self.ppf_slope.subs(
            {qx: self.autarky_qx})) ** 2 + 1) ** 0.5
        price_line_xrange = lim[1] / 3 / price_line_length_per_x
        price_line_range = (qx, self.autarky_qx - price_line_xrange,
                            self.autarky_qx + price_line_xrange)

        color = self.color_gen(self.rgb)

        autarky_plot = sp.plotting.plot(self.ppf, (qx, *lim), show=False,
                                        label=self.name + " ppf", line_color=next(color))
        further_plots = [
            sp.plotting.plot(self.indifference_curve, price_line_range, show=False,
                             label=self.name + " indifference curve", line_color=next(color)),
            sp.plotting.plot(self.autarky_price_line, price_line_range, show=False,
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

    def plot_relative(self, limx, limy):
        color = self.color_gen(self.rgb, 1.6)
        relative_plot = sp.plotting.plot(self.relative_supply, (rq, *limx),
                                         label=self.name + " RS " + self.product_x, show=False, line_color=next(color))
        further_plots = [
            sp.plotting.plot(self.relative_demand, (rq, *limx),
                             label=self.name + " RD " + self.product_x, show=False, line_color=next(color))
        ]
        for p in further_plots:
            relative_plot.extend(p)
        relative_plot.xlim = limx
        relative_plot.ylim = limy
        relative_plot.xlabel = "Q_" + self.product_x + " / Q_" + self.product_y
        relative_plot.ylabel = "p_" + self.product_x + " / p_" + self.product_y

        relative_plot.legend = True

        return relative_plot

    @measure
    def calc_trade_production(self, price_ratio): 
        trade_px = sp.solve(
            sp.Eq(self.ppf_slope, - price_ratio),
            qx
        )[0]
        trade_py = self.ppf.subs({qx: trade_px})
        print(f"trade production =\n{trade_px}, {trade_py}")
        return trade_px, trade_py
    
    @measure
    def calc_trade_consumption(self, trade_line): 
        trade_line_utility = self.utility.subs({dy: trade_line})
        
        trade_cx = sp.solve(sp.diff(trade_line_utility, qx), qx)[0]
        trade_cy = trade_line.subs({qx: trade_cx})
        print(f"trade consumption =\n{trade_cx}, {trade_cy}")
        return trade_cx, trade_cy

    def plot_trade(self, trade_price_ratio, lim=(0, 1)):
        trade_px, trade_py = self.calc_trade_production(trade_price_ratio)
        trade_line = - trade_price_ratio * (qx - trade_px) + trade_py
        trade_cx, trade_cy = self.calc_trade_consumption(trade_line)
        trade_max_utility = self.utility.subs({qx: trade_cx, dy: trade_cy})
        trade_indifference_curve = self.general_indifference_curve.subs({max_utility: trade_max_utility})
        
        color = self.color_gen(self.rgb)
        impx, impy = sp.symbols(['impx', 'impy'])
        
        # values for trade triangle
        if trade_px < trade_cx:
            flow = 'imports'
            l = trade_px
            r = trade_cx
            bottom = trade_cy
        else: 
            flow = 'exports'
            l = trade_cx
            r = trade_px
            bottom = trade_py

        print(f"{self.name} {flow} {r - l} {self.product_x}")
        print(f"utility change from {sp.N(self.autarky_max_utility)} => {trade_max_utility}\n")

        # trade_plot = self.plot_autarky(lim)
        trade_plot = sp.plotting.plot(self.ppf, (qx, *lim), show=False,
                                      label=self.name + " ppf", line_color=next(color))
        further_plots = [
            sp.plotting.plot(trade_line, (qx, *lim), show=False,
                label=self.name + " trade price line", line_color=next(color)),
            sp.plotting.plot(trade_indifference_curve, (qx, trade_cx - lim[1]/5, trade_cx + lim[1]/5), show=False,
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
