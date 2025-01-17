import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_gestures = pd.read_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data_headpose_audio_timing_gestures - Copy (2).csv', header = None, delimiter=',')
df_eyecontact = pd.read_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data_headpose_audio_timing_eye_contact.csv', header = None, delimiter=',' )

df_gestures.columns = ['Experiment', 'N/H/S', 'Gestures', 'Eye-contact_(lates_ time-value)', 'Misty_stop', 'Participants_start']
df_gestures.drop(index=0, inplace=True)
df_eyecontact.columns = ['Experiment', 'N/H/S', 'Gestures', 'Eye-contact_(lates_ time-value)', 'Misty_stop', 'Participants_start']
df_eyecontact.drop(index=0, inplace=True)

#Ensure the correct columns are added
df_gestures['Misty_stop'] = pd.to_numeric(df_gestures['Misty_stop'], errors='coerce')
df_gestures['Participants_start'] = pd.to_numeric(df_gestures['Participants_start'], errors='coerce')
df_gestures['Silence_duration'] = df_gestures['Participants_start'] - df_gestures['Misty_stop']
print(df_gestures)

plt.figure(figsize=(10,6))
sns.histplot(data=df_gestures, x='Silence_duration', binwidth=0.5)
plt.ylabel("Count")
plt.xlabel("Silence Duration (in sec)")
plt.title("Silence Duration counts")
plt.show()

df_gestures_filter1 = df_gestures[df_gestures['Silence_duration'] <= 10]
plt.figure(figsize=(10,6))
sns.histplot(data=df_gestures_filter1, x='Silence_duration', binwidth=0.5)
plt.ylabel("Count")
plt.xlabel("Silence Duration (in sec)")
plt.title("Silence Duration counts")
plt.show()


# Filter rows where Silence_duration <= 5
filtered_data_gestures = df_gestures[df_gestures['Silence_duration'] <= 5]
filtered_data_gestures_std = filtered_data_gestures['Silence_duration'].std()
print(filtered_data_gestures_std)
filtered_data_gestures = filtered_data_gestures[filtered_data_gestures['Silence_duration']<= (3+filtered_data_gestures_std)]
filtered_data_gestures = filtered_data_gestures[filtered_data_gestures['Silence_duration']>= (filtered_data_gestures_std - 3)]
filtered_data_gestures.to_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data_gestures.csv')
order_gestures = ['y', 'n']
custom_palette = {'y': 'green', 'n': 'red'}
plt.figure(figsize=(10, 6))
sns.boxplot(data=filtered_data_gestures, x='Silence_duration', y='Gestures', palette=custom_palette, order=order_gestures)
sns.stripplot(data=filtered_data_gestures, x="Silence_duration", y="Gestures", 
              size=4, color=".3", jitter=True, order = order_gestures)
plt.ylabel("Gestures (y = present, n = not present)")
plt.xlabel("Silence Duration (in sec)")
plt.title("Comparison of Silence Duration with/without Gestures")
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

#I also want to show the effect of the different conditions
custom_pallette_conditions = {'n': 'orange', 'h': 'green', 's': 'blue'}
plt.figure(figsize=(10, 6))
sns.boxplot(data=filtered_data_gestures, x='Silence_duration', y='N/H/S', palette=custom_pallette_conditions)
sns.stripplot(data=filtered_data_gestures, x="Silence_duration", y="N/H/S", 
              size=4, color=".3", jitter=True)
plt.ylabel("Emotional condition (n = neutral, h = happy, s = sad)")
plt.xlabel("Silence Duration (in sec)")
plt.title("Comparison of Silence Duration with emotional conditions")
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

#since there was only gestures measured in happy and sad, I want to reflect them individually as well
filtered_data_gestures_happy = filtered_data_gestures[filtered_data_gestures['N/H/S'] == 'h']
filtered_data_gestures_happy.to_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data_gestures_happy.csv')
custom_palette = {'y': 'green', 'n': 'red'}
plt.figure(figsize=(10, 6))
sns.boxplot(data=filtered_data_gestures_happy, x='Silence_duration', y='Gestures', palette=custom_palette)
sns.stripplot(data=filtered_data_gestures_happy, x="Silence_duration", y="Gestures", 
              size=4, color=".3", jitter=True)
plt.ylabel("Gestures (y = present, n = not present)")
plt.xlabel("Silence Duration (in sec)")
plt.title("Comparison of Silence Duration with/without Gestures in Happy condition")
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

#sad
filtered_data_gestures_sad = filtered_data_gestures[filtered_data_gestures['N/H/S']=='s']
filtered_data_gestures_sad.to_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data_gestures_sad.csv')
custom_palette = {'y': 'green', 'n': 'red'}
plt.figure(figsize=(10, 6))
sns.boxplot(data=filtered_data_gestures_happy, x='Silence_duration', y='Gestures', palette=custom_palette)
sns.stripplot(data=filtered_data_gestures_happy, x="Silence_duration", y="Gestures", 
              size=4, color=".3", jitter=True)
plt.ylabel("Gestures (y = present, n = not present)")
plt.xlabel("Silence Duration (in sec)")
plt.title("Comparison of Silence Duration with/without Gestures in Sad condition")
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

#Now I want to process the df_eyecontact
# Now I want to process the df_eyecontact
df_eyecontact['Eye-contact_(lates_ time-value)'] = pd.to_numeric(df_eyecontact['Eye-contact_(lates_ time-value)'], errors='coerce')
df_eyecontact['Eye-contact_(lates_ time-value)'] = df_eyecontact['Eye-contact_(lates_ time-value)'].fillna(5000)
df_eyecontact['Misty_stop'] = pd.to_numeric(df_eyecontact['Misty_stop'], errors='coerce')
df_eyecontact['Participants_start'] = pd.to_numeric(df_eyecontact['Participants_start'], errors='coerce')
df_eyecontact['Silence_duration'] = df_eyecontact['Participants_start'] - df_eyecontact['Misty_stop']
df_eyecontact.loc[df_eyecontact['Eye-contact_(lates_ time-value)'] <= 4999, 'Elapsed_time_eyecontact'] = df_eyecontact['Misty_stop'] - df_eyecontact['Eye-contact_(lates_ time-value)']
df_eyecontact.loc[df_eyecontact['Elapsed_time_eyecontact'].isna(), 'Elapsed_time_eyecontact'] = 5000
df_eyecontact['Eyecontact_presence'] = df_eyecontact['Elapsed_time_eyecontact'].apply(lambda x: 'n' if x == 5000 else 'y')
print(df_eyecontact)

#Filter the data for the plots
filtered_data_eyecontact = df_eyecontact[df_eyecontact['Silence_duration'] <= 5]
filtered_data_eyecontact_std = filtered_data_eyecontact['Silence_duration'].std()
print(filtered_data_eyecontact_std)
filtered_data_eyecontact = filtered_data_eyecontact[filtered_data_eyecontact['Silence_duration']<= (3+filtered_data_eyecontact_std)]
filtered_data_eyecontact = filtered_data_eyecontact[filtered_data_eyecontact['Silence_duration']>= (filtered_data_eyecontact_std - 3)]
filtered_data_eyecontact.to_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data_eye_contact_presence.csv')
df_eyecontact_present = df_eyecontact[df_eyecontact['Eyecontact_presence'] == 'y']
df_eyecontact_present = df_eyecontact_present[df_eyecontact_present['Elapsed_time_eyecontact'] >= 0]
df_eyecontact_present = df_eyecontact_present[df_eyecontact_present['Silence_duration'] <= 5]
df_eyecontact_present_std = df_eyecontact_present['Silence_duration'].std()
print(df_eyecontact_present_std)
df_eyecontact_present = df_eyecontact_present[df_eyecontact_present['Silence_duration']<= (3+df_eyecontact_present_std)]
df_eyecontact_present = df_eyecontact_present[df_eyecontact_present['Silence_duration']>= (df_eyecontact_present_std - 3)]
df_eyecontact_present.to_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data_eye_contact_present.csv')

# Now I will visualize the df_eyecontact, whether the eye_contact was present or not
plt.figure(figsize=(10, 6))
custom_palette = {'y': 'green', 'n': 'red'}
sns.boxplot(data=filtered_data_eyecontact, x='Silence_duration', y='Eyecontact_presence', palette=custom_palette)
sns.stripplot(data=filtered_data_eyecontact, x="Silence_duration", y='Eyecontact_presence', 
              size=4, color=".3", jitter=True)
plt.ylabel("Eyecontact presence (n = not present, y = present)")
plt.xlabel("Silence Duration (in sec)")
plt.title("Comparison of Silence Duration with the presence of Eyecontact")
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

#I want to add a plot for the combination of both gestures and eye-contact
filtered_data_eyecontact = filtered_data_eyecontact.copy()
filtered_data_eyecontact['Gestures_Eyecontact'] = (
    filtered_data_eyecontact['Gestures'] + filtered_data_eyecontact['Eyecontact_presence']
)
print(filtered_data_eyecontact[['Gestures', 'Eyecontact_presence', 'Gestures_Eyecontact']])
plt.figure(figsize=(10,6))
order = ['yy', 'yn', 'ny', 'nn']
filtered_data_eyecontact.to_csv(r'C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data_eye_contact_presence.csv')
custom_pallette_combination = {'yy': 'green', 'yn': 'orange', 'ny': 'yellow', 'nn': 'red'}
sns.boxplot(data=filtered_data_eyecontact, x='Silence_duration', y='Gestures_Eyecontact', palette=custom_pallette_combination, order=order)
sns.stripplot(data=filtered_data_eyecontact, x="Silence_duration", y='Gestures_Eyecontact', 
              size=4, color=".3", jitter=True, order=order)
plt.ylabel("Presence of gestures (first letter)and eyecontact (second letter), n = not present, y = present")
plt.xlabel("Silence Duration (in sec)")
plt.title("Comparison of Silence Duration with the combined presence of gestures and or eyecontact")
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

#The statistical analysis can be found in stata