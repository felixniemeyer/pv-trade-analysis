import sympy as sp
import colorsys
import time

from symbols import *

def make_ellipsoid_ppf(max_pv, max_wine):
    general_ppf = sp.solve(
        sp.Eq(sp.sqrt((qx/max_pv) ** sp.Rational(2,1) + (qy/max_wine) ** sp.Rational(2,1)), 1),
        qy
    )[0]
    return general_ppf

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
        self.ppf_slope = sp.diff(self.ppf, qx)

        # the following calculations rely on each other and need to be in order
        self.calc_autarky_optimum() 
        self.calc_indifference_curve()
        self.calc_relative_supply()
        self.calc_relative_demand()
        self.calc_rp_implied_production()
        self.calc_rp_implied_demand()

    @measure
    def calc_autarky_optimum(self): 
        self.ppf_utility = self.utility.subs({dy: self.ppf})
        self.ppf_utility_slope = sp.diff(self.ppf_utility, qx)
        self.autarky_qx = sp.solve(
            self.ppf_utility_slope, 
            qx
        )[0]
        self.autarky_qy = self.ppf.subs({qx: self.autarky_qx})
        print(f"{self.name}: optimal production under autarky: qx, qy =\n\t{self.autarky_qx}, {self.autarky_qy}")
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
        print(f"{self.name}: indifference curve under autarky =\n\t{self.indifference_curve}")


    @measure
    def calc_relative_supply(self): 
        self.rq_implied_qx = sp.solve([
            sp.Eq(rq, qx / self.ppf)
        ], qx)[0][0]
        print(f"{self.name}: q_{self.product_x}(rq) =\n\t{self.rq_implied_qx}")
        self.rq_implied_rp = - \
            self.ppf_slope.subs({qx: self.rq_implied_qx})
        print(f"{self.name}: rp(rq) =\n\t{self.rq_implied_rp}")
        
    @measure 
    def calc_relative_demand(self): 
        pass # too complicated mathematically for now
        
    @measure
    def calc_rp_implied_production(self): 
        self.rp_implied_qx = sp.solve(
            sp.Eq(self.ppf_slope, - rp),  
            qx
        )[0]
        print("rp implied qx =\n", self.rp_implied_qx)
        self.rp_implied_qy = self.ppf.subs({qx: self.rp_implied_qx})
        print("rp implied qy =\n", self.rp_implied_qy)
        self.rp_implied_rq = self.rp_implied_qx / self.rp_implied_qy
        print("test")
    
    @measure
    def calc_rp_implied_demand(self): 
        self.rp_implied_trade_line = (-rp) * (qx - self.rp_implied_qx) + self.rp_implied_qy
        rp_implied_trade_line_utility = self.utility.subs({dy: self.rp_implied_trade_line})
        print("rp implied trade line utility =\n", rp_implied_trade_line_utility)
        self.rp_implied_dx = sp.solve(rp_implied_trade_line_utility.diff(qx), (qx))[0]
        print("rp implied dx =\n", self.rp_implied_dx)
        self.rp_implied_dy = self.rp_implied_trade_line.subs({qx: self.rp_implied_dx})
        print("rp implied dy =\n", self.rp_implied_dy)
        self.rp_implied_rd = self.rp_implied_dx / self.rp_implied_dy

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
        relative_plot = sp.plotting.plot(self.rq_implied_rp, (rq, *limx),
                                         label=self.name + " RS " + self.product_x, show=False, line_color=next(color))
        further_plots = [
            sp.plotting.plot_parametric(self.rp_implied_rd, rp, (rp, limy[1]/10, limy[1]), 
                label=self.name + " RD " + self.product_x, show=False, line_color=next(color)), 
        ]
        for p in further_plots:
            relative_plot.extend(p)
        relative_plot.xlim = limx
        relative_plot.ylim = limy
        relative_plot.xlabel = "Q_" + self.product_x + " / Q_" + self.product_y
        relative_plot.ylabel = "p_" + self.product_x + " / p_" + self.product_y

        relative_plot.legend = True

        return relative_plot

    def plot_trade(self, trade_price_ratio, lim=(0, 1)):
        trade_qx = self.rp_implied_qx.subs({rp:trade_price_ratio})
        trade_qy = self.rp_implied_qy.subs({rp:trade_price_ratio})
        print(f"production under trade =\n{trade_qx}, {trade_qy}")
        trade_line = self.rp_implied_trade_line.subs({rp:trade_price_ratio}) 
        trade_dx = self.rp_implied_dx.subs({rp:trade_price_ratio})
        trade_dy = self.rp_implied_dy.subs({rp:trade_price_ratio})
        print(f"demand under trade =\n{trade_dx}, {trade_dy}")

        trade_max_utility = self.utility.subs({qx: trade_dx, dy: trade_dy})
        trade_indifference_curve = self.general_indifference_curve.subs({max_utility: trade_max_utility})
        
        # values for trade triangle
        if trade_dx < trade_qx:
            flow = 'exports'
            l = trade_dx
            r = trade_qx
            bottom = trade_qy
        else: 
            flow = 'imports'
            l = trade_qx
            r = trade_dx
            bottom = trade_dy
        
        d = r - l

        print(f"{self.name} {flow} {d} {self.product_x}")
        print(f"utility change from {sp.N(self.autarky_max_utility)} => {trade_max_utility}\n")

        color = self.color_gen(self.rgb)
        
        # for trade triangle implicit plot
        impx, impy = sp.symbols(['impx', 'impy'])

        # trade_plot = self.plot_autarky(lim)
        trade_plot = sp.plotting.plot(self.ppf, (qx, *lim), show=False,
                                      label=self.name + " ppf", line_color=next(color))
        further_plots = [
            sp.plotting.plot(trade_line, (qx, l - d, r + d), show=False,
                label=self.name + " trade price line", line_color=next(color)),
            sp.plotting.plot(trade_indifference_curve, (qx, trade_dx - lim[1]/5, trade_dx + lim[1]/5), show=False,
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
