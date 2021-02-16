from sympy import symbols

# symbols
q_pv = qx = symbols('qx', positive=True, real=True)  # quantity of good x
q_wine = qy = symbols('qy', positive=True, real=True)  # quantity of good x
sy = symbols('sy', positive=True, real=True)  # supply of good y
dy = symbols('dy', positive=True, real=True)  # demand of good y
# max utility that can be reached for a given budget
max_utility = symbols('max_utility', positive=True, real=True)

# RS and RD of good x
rq = symbols('rq', positive=True, real=True)  # relative quantity
# for trade
rp = symbols('rp', positive=True, real=True)  # relative price
