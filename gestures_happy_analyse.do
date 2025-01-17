clear all
set more off
use "C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data_gestures_happy.dta"

sum silence_duration if gestures == "n"
// obs = 30
// mean = 1.436667
// sd = .7672087
// min = .2
// max = 3

sum silence_duration if gestures == "y"
// obs = 27
// mean = 1.577778
// sd = .8776425
// min = .2
// max = 3.6

// let's test for normality
swilk silence_duration if gestures == "y" // p = 0.46597
swilk silence_duration if gestures == "n" // p = 0.23324
sktest silence_duration if gestures == "y" // p = 0.4880
sktest silence_duration if gestures == "n" // p = 0.2569
// All values are bigger than 0.05, thus the data is normally distributed, we can run a ttest

ttest silence_duration, by(gestures) unequal
// p = 0.5230
// p-value is bigger than 0.05. We do not reject H0. There is no evidence for a difference in silence_duration if gestures are used or if they are not used.

