import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



# Loading the patient 1 data, and expressing it as arrays
PRESS1_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT1/PRESS_scan1.csv"
df_PRESS1_scan1 = pd.read_csv(PRESS1_scan1_file_path)
PRESS1_scan1_values = df_PRESS1_scan1.iloc[0, 2::3]
PRESS1_scan1_values_array = PRESS1_scan1_values.to_numpy()

PRESS1_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT1/PRESS_scan2.csv"
df_PRESS1_scan2 = pd.read_csv(PRESS1_scan2_file_path)
PRESS1_scan2_values = df_PRESS1_scan2.iloc[0, 2::3]
PRESS1_scan2_values_array = PRESS1_scan2_values.to_numpy()

SLaser1_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT1/SLaser_scan1.csv"
df_SLaser1_scan1 = pd.read_csv(SLaser1_scan1_file_path)
SLaser1_scan1_values = df_SLaser1_scan1.iloc[0, 2::3]
SLaser1_scan1_values_array = SLaser1_scan1_values.to_numpy()

SLaser1_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT1/SLaser_scan2.csv"
df_SLaser1_scan2 = pd.read_csv(SLaser1_scan2_file_path)
SLaser1_scan2_values = df_SLaser1_scan2.iloc[0, 2::3]
SLaser1_scan2_values_array = SLaser1_scan2_values.to_numpy()



# Loading the patient 2 data, and expressing it as arrays
PRESS2_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT2/PRESS_scan1.csv"
df_PRESS2_scan1 = pd.read_csv(PRESS2_scan1_file_path)
PRESS2_scan1_values = df_PRESS2_scan1.iloc[0, 2::3]
PRESS2_scan1_values_array = PRESS2_scan1_values.to_numpy()

PRESS2_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT2/PRESS_scan2.csv"
df_PRESS2_scan2 = pd.read_csv(PRESS2_scan2_file_path)
PRESS2_scan2_values = df_PRESS2_scan2.iloc[0, 2::3]
PRESS2_scan2_values_array = PRESS2_scan2_values.to_numpy()

SLaser2_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT2/SLaser_scan1.csv"
df_SLaser2_scan1 = pd.read_csv(SLaser2_scan1_file_path)
SLaser2_scan1_values = df_SLaser2_scan1.iloc[0, 2::3]
SLaser2_scan1_values_array = SLaser2_scan1_values.to_numpy()

SLaser2_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT2/SLaser_scan2.csv"
df_SLaser2_scan2 = pd.read_csv(SLaser2_scan2_file_path)
SLaser2_scan2_values = df_SLaser2_scan2.iloc[0, 2::3]
SLaser2_scan2_values_array = SLaser2_scan2_values.to_numpy()



# Loading the patient 3 data, and expressing it as arrays
PRESS3_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT3/PRESS_scan1.csv"
df_PRESS3_scan1 = pd.read_csv(PRESS3_scan1_file_path)
PRESS3_scan1_values = df_PRESS3_scan1.iloc[0, 2::3]
PRESS3_scan1_values_array = PRESS3_scan1_values.to_numpy()

PRESS3_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT3/PRESS_scan2.csv"
df_PRESS3_scan2 = pd.read_csv(PRESS3_scan2_file_path)
PRESS3_scan2_values = df_PRESS3_scan2.iloc[0, 2::3]
PRESS3_scan2_values_array = PRESS3_scan2_values.to_numpy()

SLaser3_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT3/SLaser_scan1.csv"
df_SLaser3_scan1 = pd.read_csv(SLaser3_scan1_file_path)
SLaser3_scan1_values = df_SLaser3_scan1.iloc[0, 2::3]
SLaser3_scan1_values_array = SLaser3_scan1_values.to_numpy()

SLaser3_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT3/SLaser_scan2.csv"
df_SLaser3_scan2 = pd.read_csv(SLaser3_scan2_file_path)
SLaser3_scan2_values = df_SLaser3_scan2.iloc[0, 2::3]
SLaser3_scan2_values_array = SLaser3_scan2_values.to_numpy()



# Loading the patient 4 data, and expressing it as arrays
PRESS4_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT4/PRESS_scan1.csv"
df_PRESS4_scan1 = pd.read_csv(PRESS4_scan1_file_path)
PRESS4_scan1_values = df_PRESS4_scan1.iloc[0, 2::3]
PRESS4_scan1_values_array = PRESS4_scan1_values.to_numpy()

PRESS4_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT4/PRESS_scan2.csv"
df_PRESS4_scan2 = pd.read_csv(PRESS4_scan2_file_path)
PRESS4_scan2_values = df_PRESS4_scan2.iloc[0, 2::3]
PRESS4_scan2_values_array = PRESS4_scan2_values.to_numpy()

SLaser4_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT4/SLaser_scan1.csv"
df_SLaser4_scan1 = pd.read_csv(SLaser4_scan1_file_path)
SLaser4_scan1_values = df_SLaser4_scan1.iloc[0, 2::3]
SLaser4_scan1_values_array = SLaser4_scan1_values.to_numpy()

SLaser4_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT4/SLaser_scan2.csv"
df_SLaser4_scan2 = pd.read_csv(SLaser4_scan2_file_path)
SLaser4_scan2_values = df_SLaser4_scan2.iloc[0, 2::3]
SLaser4_scan2_values_array = SLaser4_scan2_values.to_numpy()



# Loading the patient 5 data, and expressing it as arrays
PRESS5_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT5/PRESS_scan1.csv"
df_PRESS5_scan1 = pd.read_csv(PRESS5_scan1_file_path)
PRESS5_scan1_values = df_PRESS5_scan1.iloc[0, 2::3]
PRESS5_scan1_values_array = PRESS5_scan1_values.to_numpy()

PRESS5_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT5/PRESS_scan2.csv"
df_PRESS5_scan2 = pd.read_csv(PRESS5_scan2_file_path)
PRESS5_scan2_values = df_PRESS5_scan2.iloc[0, 2::3]
PRESS5_scan2_values_array = PRESS5_scan2_values.to_numpy()

SLaser5_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT5/SLaser_scan1.csv"
df_SLaser5_scan1 = pd.read_csv(SLaser5_scan1_file_path)
SLaser5_scan1_values = df_SLaser5_scan1.iloc[0, 2::3]
SLaser5_scan1_values_array = SLaser5_scan1_values.to_numpy()

SLaser5_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT5/SLaser_scan2.csv"
df_SLaser5_scan2 = pd.read_csv(SLaser5_scan2_file_path)
SLaser5_scan2_values = df_SLaser5_scan2.iloc[0, 2::3]
SLaser5_scan2_values_array = SLaser5_scan2_values.to_numpy()



# Loading the patient 6 data, and expressing it as arrays
PRESS6_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT6/PRESS_scan1.csv"
df_PRESS6_scan1 = pd.read_csv(PRESS6_scan1_file_path)
PRESS6_scan1_values = df_PRESS6_scan1.iloc[0, 2::3]
PRESS6_scan1_values_array = PRESS6_scan1_values.to_numpy()

PRESS6_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT6/PRESS_scan2.csv"
df_PRESS6_scan2 = pd.read_csv(PRESS6_scan2_file_path)
PRESS6_scan2_values = df_PRESS6_scan2.iloc[0, 2::3]
PRESS6_scan2_values_array = PRESS6_scan2_values.to_numpy()

SLaser6_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT6/SLaser_scan1.csv"
df_SLaser6_scan1 = pd.read_csv(SLaser6_scan1_file_path)
SLaser6_scan1_values = df_SLaser6_scan1.iloc[0, 2::3]
SLaser6_scan1_values_array = SLaser6_scan1_values.to_numpy()

SLaser6_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT6/SLaser_scan2.csv"
df_SLaser6_scan2 = pd.read_csv(SLaser6_scan2_file_path)
SLaser6_scan2_values = df_SLaser6_scan2.iloc[0, 2::3]
SLaser6_scan2_values_array = SLaser6_scan2_values.to_numpy()



# Loading the patient 7 data, and expressing it as arrays
PRESS7_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT7/PRESS_scan1.csv"
df_PRESS7_scan1 = pd.read_csv(PRESS7_scan1_file_path)
PRESS7_scan1_values = df_PRESS7_scan1.iloc[0, 2::3]
PRESS7_scan1_values_array = PRESS7_scan1_values.to_numpy()

PRESS7_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT7/PRESS_scan2.csv"
df_PRESS7_scan2 = pd.read_csv(PRESS7_scan2_file_path)
PRESS7_scan2_values = df_PRESS7_scan2.iloc[0, 2::3]
PRESS7_scan2_values_array = PRESS7_scan2_values.to_numpy()

SLaser7_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT7/SLaser_scan1.csv"
df_SLaser7_scan1 = pd.read_csv(SLaser7_scan1_file_path)
SLaser7_scan1_values = df_SLaser7_scan1.iloc[0, 2::3]
SLaser7_scan1_values_array = SLaser7_scan1_values.to_numpy()

SLaser7_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT7/SLaser_scan2.csv"
df_SLaser7_scan2 = pd.read_csv(SLaser7_scan2_file_path)
SLaser7_scan2_values = df_SLaser7_scan2.iloc[0, 2::3]
SLaser7_scan2_values_array = SLaser7_scan2_values.to_numpy()



# Loading the patient 8 data, and expressing it as arrays
PRESS8_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT8/PRESS_scan1.csv"
df_PRESS8_scan1 = pd.read_csv(PRESS8_scan1_file_path)
PRESS8_scan1_values = df_PRESS8_scan1.iloc[0, 2::3]
PRESS8_scan1_values_array = PRESS8_scan1_values.to_numpy()

PRESS8_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT8/PRESS_scan2.csv"
df_PRESS8_scan2 = pd.read_csv(PRESS8_scan2_file_path)
PRESS8_scan2_values = df_PRESS8_scan2.iloc[0, 2::3]
PRESS8_scan2_values_array = PRESS8_scan2_values.to_numpy()

SLaser8_scan1_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT8/SLaser_scan1.csv"
df_SLaser8_scan1 = pd.read_csv(SLaser8_scan1_file_path)
SLaser8_scan1_values = df_SLaser8_scan1.iloc[0, 2::3]
SLaser8_scan1_values_array = SLaser8_scan1_values.to_numpy()

SLaser8_scan2_file_path = "C:/Users/elias/OneDrive/Desktop/Carleton/Research stuff/scan_data/PRESS_vs_SLaser/Metabolite results/TRT8/SLaser_scan2.csv"
df_SLaser8_scan2 = pd.read_csv(SLaser8_scan2_file_path)
SLaser8_scan2_values = df_SLaser8_scan2.iloc[0, 2::3]
SLaser8_scan2_values_array = SLaser8_scan2_values.to_numpy()



# Averages
PRESS1_avg = (PRESS1_scan1_values_array + PRESS1_scan2_values_array) / 2
SLaser1_avg = (SLaser1_scan1_values_array + SLaser1_scan2_values_array) / 2

PRESS2_avg = (PRESS2_scan1_values_array + PRESS2_scan2_values_array) / 2
SLaser2_avg = (SLaser2_scan1_values_array + SLaser2_scan2_values_array) / 2

PRESS3_avg = (PRESS3_scan1_values_array + PRESS3_scan2_values_array) / 2
SLaser3_avg = (SLaser3_scan1_values_array + SLaser3_scan2_values_array) / 2

PRESS4_avg = (PRESS4_scan1_values_array + PRESS4_scan2_values_array) / 2
SLaser4_avg = (SLaser4_scan1_values_array + SLaser4_scan2_values_array) / 2

PRESS5_avg = (PRESS5_scan1_values_array + PRESS5_scan2_values_array) / 2
SLaser5_avg = (SLaser5_scan1_values_array + SLaser5_scan2_values_array) / 2

PRESS6_avg = (PRESS6_scan1_values_array + PRESS6_scan2_values_array) / 2
SLaser6_avg = (SLaser6_scan1_values_array + SLaser6_scan2_values_array) / 2

PRESS7_avg = (PRESS7_scan1_values_array + PRESS7_scan2_values_array) / 2
SLaser7_avg = (SLaser7_scan1_values_array + SLaser7_scan2_values_array) / 2

PRESS8_avg = (PRESS8_scan1_values_array + PRESS8_scan2_values_array) / 2
SLaser8_avg = (SLaser8_scan1_values_array + SLaser8_scan2_values_array) / 2


PRESS_tot_avg = (1/8) * (PRESS1_avg + PRESS2_avg + PRESS3_avg + PRESS4_avg + PRESS5_avg + PRESS6_avg + PRESS7_avg + PRESS8_avg)
SLaser_tot_avg = (1/8) * (SLaser1_avg + SLaser2_avg + SLaser3_avg + SLaser4_avg + SLaser5_avg + SLaser6_avg + SLaser7_avg + SLaser8_avg)



# Partial variances
var_PRESS1_scan1 = (PRESS1_scan1_values_array - PRESS1_avg)**2
var_PRESS1_scan2 = (PRESS1_scan2_values_array - PRESS1_avg)**2
var_SLaser1_scan1 = (SLaser1_scan1_values_array - SLaser1_avg)**2
var_SLaser1_scan2 = (SLaser1_scan2_values_array - SLaser1_avg)**2

var_PRESS2_scan1 = (PRESS2_scan1_values_array - PRESS2_avg)**2
var_PRESS2_scan2 = (PRESS2_scan2_values_array - PRESS2_avg)**2
var_SLaser2_scan1 = (SLaser2_scan1_values_array - SLaser2_avg)**2
var_SLaser2_scan2 = (SLaser2_scan2_values_array - SLaser2_avg)**2

var_PRESS3_scan1 = (PRESS3_scan1_values_array - PRESS3_avg)**2
var_PRESS3_scan2 = (PRESS3_scan2_values_array - PRESS3_avg)**2
var_SLaser3_scan1 = (SLaser3_scan1_values_array - SLaser3_avg)**2
var_SLaser3_scan2 = (SLaser3_scan2_values_array - SLaser3_avg)**2

var_PRESS4_scan1 = (PRESS4_scan1_values_array - PRESS4_avg)**2
var_PRESS4_scan2 = (PRESS4_scan2_values_array - PRESS4_avg)**2
var_SLaser4_scan1 = (SLaser4_scan1_values_array - SLaser4_avg)**2
var_SLaser4_scan2 = (SLaser4_scan2_values_array - SLaser4_avg)**2

var_PRESS5_scan1 = (PRESS5_scan1_values_array - PRESS5_avg)**2
var_PRESS5_scan2 = (PRESS5_scan2_values_array - PRESS5_avg)**2
var_SLaser5_scan1 = (SLaser5_scan1_values_array - SLaser5_avg)**2
var_SLaser5_scan2 = (SLaser5_scan2_values_array - SLaser5_avg)**2

var_PRESS6_scan1 = (PRESS6_scan1_values_array - PRESS6_avg)**2
var_PRESS6_scan2 = (PRESS6_scan2_values_array - PRESS6_avg)**2
var_SLaser6_scan1 = (SLaser6_scan1_values_array - SLaser6_avg)**2
var_SLaser6_scan2 = (SLaser6_scan2_values_array - SLaser6_avg)**2

var_PRESS7_scan1 = (PRESS7_scan1_values_array - PRESS7_avg)**2
var_PRESS7_scan2 = (PRESS7_scan2_values_array - PRESS7_avg)**2
var_SLaser7_scan1 = (SLaser7_scan1_values_array - SLaser7_avg)**2
var_SLaser7_scan2 = (SLaser7_scan2_values_array - SLaser7_avg)**2

var_PRESS8_scan1 = (PRESS8_scan1_values_array - PRESS8_avg)**2
var_PRESS8_scan2 = (PRESS8_scan2_values_array - PRESS8_avg)**2
var_SLaser8_scan1 = (SLaser8_scan1_values_array - SLaser8_avg)**2
var_SLaser8_scan2 = (SLaser8_scan2_values_array - SLaser8_avg)**2


var_PRESS_sum_scan1 = var_PRESS1_scan1 + var_PRESS2_scan1 + var_PRESS3_scan1 + var_PRESS4_scan1 + var_PRESS5_scan1 + var_PRESS6_scan1 + var_PRESS7_scan1 + var_PRESS8_scan1
var_SLaser_sum_scan1 = var_SLaser1_scan1 + var_SLaser2_scan1 + var_SLaser3_scan1 + var_SLaser4_scan1 + var_SLaser5_scan1 + var_SLaser6_scan1 + var_SLaser7_scan1 + var_SLaser8_scan1

var_PRESS_sum_scan2 = var_PRESS1_scan2 + var_PRESS2_scan2 + var_PRESS3_scan2 + var_PRESS4_scan2 + var_PRESS5_scan2 + var_PRESS6_scan2 + var_PRESS7_scan2 + var_PRESS8_scan2
var_SLaser_sum_scan2 = var_SLaser1_scan2 + var_SLaser2_scan2 + var_SLaser3_scan2 + var_SLaser4_scan2 + var_SLaser5_scan2 + var_SLaser6_scan2 + var_SLaser7_scan2 + var_SLaser8_scan2

var_PRESS_final = 1/(2*8) * (var_PRESS_sum_scan1 + var_PRESS_sum_scan2)
var_SLaser_final = 1/(2*8) * (var_SLaser_sum_scan1 + var_SLaser_sum_scan2)



# Non summed intraclass Correlation
r_partial_PRESS1 = (PRESS1_scan1_values_array - PRESS_tot_avg) * (PRESS1_scan2_values_array - PRESS_tot_avg)
r_partial_SLaser1 = (SLaser1_scan1_values_array - SLaser_tot_avg) * (SLaser1_scan2_values_array - SLaser_tot_avg)

r_partial_PRESS2 = (PRESS2_scan1_values_array - PRESS_tot_avg) * (PRESS2_scan2_values_array - PRESS_tot_avg)
r_partial_SLaser2 = (SLaser2_scan1_values_array - SLaser_tot_avg) * (SLaser2_scan2_values_array - SLaser_tot_avg)

r_partial_PRESS3 = (PRESS3_scan1_values_array - PRESS_tot_avg) * (PRESS3_scan2_values_array - PRESS_tot_avg)
r_partial_SLaser3 = (SLaser3_scan1_values_array - SLaser_tot_avg) * (SLaser3_scan2_values_array - SLaser_tot_avg)

r_partial_PRESS4 = (PRESS4_scan1_values_array - PRESS_tot_avg) * (PRESS4_scan2_values_array - PRESS_tot_avg)
r_partial_SLaser4 = (SLaser4_scan1_values_array - SLaser_tot_avg) * (SLaser4_scan2_values_array - SLaser_tot_avg)

r_partial_PRESS5 = (PRESS5_scan1_values_array - PRESS_tot_avg) * (PRESS5_scan2_values_array - PRESS_tot_avg)
r_partial_SLaser5 = (SLaser5_scan1_values_array - SLaser_tot_avg) * (SLaser5_scan2_values_array - SLaser_tot_avg)

r_partial_PRESS6 = (PRESS6_scan1_values_array - PRESS_tot_avg) * (PRESS6_scan2_values_array - PRESS_tot_avg)
r_partial_SLaser6 = (SLaser6_scan1_values_array - SLaser_tot_avg) * (SLaser6_scan2_values_array - SLaser_tot_avg)

r_partial_PRESS7 = (PRESS7_scan1_values_array - PRESS_tot_avg) * (PRESS7_scan2_values_array - PRESS_tot_avg)
r_partial_SLaser7 = (SLaser7_scan1_values_array - SLaser_tot_avg) * (SLaser7_scan2_values_array - SLaser_tot_avg)

r_partial_PRESS8 = (PRESS8_scan1_values_array - PRESS_tot_avg) * (PRESS8_scan2_values_array - PRESS_tot_avg)
r_partial_SLaser8 = (SLaser8_scan1_values_array - SLaser_tot_avg) * (SLaser8_scan2_values_array - SLaser_tot_avg)



# intraclass Correlation

r_PRESS = 1/(8 * var_PRESS_final) * (r_partial_PRESS1 + r_partial_PRESS2 + r_partial_PRESS3 + r_partial_PRESS4 + r_partial_PRESS5 + r_partial_PRESS6 + r_partial_PRESS7 + r_partial_PRESS8)
r_SLaser = 1/(8 * var_SLaser_final) * (r_partial_SLaser1 + r_partial_SLaser2 + r_partial_SLaser3 + r_partial_SLaser4 + r_partial_SLaser5 + r_partial_SLaser6 + r_partial_SLaser7 + r_partial_SLaser8)

print(r_PRESS)
print(r_SLaser)