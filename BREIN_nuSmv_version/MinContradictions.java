import java.io.*;
import java.util.*;

public class MinContradictions {

    private class Experiment{
        private String experimentName;
        private Set<String> constraintSet;
        private String constraints;

        private void addConstraint(String constraint){
            constraintSet.add(constraint);
        }

        public Set<String> getConstraintSet(){
            return constraintSet;
        }

        public String getConstraints(){
            return constraints;
        }

        public void putConstraints(String constraints){
            this.constraints = constraints;
        }

        @Override
        public int hashCode(){
            return this.experimentName.hashCode();
        }

        @Override
        public boolean equals(Object o){
            Experiment e = (Experiment)o;
            if(e.experimentName.equals(this.experimentName)){
                return true;
            }
            return false;
        }

        @Override
        public String toString(){
            return experimentName;
        }
    }


    private String model;
    private String mode;
    private String currentSpec;
    private String specTemplate;
    private Map<String, Experiment> experiments;
    private Set<HashSet<Experiment>> solutionSets;

    public static void main(String[] args) throws IOException {
        MinContradictions mc = new MinContradictions();
        mc.model = args[0];
        mc.currentSpec = args[1];
        mc.mode = args[2];
        mc.experiments = new HashMap<String, Experiment>();
        mc.solutionSets = new HashSet<HashSet<Experiment>>();
        mc.readObservation(mc.currentSpec);
        mc.findMinSets();
    }

    private void updateSolutionSets(Set<Experiment> solution){
        solutionSets.add((HashSet)solution);
    }

    private void readObservation(String specFileName) throws IOException {
        //Create spec file without experimental observations
        StringBuilder specFileTemplate = new StringBuilder();
        BufferedReader br = new BufferedReader(new FileReader(System.getProperty("user.dir") + "/src/main/java/TestModels/test_model/" + specFileName));
        String line;
        while ((line = br.readLine()) != null) {
            String experimentNumber;
            //If line is experimental observation, add to experiment object, otherwise add to spec template
            if (line.contains("#Experiment")) {
                experimentNumber = line.substring(0, line.indexOf("["));
                Experiment e = experiments.get(experimentNumber);
                e.addConstraint(line);
            } else {
                specFileTemplate.append(line + "\n");
            }
        }
        this.specTemplate = specFileTemplate.toString();

        //For each experiment, create constraint string from full set
        for(Experiment e : experiments.values()){
            StringBuilder experimentSpec = new StringBuilder();
            for(String s : e.getConstraintSet()){
                experimentSpec.append(s);
            }
            e.putConstraints(experimentSpec.toString());
        }
    }

    private void findMinSets() throws IOException {
        //Boot up NAE
        Runtime rt = Runtime.getRuntime();
        Process pr1 = rt.exec("javac NAE/*.java validate/*.java");
        Process pr2 = rt.exec("jar cvfm NAE.jar NAE/manifest.txt NAE/*.class validate/*.class");

        //All experiments being checked in current iteration (The complement of the union of all solution sets)
        Set<Experiment> currentExperiments = new HashSet<>(experiments.values());
        //subtraction of every set not in the current solution from currentExperiments
        Set<Experiment> remainingExperiments = new HashSet<>(experiments.values());

        //Check to make sure there is another solution set that exists
        while(this.runNAE(this.currentSpec, this.model, rt, this.mode) == true){
            //For each element in currentExperiments: Build the spec file from scratch without current element.  If contradiction still exists, continue.  Else, put element back in set and continue.
            for(Experiment e : currentExperiments){
                remainingExperiments.remove(e);
                buildCurrentSpec(remainingExperiments);
                if(this.runNAE(this.currentSpec, this.model, rt, this.mode) == true){
                    continue;
                }
                else{
                    remainingExperiments.add(e);
                }
            }
            updateSolutionSets(remainingExperiments);
            currentExperiments.remove(remainingExperiments);
            remainingExperiments.clear();
            remainingExperiments.addAll(currentExperiments);
        }
        System.out.println(solutionSets.toString());
    }

    private void buildCurrentSpec(Set<Experiment> experimentSet){
        StringBuilder spec = new StringBuilder();
        spec.append(specTemplate);
        for(Experiment experiment : experimentSet){
            spec.append(experiment.getConstraints());
        }
        this.currentSpec = spec.toString();
    }

    private boolean runNAE(String completeSpecFile, String modelFile, Runtime rt, String mode) throws IOException {
        Process pr = rt.exec("java -jar NAE.jar 1 " + modelFile + " " + completeSpecFile + " " + mode);
        BufferedReader reader=new BufferedReader(new InputStreamReader(
                pr.getInputStream()));
        return (reader.readLine().equals("No Solutions Found"));
    }
}