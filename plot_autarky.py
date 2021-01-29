import sympy as sp
import matplotlib.pyplot as plt

# SAVE_TO_FILE = <file prefix> or False
SAVE_TO_FILE = "plots/autarky/" 

def plot_autarky(u_pv_exponent, u_wine_exponent, p_pv_coefficient, p_wine_coefficient, budget, title):
    Q_pv = sp.symbols('Q_pv', positive=True)
    PQ_wine = sp.symbols('PQ_wine', positive=True)
    CQ_wine = sp.symbols('CQ_wine', positive=True)
    max_utility = sp.symbols('max_utility', positive=True)

    utility = Q_pv**u_pv_exponent * CQ_wine**u_wine_exponent

    production_cost = sp.sqrt((Q_pv*p_pv_coefficient)**2 + (PQ_wine*p_wine_coefficient)**2) 

    ppf = sp.solve(sp.Eq(production_cost, budget), PQ_wine)[0]

    general_indifference_curve = sp.solve(sp.Eq(utility, max_utility), CQ_wine)[0]

    ratio = sp.diff(ppf, Q_pv)

    ppf_utility = utility.subs({CQ_wine: ppf})
    ppf_utility_d = sp.diff(ppf_utility, Q_pv)

    optimum = sp.solve([
        ppf_utility_d, 
        sp.Eq(ppf, general_indifference_curve)
    ],
        (max_utility, Q_pv)
    )

    print(optimum)

    (mu, qpv) = optimum[0]

    tangent = ratio.subs({Q_pv:qpv}) * ( Q_pv - qpv) + ppf.subs({Q_pv:qpv})

    plot = sp.plotting.plot(ppf, (Q_pv, 0, 150), show=False, label="ppf", line_color='#ee6321')
    further_graphs = [
        sp.plotting.plot(general_indifference_curve.subs({max_utility: mu}), (Q_pv, 0, 150), show=False, label="indifference curve", line_color='#3070ab'),
        sp.plotting.plot(tangent, (Q_pv, 0, 150), show=False, label="tangent", line_color='grey'),
    ]
    for g in further_graphs: 
        plot.extend(g)
    plot.xlim = (0, 160)
    plot.ylim = (0, 160)
    plot.xlabel = "Q_PV"
    plot.ylabel = "Q_wine"
    plot.legend = True
    # plot.title = title + "(autarky)" 
    if(SAVE_TO_FILE != False and title != False):
        plot.save(SAVE_TO_FILE + title + ".png")
    plot.show()
    
plot_autarky(
    sp.S(1/2),
    sp.S(1/2),
    sp.S(1),
    sp.S(1),
    sp.S(100),
    "initial position"
)

plot_autarky(
    sp.S(2),
    sp.S(1/2),
    sp.S(1),
    sp.S(1),
    sp.S(100),
    "EU with PV consumption subsidies"
)

plot_autarky(
    sp.S(1/2),
    sp.S(1/2),
    sp.S(2/3),
    sp.S(1),
    sp.S(100),
    "CN with PV production subsidies"
)