// Observation predicates
$None := {Gene0 = 0 and Gene1 = 0 and Gene2 = 0};
$Zero := {Gene0 = 1 and Gene1 = 0 and Gene2 = 0};
$One := {Gene0 = 0 and Gene1 = 1 and Gene2 = 0};
$Two := {Gene0 = 0 and Gene1 = 0 and Gene2 = 1};
$ZeroAndOne := {Gene0 = 1 and Gene1 = 1 and Gene2 = 0};
$ZeroAndTwo := {Gene0 = 1 and Gene1 = 0 and Gene2 = 1};
$OneAndTwo := {Gene0 = 0 and Gene1 = 1 and Gene2 = 1};
$All := {Gene0 = 1 and Gene1 = 1 and Gene2 = 1};


// Observations
#Experiment1[0] |= $ZeroAndOne;
#Experiment1[1] |= $None;
#Experiment1[2] |= $Zero;

#Experiment2[0] |= $One;
#Experiment2[1] |= $Two;
#Experiment2[2] |= $None;

#Experiment3[0] |= $ZeroAndTwo;
#Experiment3[1] |= $One;

#Experiment4[0] |= $OneAndTwo;
#Experiment4[1] |= $Two;

#Experiment5[0] |= $All;
#Experiment5[1] |= $One;
