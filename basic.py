import matplotlib.pyplot as plt
import sympy as sp

Q_pv = sp.symbols('Q_pv', positive=True)

PQ_wine = sp.symbols('PQ_wine', positive=True)
CQ_wine = sp.symbols('CQ_wine', positive=True)

utility = sp.sqrt(Q_pv*CQ_wine)

production_cost = sp.sqrt((Q_pv*2)**2 + PQ_wine**2) # sp.sqrt(Q_pv**2 + PQ_wine**2)
print(production_cost)

# plot utility function
# sp.plotting.plot3d(utility, (Q_pv, 0, 1), (CQ_wine, 0, 1))

budget = sp.symbols("budget", positive=True)
max_utility = sp.symbols('max_utility', positive=True)

general_ppf = sp.solve(sp.Eq(production_cost, budget), PQ_wine)[0]

general_indifference_curve = sp.solve(sp.Eq(utility, max_utility), CQ_wine)[0]

ppf = general_ppf.subs({budget: sp.S(100)})

ratio = sp.diff(ppf, Q_pv)

    
(mu, qpv) = optimum = sp.solve([
    sp.Eq(ppf, general_indifference_curve), 
    sp.Eq(ratio, sp.diff(general_indifference_curve, Q_pv))
], (max_utility, Q_pv))[0]

print("maximum utility resulting from production budget:", mu)

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