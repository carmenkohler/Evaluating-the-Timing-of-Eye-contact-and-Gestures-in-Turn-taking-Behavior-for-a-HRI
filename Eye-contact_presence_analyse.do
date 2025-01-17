clear all
set more off
use "C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data_eye_contact_presence.dta"

sum silence_duration if eyecontact_presence == "y"
// obs = 68
// mean = 1.351471
// sd = 0.8156112
// min = .2
// max = 3.8

sum silence_duration if eyecontact_presence == "n"
// obs = 66
// mean = 1.831818
// sd = .9282173
// min = .3
// max = 3.9

// Let's first test whether the data is normally distributed
swilk silence_duration if eyecontact_presence == "y" // p = 0.00071
swilk silence_duration if eyecontact_presence == "n" // p = 0.04820
sktest silence_duration if eyecontact_presence == "y" // p = 0.0041
sktest silence_duration if eyecontact_presence == "n" // p = 0.0269
// All p-values were smaller than 0.05, thus I will perform a ladder test to see if there is a transformation that we can make such that the data will be normally distributed.

ladder silence_duration if eyecontact_presence == "y"
ladder silence_duration if eyecontact_presence == "n"
// We could try the log as this is the value for which the p-values are in both tests larger than 0.05

gen logsilence_duration = log(silence_duration)

// Now we again test whether the data is normally distributed, using the log of the silence_duration
swilk logsilence_duration if eyecontact_presence == "y" // p = 0.03415
swilk logsilence_duration if eyecontact_presence == "n" // p = 0.00322
sktest logsilence_duration if eyecontact_presence == "y" // p = 0.1415
sktest logsilence_duration if eyecontact_presence == "n" // p = 0.0765
// We also see that the the data is again not normally distributed, as there is a p-value lower than 0.05. Hence, we decide to use the ranksum and median test.

ranksum silence_duration, by(eyecontact_presence)
// p = 0.0017, which is smaller than 0.05, so this suggests a significant effect.
median silence_duration, by(eyecontact_presence)
// p = 0.0021, which is smaller than 0.05, so this suggests that there is enough evidence to not reject H0.

esize twosample silence_duration, by(eyecontact_presence) unequal
// Cohen's d = 0.550329. Which is a medium effect size. Thus we have found enough evidence to say that if eye-contact was present, the silence_duration of a gap is smaller and the effect size is small.

gen gestures_num = .
replace gestures_num = 1 if gestures == "y"
replace gestures_num = 0 if gestures == "n"

gen eyecontact_presence_num = .
replace eyecontact_presence_num = 1 if eyecontact_presence =="y"
replace eyecontact_presence_num = 0 if eyecontact_presence =="n"

anova silence_duration eyecontact_presence_num
regress
// This also shows a p-value lower than 0.05, namely p = 0.002

reg silence_duration i.eyecontact_presence_num

anova silence_duration gestures_num eyecontact_presence_num
regress

anova silence_duration gestures_num eyecontact_presence_num gestures_num#eyecontact_presence_num
regress
// p-value of 0.336, which shows thus that there is not enough evidence found to conclude that there is a significant effect between silence duration and both gestures and eyecontact presence. Hence, we reject the H2.

encode gestures_eyecontact, gen(gestures_eyecontact_num)

anova silence_duration i.gestures_eyecontact_num
regress
// p-value of 0.0016, so there is not enough evidence found to conclude that there is a signifanct effect between silence duration and the presence or absence of gestures combined with eyecontact in the sad condition. 
