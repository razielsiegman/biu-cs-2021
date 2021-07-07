javac NAE/*.java validate/*.java
jar cvfm NAE.jar NAE/manifest.txt NAE/*.class validate/*.class
java -jar NAE.jar 100 TestModels/toy_model/model.net TestModels/toy_model/observations.spec time_step