// Observation predicates
$Expression1 := {Gene0 = 1 and Gene1 = 1 and Gene2 = 0};
$Expression2 := {Gene0 = 0 and Gene1 = 0 and Gene2 = 0};
$Expression3 := {Gene0 = 1 and Gene1 = 0 and Gene2 = 0};

// Observations
#Experiment1[0] |= $Expression1;
#Experiment1[1] |= $Expression2;
#Experiment1[2] |= $Expression3;
