import math

# https://www.tf.uni-kiel.de/matwis/amat/iss/kap_8/advanced/a8_3_1.html
yearly_avg_W_per_h_and_m2 = 200 # W/m2
panel_efficiency = 0.15

Wh_per_year_per_m2 = 365.25 * 24 * panel_efficiency * yearly_avg_W_per_h_and_m2
print("Wh generation per year per square meter", Wh_per_year_per_m2)

# bp report
world_consumption_EJ = 583.90 
world_consumption_TWh = world_consumption_EJ * 1000 / 3.6 
print(world_consumption_TWh) # more compared to final consumption, because lot's of energy is consumed in energy production 

# https://www.iea.org/subscribe-to-data-services/world-energy-balances-and-statistics
# 9 938 Mtoe world final consumption
world_final_consumption_Wh = 9938 * 10**6 * 1.163 * 10**7
print("world consumption per year in TWh (according to iea.org)", world_final_consumption_Wh / 10 ** 12)

m2 = world_final_consumption_Wh / Wh_per_year_per_m2

km2 = m2 / 10**6

print("square kilometers", km2)
print("side length in km", math.sqrt(km2))



