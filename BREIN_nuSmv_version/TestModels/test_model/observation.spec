$Condition0 := { S0 = 1};
$Condition1 := { S1 = 1};
$Condition2 := { S2 = 1};
$Condition3 := { S3 = 1};

$NoCondition1 := { S1 = 0};
$NoCondition2 := { S2 = 0};
$NoCondition3 := { S3 = 0};

$DTCContact := {
 DTC = 1 and
 StemcellFate  = 1 
};

$ContactConditions := {
 LAG2	= 1 and
 APX1	= 1 and
 GLP1	= 1 and
 LAG1	= 0 and
 LST1 	= 0 and
 SYGL1	= 0 and
 FBF1B	= 0 and
 FBF2	= 0 and
 FBF1U	= 1 and
 GLP1ICD	= 0 and
 SEL8	= 0 and
 HOP1 	= 0 and
 SEL12 	= 0 and
 SEL10	= 0 and
 GLD1	= 0 and
 GLD2	= 0 and
 GLD3	= 0 and
 NOS3	= 0 and
 AxisandSCprotein = 0 and
 SCFPROM1 = 0 and
 CYE1CDK2	= 1 and
 MeioticDev  = 0 
 and StemcellFate  = 1 
};

$NoKnockOuts := {
 KO(GLP1) = 0 and
 KO(SYGL1) = 0 and
 KO(LST1) = 0 and
 KO(GLD1) = 0 and
 KO(GLD2) = 0 
};

$NoOverExpression := {
 FE(GLP1)=0 and
 FE(LST1)=0 and
 FE(SYGL1)=0
};

 $DTCConstant := {
 DTC  = 1 and
 MeioticDev  = 0 
 and StemcellFate  = 1 
 };

 $GLD1Pathway := {
 FBF1B	= 0 and
 GLD1	= 1 and
 MeioticDev  = 1 
 and StemcellFate  = 0 
 };
 
 $SCFPROM1Pathway := {
 FBF1B	= 0 and
 SCFPROM1 = 1 and
 MeioticDev  = 1 
 and StemcellFate  = 0 
};

 $AxisandSCproteinPathway := {
 FBF1B	= 0 and
 FBF2	= 0 and
 AxisandSCprotein = 1 and
 MeioticDev  = 1 
};

 $GLD2Pathway := { 
 FBF1B	= 0 and
 FBF1U	= 1 and
 GLD3	= 1 and
 GLD2	= 1 and
 MeioticDev  = 1 
 and StemcellFate  = 0 
 };
 
$GLP1KnockOutStep0 := {
 GLP1	= 0 };
 
$LST1SYGL1KnockOutStep0 := {
 LST1 	= 0 and
 SYGL1	= 0 
 };
 
$GLD1GLD2KnockOutStep0 := {
 GLD1 	= 0 and
 GLD2	= 0 
 };
 
$LST1KnockOutStep0 := {
 LST1 	= 0 };
 
$SYGL1KnockOutStep0 := {
 SYGL1 	= 0 };
 
$GLP1OverExpressionStep0 := {
 GLP1	= 1 };
 
$LST1OverExpressionStep0 := {
 LST1 	= 1 };
 
$SYGL1OverExpressionStep0 := {
 SYGL1 	= 1 };
 
$GLP1KnockOutConditions := {
 LAG2	= 1 and
 APX1	= 1 and
 GLP1	= 0 and
 LAG1	= 0 and
 LST1 	= 0 and
 SYGL1	= 0 and
 FBF1B	= 0 and
 FBF2	= 0 and
 FBF1U	= 1 and
 GLP1ICD	= 0 and
 SEL8	= 0 and
 HOP1 	= 0 and
 SEL12 	= 0 and
 SEL10	= 0 and
 GLD1	= 0 and
 GLD2	= 0 and
 GLD3	= 0 and
 NOS3	= 0 and
 AxisandSCprotein = 0 and
 SCFPROM1 = 0 and
 CYE1CDK2	= 1 and
 MeioticDev  = 0 
 and StemcellFate  = 1 
};

$LST1SYGL1KnockOutConditions := {
 LST1 	= 0 and
 SYGL1	= 0 
};

$GLP1GeneKnockOut := {
 KO(GLP1) = 1 and
 KO(SYGL1) = 0 and
 KO(LST1) = 0 and
 KO(GLD1) = 0 and
 KO(GLD2) = 0 
};

$LST1SYGL1GeneKnockOut := {
 KO(GLP1) = 0 and
 KO(SYGL1) = 1 and
 KO(LST1) = 1 and
 KO(GLD1) = 0 and
 KO(GLD2) = 0 
};

$GLD1GLD2GeneKnockOut := {
 KO(GLP1) = 0 and
 KO(SYGL1) = 0 and
 KO(LST1) = 0 and
 KO(GLD1) = 1 and
 KO(GLD2) = 1 
};

$LST1GeneKnockOut := {
 KO(GLP1) = 0 and
 KO(SYGL1) = 0 and
 KO(LST1) = 1 and
 KO(GLD1) = 0 and
 KO(GLD2) = 0 
}; 

$SYGL1GeneKnockOut := {
 KO(GLP1) = 0 and
 KO(SYGL1) = 1 and
 KO(LST1) = 0 and
 KO(GLD1) = 0 and
 KO(GLD2) = 0 
};

$FinalStateGLP1ZeroExpression := {
 GLP1  = 0 and
 MeioticDev  = 1 
};

$FinalStateLST1SYGL1ZeroExpression := {
 LST1 = 0 and
 SYGL1 = 0 and
 MeioticDev  = 1 
};

$FinalStateGLD1GLD2ZeroExpression := {
 GLD1	= 0 and
 GLD2	= 0 and
 MeioticDev  = 0 
};

$FinalStateLST1ZeroExpression := {
 LST1 = 0 and
 MeioticDev  = 0 and
 StemcellFate  = 1 
};

$FinalStateSYGL1ZeroExpression := {
 SYGL1 = 0 and
 MeioticDev  = 0 and
 StemcellFate  = 1
};

$GLP1OverExpressionConditions := {
 LAG2	= 1 and
 APX1	= 1 and
 GLP1	= 1 
};

$LST1OverExpressionConditions := {
 LST1 = 1 and
 FBF1B = 1 
 };

$SYGL1OverExpressionConditions := {
 SYGL1 = 1 and
 FBF1B = 1 
};
 
$GLP1GeneOverExpression := {
 FE(GLP1) = 1 and
 FE(LST1) = 0 and
 FE(SYGL1) = 0
};

$LST1GeneOverExpression := {
 FE(GLP1) = 0 and
 FE(LST1) = 1 and
 FE(SYGL1) = 0
};

$SYGL1GeneOverExpression := {
 FE(GLP1) = 0 and
 FE(LST1) = 0 and
 FE(SYGL1) = 1 
};

$GLD1GeneOverExpression := {
 FE(GLP1) = 0 and
 FE(LST1) = 0 and
 FE(SYGL1) = 0 
};

$FinalStateGLP1OverExpression := {
 GLP1 = 1 and
 MeioticDev  = 0 
};

$FinalStateLST1OverExpression := {
 LST1 = 1 and
 MeioticDev  = 0
};

$FinalStateSYGL1OverExpression := {
 SYGL1	= 1 and
 MeioticDev  = 0 
};

//experimental observations

//DTC Constitutive Activity
(#ExperimentZero[0] |= $Condition0)  and
(#ExperimentZero[0] |= $DTCContact)  and
(#ExperimentZero[0] |= $NoCondition1)  and
(#ExperimentZero[0] |= $NoCondition2)  and
(#ExperimentZero[0] |= $NoCondition3)  and
(#ExperimentZero[1] |= $ContactConditions)and
(#ExperimentZero[1] |= $NoKnockOuts) and
(#ExperimentZero[1] |= $NoOverExpression) and
(#ExperimentZero[17] |= $DTCConstant);

// GLP1 KO
(#ExperimentFive[0] |= $Condition0)  and
(#ExperimentFive[0] |= $DTCContact)  and
(#ExperimentFive[0] |= $NoCondition1)  and
(#ExperimentFive[0] |= $NoCondition2)  and
(#ExperimentFive[0] |= $NoCondition3)  and
(#ExperimentFive[1] |= $GLP1KnockOutConditions) and
(#ExperimentFive[1] |= $GLP1GeneKnockOut) and
(#ExperimentFive[1] |= $NoOverExpression) and
(#ExperimentFive[17] |= $FinalStateGLP1ZeroExpression);

// LST1SYGL1 KO
(#ExperimentSix[0] |= $Condition0)  and
(#ExperimentSix[0] |= $DTCContact)  and
(#ExperimentSix[0] |= $LST1SYGL1KnockOutStep0)  and
(#ExperimentSix[0] |= $NoCondition1)  and
(#ExperimentSix[0] |= $NoCondition2)  and
(#ExperimentSix[0] |= $NoCondition3)  and
(#ExperimentSix[1] |= $LST1SYGL1KnockOutConditions) and
(#ExperimentSix[1] |= $LST1SYGL1GeneKnockOut) and
(#ExperimentSix[1] |= $NoOverExpression) and
(#ExperimentSix[17] |= $FinalStateLST1SYGL1ZeroExpression);

// GLD1GLD2 KO
(#ExperimentSeven[0] |= $Condition0) and
(#ExperimentSeven[0] |= $DTCContact)  and
(#ExperimentSeven[0] |= $GLD1GLD2KnockOutStep0)  and
(#ExperimentSeven[0] |= $NoCondition1)  and
(#ExperimentSeven[0] |= $NoCondition2)  and
(#ExperimentSeven[0] |= $NoCondition3)  and
(#ExperimentSeven[1] |= $ContactConditions) and
(#ExperimentSeven[1] |= $GLD1GLD2GeneKnockOut) and
(#ExperimentSeven[1] |= $NoOverExpression) and
(#ExperimentSeven[17] |= $FinalStateGLD1GLD2ZeroExpression);

// LST1 KO
(#ExperimentEight[0] |= $Condition0) and
(#ExperimentEight[0] |= $DTCContact)  and
(#ExperimentEight[0] |= $LST1KnockOutStep0)  and
(#ExperimentEight[0] |= $NoCondition1)  and
(#ExperimentEight[0] |= $NoCondition2)  and
(#ExperimentEight[0] |= $NoCondition3)  and
(#ExperimentEight[1] |= $ContactConditions) and
(#ExperimentEight[1] |= $LST1GeneKnockOut) and
(#ExperimentEight[1] |= $NoOverExpression) and
(#ExperimentEight[17] |= $FinalStateLST1ZeroExpression);

// SYGL1 KO
(#ExperimentNine[0] |= $Condition0) and
(#ExperimentNine[0] |= $DTCContact)  and
(#ExperimentNine[0] |= $SYGL1KnockOutStep0)  and
(#ExperimentNine[0] |= $NoCondition1)  and
(#ExperimentNine[0] |= $NoCondition2)  and
(#ExperimentNine[0] |= $NoCondition3)  and
(#ExperimentNine[1] |= $ContactConditions) and
(#ExperimentNine[1] |= $SYGL1GeneKnockOut) and
(#ExperimentNine[1] |= $NoOverExpression) and
(#ExperimentNine[17] |= $FinalStateSYGL1ZeroExpression);

// GLP1 OE
(#ExperimentTen[0] |= $Condition0) and
(#ExperimentTen[0] |= $DTCContact)  and
(#ExperimentTen[0] |= $GLP1OverExpressionStep0)  and
(#ExperimentTen[0] |= $NoCondition1)  and
(#ExperimentTen[0] |= $NoCondition2)  and
(#ExperimentTen[0] |= $NoCondition3)  and
(#ExperimentTen[1] |= $GLP1OverExpressionConditions);
(#ExperimentTen[1] |= $NoKnockOuts)and
(#ExperimentTen[1] |= $GLP1GeneOverExpression);
(#ExperimentTen[17] |= $FinalStateGLP1OverExpression);

// LST1 OE
(#ExperimentEleven[0] |= $Condition0) and
(#ExperimentEleven[0] |= $DTCContact)  and
(#ExperimentEleven[0] |= $LST1OverExpressionStep0)  and
(#ExperimentEleven[0] |= $NoCondition1)  and
(#ExperimentEleven[0] |= $NoCondition2)  and
(#ExperimentEleven[0] |= $NoCondition3)  and
(#ExperimentEleven[1] |= $LST1OverExpressionConditions) and
(#ExperimentEleven[1] |= $NoKnockOuts)and
(#ExperimentEleven[1] |= $LST1GeneOverExpression);
(#ExperimentEleven[17] |= $FinalStateLST1OverExpression);

// SYGL1 OE
(#ExperimentTwelve[0] |= $Condition0) and
(#ExperimentTwelve[0] |= $DTCContact)  and
(#ExperimentTwelve[0] |= $SYGL1OverExpressionStep0)  and
(#ExperimentTwelve[0] |= $NoCondition1)  and
(#ExperimentTwelve[0] |= $NoCondition2)  and
(#ExperimentTwelve[0] |= $NoCondition3)  and
(#ExperimentTwelve[2] |= $SYGL1OverExpressionConditions) and
(#ExperimentTwelve[2] |= $NoKnockOuts)and
(#ExperimentTwelve[2] |= $SYGL1GeneOverExpression);
(#ExperimentTwelve[17] |= $FinalStateSYGL1OverExpression);