// Observation predicates
$Conditions1 := { S1 = 0 and S2 = 1};
$Conditions2 := { S1 = 1 and S2 = 1};
$Expression1 := {A = 1 and B = 1 and C = 1};
$Expression2 := {A = 0 and B = 1 and C = 1};
$Expression3 := {A = 1 and B = 1 and C = 0};
$Expression4 := {A = 1 and B = 0 and C = 0};

// Observations
#Experiment1[0] |= $Conditions1;
#Experiment1[0] |= $Expression1;
#Experiment1[18] |= $Expression2;

#Experiment2[0] |= $Conditions2;
#Experiment2[0] |= $Expression2;
#Experiment2[18] |= $Expression1;

#Experiment3[0] |= $Conditions2;
#Experiment3[0] |= $Expression1;
#Experiment3[18] |= $Expression2;


#Experiment4[0] |= $Conditions1;
#Experiment4[0] |= $Expression1;
#Experiment4[18] |= $Expression3;

#Experiment5[0] |= $Expression2;
#Experiment5[18] |= $Expression4;