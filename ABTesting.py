import scipy.stats as st
import math


# User given parameters
control_conversion_rate = 0.025 # Primary Success Metric
target_change = -0.1    # Expected Change in Primary Success Metric
alpha = 0.05    # Confidence Level  Change to output a standard array. For now, 80, 85, 90, 95, 99
beta = 0.8  # Power
tail_count = 2  # One or Two Tailed (radio button)
pop_ratio = 0.5   # Control:Variant Ratio   []:[] (0.5 means[2]:[1]. Because fuck me) *
weekly_visits = 14000 # Weekly Visitors *

# Calculations
variance_conversion_rate = control_conversion_rate * (1+target_change)

pooled_variance_estimator = control_conversion_rate*(1-control_conversion_rate) + variance_conversion_rate*(1-variance_conversion_rate)

za2 = round(st.norm.ppf(1-alpha/tail_count), 2)

zb = round(abs(st.norm.ppf(1-beta)), 2)

equal_split_1 = (pooled_variance_estimator/(control_conversion_rate-variance_conversion_rate)**2)
equal_split_2 = (za2+zb)**2
equal_split = math.ceil(equal_split_1*equal_split_2)

revised_sample_size = math.ceil((equal_split * (1+pop_ratio)**2)/(4*pop_ratio))

pop_1_size = math.ceil(revised_sample_size/(1+pop_ratio))

pop_2_size = math.ceil((pop_ratio*revised_sample_size)/(1+pop_ratio))

week_count = math.ceil(revised_sample_size/weekly_visits)

print('It will take %d week(s) to get the %d visiors required.' % (week_count, revised_sample_size))
print('The control group requires %d visitors and the variant group requires %d visitors' % (pop_1_size, pop_2_size))
