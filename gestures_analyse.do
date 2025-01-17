clear all
set more off
use "C:\Users\20212599\OneDrive - TU Eindhoven\Documents\GitHub\BEP_data_analyse_Carmen_K-hler\Data experimenten\Data_gestures.dta"

sum silence_duration if gestures == "y"
// obs = 55
// mean = 1.356364
// sd = 0.8706668
// min = .1
// max = 3.6

sum silence_duration if gestures == "n"
// obs = 130
// mean = 1.63
// sd = .8563172
// min = .2
// max = 3.9

// Let's first test whether the data is normally distributed
swilk silence_duration if gestures=="y" // p = 0.01322
swilk silence_duration if gestures=="n" // p = 0.00414
sktest silence_duration if gestures=="y" // p = 0.0738
sktest silence_duration if gestures=="n" // p = 0.0657
// We need to tranform the variables

ladder silence_duration if gestures=="y"
ladder silence_duration if gestures=="n"
// Only when using the square of the silence_duration, we can find p-values that are bigger than 0.05. Thus, we will transform the variables to log variables.

gen squaresilence_duration = (silence_duration)^2

// I will test whether it indeeds shows that the data is now normally distributed
swilk squaresilence_duration if gestures=="y" // p = 0.00000
swilk squaresilence_duration if gestures=="n" //  p = 0.00000
sktest squaresilence_duration if gestures=="y" // p = 0.00000
sktest squaresilence_duration if gestures=="n" // p = 0.00000
// Normality is still rejected.

ladder silence_duration if gestures=="y"
ladder silence_duration if gestures=="n"
// There are no other options according to this test.

ranksum silence_duration, by(gestures)
// p = 0.0342, which is smaller than 0.05 and therefore H0 is supported.
median silence_duration, by(gestures)
// p = 0.244, which is bigger than 0.05, and therefore H0 is rejected.
// We use the most strict test, so we decide to use the median test.

// We test whether the happy condition makes a difference.
gen gestures_happy = .
replace gestures_happy = 1 if gestures == "y" & nhs == "h"
replace gestures_happy = 0 if gestures == "n" & nhs == "h"

sum silence_duration if gestures_happy == 0
// obs = 30
// mean = 1.436667
// sd = .7672087
// min = .2
// max = 3

sum silence_duration if gestures_happy == 1
// obs = 27
// mean = 1.577778
// sd = .8776425
// min = .2
// max = 3.6

gen gestures_sad = .
replace gestures_sad = 1 if gestures == "y" & nhs == "s"
replace gestures_sad = 0 if gestures == "n" & nhs == "s"

sum silence_duration if gestures_sad == 0
// obs = 32
// mean = 1.828125
// sd = 1.045492
// min = .3
// max = 3.8

sum silence_duration if gestures_sad == 1
// obs = 28
// mean = 1.142857
// sd = .8234654
// min = .1
// max = 3.6


// We do the same for the sad condition.
encode gestures, gen(gestures_num)
encode nhs, gen(emotional_num)


anova silence_duration gestures_num emotional_num
regress
// p happy = 0.930
// p sad = 0.986

anova silence_duration gestures_num emotional_num
regress
predict e, residual
swilk e
sktest e
// Both smaller than 0.05. Thus we reject H0. 


reg silence_duration gestures_num emotional_num, robust
predict e_robust, residual
swilk e_robust
sktest e_robust
// H0: the errors are distributed normally. 
// Both p-values are below 0.05. Thus we reject H0. Unfortunaltely, the errors are still not distributed normally. I will try using bootstrapping. 

/**
reg silence_duration gestures_num emotional_num
bootstrap, reps(2500): reg silence_duration gestures_num emotional_num
predict e_bootstrap, residual
swilk e_bootstrap
sktest e_bootstrap
// H0: the errors are distributed normally. 
// The p-value of the swilk test is smaller than 0.05. Therefore, this is not normally distributed. However, the p-value of the sktest is also below 0.05. Thus, the errors are not distributed normally. 
**/