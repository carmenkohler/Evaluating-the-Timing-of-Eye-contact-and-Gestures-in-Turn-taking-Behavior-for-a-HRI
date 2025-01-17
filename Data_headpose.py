import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_headpose_exp3 = pd.read_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data\Experiment 3 1545-1645\headpose_20_11_1545_1645.txt', header=None, delimiter="\t")
df_headpose_exp4 = pd.read_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data\Experiment 4 1045-1145\headpose_21_11_1045_1145.txt', header=None, delimiter="\t")
df_headpose_exp5 = pd.read_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data\Experiment 5 1200-1300\headpose_8_9.csv', header=None, delimiter=",")
df_headpose_exp6 = pd.read_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data\Experiment 6 1315-1415\headpose_22_11_1315_1415.txt', header=None, delimiter="\t")
df_headpose_exp7 = pd.read_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data\Experiment 7 1045-1145\headpose_22_11_1045_1145.391247370229646 20', header=None, delimiter="\t")
df_headpose_exp8 = pd.read_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data\Experiment 8 1200-1300\headpose_21_11 1200_1300.txt', header=None, delimiter="\t")
df_headpose_exp9 = pd.read_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data\Experiment 9 13.15-14.15\headpose_25_11_1315_1415.txt', header=None, delimiter="\t")
df_headpose_exp10 = pd.read_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data\Experiment 10 1545-1645\headpose_22_11_1545_1645.txt', header=None, delimiter="\t")
df_headpose_exp11 = pd.read_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data\Experiment 11 15.45-16.45\headpose_25_11_1545_1645.txt', header=None, delimiter="\t")
df_headpose_exp12 = pd.read_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data\Experiment 12 930-1030\headpose_26_11_930_1030.txt', header=None, delimiter="\t")
df_headpose_exp13 = pd.read_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data\Experiment 13 1545-1645\headpose_26_11_1545_1645.txt', header=None, delimiter="\t")

df_headpose_3_to_8 = pd.concat([df_headpose_exp3, df_headpose_exp4, df_headpose_exp5, df_headpose_exp6, df_headpose_exp7, df_headpose_exp8])
df_headpose_9_to_14 = pd.concat([df_headpose_exp9, df_headpose_exp10, df_headpose_exp11, df_headpose_exp12, df_headpose_exp13])
df_headpose_all = pd.concat([df_headpose_3_to_8, df_headpose_9_to_14])
df_headpose_all.columns = ['Pitch', 'Yaw', 'Timestamp', 'Unknown']
df_headpose_all.head()

plt.figure(figsize=(10, 6))
ax_scatterplot_headposition_data = plt.axes()
sns.histplot(data = df_headpose_all, x = 'Yaw', binwidth = 3)
plt.xlabel('Yaw (in degrees)')
plt.ylabel('Count')
plt.title('Yaw count in all data')
plt.show()