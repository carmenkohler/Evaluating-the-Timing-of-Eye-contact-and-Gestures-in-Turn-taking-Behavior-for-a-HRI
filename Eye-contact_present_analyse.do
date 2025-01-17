clear all
set more off
use "C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data_eye_contact_present.dta"

scatter silence_duration elapsed_time_eyecontact

scatter silence_duration elapsed_time_eyecontact || lfit silence_duration elapsed_time_eyecontact
// You can see that the line slightly decreases, but only very little

reg silence_duration elapsed_time_eyecontact
// We can see that p = 0.266, which is bigger than 0.05, and thus the H0 is rejected. We have not found enough evidence to find a significant effect.

gen gestures_num = .
replace gestures_num = 1 if gestures == "y"
replace gestures_num = 0 if gestures == "n"

anova silence_duration gestures_num c.elapsed_time_eyecontact gestures_num#c.elapsed_time_eyecontact
regress
// p = 0.444