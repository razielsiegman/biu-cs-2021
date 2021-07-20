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
#Experiment1[0] |= $ZeroAndOne and
#Experiment1[1] |= $None and
#Experiment1[2] |= $Zero and
fixpoint(#Experiment1[2]);