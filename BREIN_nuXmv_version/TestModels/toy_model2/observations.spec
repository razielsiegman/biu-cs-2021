// Observation predicates
$Expression1 := {Gene0 = 1 and Gene1 = 1 and Gene2 = 0 and Gene3 = 0 and Gene4 = 0};
$Expression2 := {Gene0 = 0 and Gene1 = 0 and Gene2 = 0 and Gene3 = 0 and Gene4 = 1};

$Expression3 := {Gene0 = 1 and Gene1 = 1 and Gene2 = 0 and Gene3 = 0 and Gene4 = 0};
$Expression4 := {Gene0 = 0 and Gene1 = 0 and Gene2 = 0 and Gene3 = 0 and Gene4 = 1};
$Expression5 := {Gene0 = 1 and Gene1 = 1 and Gene2 = 0 and Gene3 = 0 and Gene4 = 1};
$Expression6 := {Gene0 = 0 and Gene1 = 1 and Gene2 = 0 and Gene3 = 0 and Gene4 = 1};

// Observations
#Experiment1[0] |= $Expression1;
#Experiment1[1] |= $Expression2;

#Experiment2[0] |= $Expression3;
#Experiment2[1] |= $Expression4;
#Experiment2[2] |= $Expression5;
#Experiment2[3] |= $Expression6;