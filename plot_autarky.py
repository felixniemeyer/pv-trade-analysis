import sympy as sp

Q_pv = sp.symbols('Q_pv', positive=True)

PQ_wine = sp.symbols('PQ_wine', positive=True)
CQ_wine = sp.symbols('CQ_wine', positive=True)

utility = Q_pv**sp.S(1/3) * CQ_wine**sp.S(1/2)

production_cost = sp.sqrt((Q_pv*sp.S(3/2))**sp.S(2) + PQ_wine**sp.S(2)) # sp.sqrt(Q_pv**2 + PQ_wine**2)

budget = sp.symbols("budget", positive=True)
max_utility = sp.symbols('max_utility', positive=True)

general_ppf = sp.solve(sp.Eq(production_cost, budget), PQ_wine)[0]

general_indifference_curve = sp.solve(sp.Eq(utility, max_utility), CQ_wine)[0]

ppf = general_ppf.subs({budget: sp.S(100)})
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

plot = sp.plotting.plot(ppf, (Q_pv, 0, 150), show=False, label="ppf")
further_graphs = [
    sp.plotting.plot(general_indifference_curve.subs({max_utility: mu}), (Q_pv, 0, 150), show=False, label="ic"),
    sp.plotting.plot(tangent, (Q_pv, 0, 150), show=False, label="ic"),
]
for g in further_graphs: 
    plot.extend(g)
plot.xlim = (0, 150)
plot.ylim = (0, 150)
plot.show()