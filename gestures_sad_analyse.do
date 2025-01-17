clear all
set more off
use "C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data_gestures_sad.dta"

sum silence_duration if gestures == "n"
// obs = 32
// mean = 1.828125
// sd = 1.045492
// min = .3
// max = 3.8

sum silence_duration if gestures == "y"
// obs = 28
// mean = 1.142857
// sd = .8234654
// min = .1
// max = 3.6

// Let's test for normality
swilk silence_duration if gestures == "n" // p = 0.08802
swilk silence_duration if gestures == "y" // p = 0.00577
sktest silence_duration if gestures == "n" // p = 0.0663
sktest silence_duration if gestures == "y" // p = 0.0101
// Normality is rejected because there are multiple p-values smaller than 0.05. Hence, I will perform a ladder test.

ladder silence_duration if gestures == "n"
ladder silence_duration if gestures == "y"
// Both log and square root seem to be possible transformations, I will first test the log

gen logsilence_duration = log(silence_duration)

swilk logsilence_duration if gestures == "y" // p=0.53289
swilk logsilence_duration if gestures == "n" // p=0.05203
sktest logsilence_duration if gestures == "y" // p=0.2552
sktest logsilence_duration if gestures == "n" // p=0.2105
// Normality is not rejected, so I can perform my ttest now

ttest logsilence_duration, by(gestures) unequal
// p-value  = 0.0085, which is smaller than 0.05. Hence, we have found that there is sufficient evidence to say that using gestures or not in the sad condition does show a difference in the silence duration.

esize twosample logsilence_duration, by(gestures) unequal
// d = 0.7122177, which is thus a medium effect size. 