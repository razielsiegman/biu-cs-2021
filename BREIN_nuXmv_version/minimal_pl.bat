rem building NAE...

javac NAE\*.java validate\*.java
jar cvfm NAE.jar NAE\manifest.txt NAE\*.class validate\*.class

rem Running time_step models:

powershell -Command "Measure-Command { java -jar NAE.jar 1 TestModels\minimal_pl\model.net TestModels\minimal_pl\observations.spec time_step | Out-Default}"
