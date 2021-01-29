total_2019_renewable_consumption_TWh = 2805.5
total_2019_renewable_consumption_EJ = total_2019_renewable_consumption_TWh * 3.6 / 1000



total_2019_renewable_generation_EJ = 25.01

print("should equal this factor for input-equivalence:", total_2019_renewable_consumption_EJ / total_2019_renewable_generation_EJ)

# 2018: 0.4, 2050: 0.45
year = 2019
factor = 0.4 + (0.45 - 0.4) * (year - 2017) / (2050 - 2017)
print("input-equivalent factor for 2019", factor)

