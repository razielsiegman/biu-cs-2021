import NAE.NAE;

import java.io.*;
import java.util.*;
import java.nio.file.*;

public class MinContradictions {

    private class Experiment{
        private String experimentName;
        private Set<String> constraintSet;
        private String constraints;

        public Experiment(String experimentName){
            this.experimentName = experimentName;
            this.constraintSet = new HashSet<String>();
        }

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
    private String newSpec;
    private String mode;
    private String currentSpec;
    private String specTemplate;
    private Map<String, Experiment> experiments;
    private Set<HashSet<Experiment>> expSolutionSets;
    private Set<HashSet<String>> conSolutionSets;
    private Runtime rt;
    private boolean constraints;

    public static void main(String[] args) throws IOException {
        if(args[1].contains("ltl") || args[1].contains("ctl")) {
            throw new IllegalArgumentException("Minimal solution sets cannot be found for temporal logic models");
        }
        //Boot up NAE
        Runtime rt = Runtime.getRuntime();
        Process pr1 = rt.exec("javac NAE/*.java validate/*.java");
        Process pr2 = rt.exec("jar cvfm NAE.jar NAE/manifest.txt NAE/*.class validate/*.class");
        MinContradictions mc = new MinContradictions();
        System.out.println("Would you like minimal constraint sets in addition to minimal experiment sets? (\"y\" for yes, \"n\" for no)");
        Scanner scanner = new Scanner(System.in);
        String s = scanner.nextLine();
        if(!s.equals("y") && !s.equals("n")){
            throw new IllegalArgumentException("Input must be a \"y\" or \"n\"");
        }
        if(s.equals("y")){
            mc.constraints = true;
        }
        else{
            mc.constraints = false;
        }
        mc.rt = rt;
        mc.model = args[0];
        mc.newSpec = args[1] + "//..//" + "observations1.spec";
        PrintWriter pr = new PrintWriter(mc.newSpec, "UTF-8");
        String content = Files.readString(Paths.get(args[1]));
        pr.print(content);
        pr.close();
        mc.mode = "time_step";
        mc.experiments = new HashMap<String, Experiment>();
        mc.expSolutionSets = new HashSet<HashSet<Experiment>>();
        mc.conSolutionSets = new HashSet<HashSet<String>>();
        mc.readObservation(mc.newSpec);
        mc.findMinExpSets();
    }

    private void readObservation(String specFileName) throws IOException {
        //Create spec file without experimental observations
        StringBuilder specFileTemplate = new StringBuilder();
        BufferedReader br = new BufferedReader(new FileReader(specFileName));
        String line;
        while ((line = br.readLine()) != null) {
            String experimentName;
            //If line is experimental observation, add to experiment object, otherwise add to spec template
            if (line.contains("#")) {
                experimentName = line.substring(line.indexOf("#"), line.indexOf("["));
                if(!experiments.containsKey(experimentName)){
                    experiments.put(experimentName, new Experiment(experimentName));
                }
                experiments.get(experimentName).addConstraint(line);
            } else {
                specFileTemplate.append(line + "\n");
            }
        }
        this.specTemplate = specFileTemplate.toString();

        //For each experiment, create constraint string from full set
        for(Experiment e : experiments.values()){
            StringBuilder experimentSpec = new StringBuilder();
            for(String s : e.getConstraintSet()){
                experimentSpec.append(s + "\n");
            }
            e.putConstraints(experimentSpec.toString());
        }
    }

    private void findMinExpSets() throws IOException {
        //All experiments being checked in current iteration (The complement of the union of all solution sets)
        Set<Experiment> currentExperiments = new HashSet<>(experiments.values());
        //subtraction of every set not in the current solution from currentExperiments
        Set<Experiment> remainingExperiments = new HashSet<>(experiments.values());

        //Check to make sure there is another solution set that exists
        while(this.runNAE(this.newSpec, this.model, this.rt, this.mode) == true){
            //For each element in currentExperiments: Build the spec file from scratch without current element.  If contradiction still exists, continue.  Else, put element back in set and continue.
            for(Experiment e : currentExperiments){
                remainingExperiments.remove(e);
                buildCurrentSpecExp(remainingExperiments);
                if(this.runNAE(this.newSpec, this.model, this.rt, this.mode)){
                    continue;
                }
                else{
                    remainingExperiments.add(e);
                }
            }
            expSolutionSets.add(new HashSet<Experiment>(remainingExperiments));
            System.out.print("Experiment Set: " + remainingExperiments + "\n");
            if(this.constraints){
                this.findMinConSets(new HashSet<Experiment>(remainingExperiments));
            }
            currentExperiments.removeAll(remainingExperiments);
            remainingExperiments.clear();
            remainingExperiments.addAll(currentExperiments);
            buildCurrentSpecExp(remainingExperiments);
        }
    }

    private void findMinConSets(Set<Experiment> exps) throws IOException {
        //All experiments being checked in current iteration (The complement of the union of all solution sets)
        Set<String> currentConstraints = new HashSet<String>();
        for(Experiment e: exps){
            currentConstraints.addAll(e.getConstraintSet());
        }
        //subtraction of every set not in the current solution from currentExperiments
        Set<String> remainingConstraints = new HashSet<String>(currentConstraints);
        buildCurrentSpecCon(remainingConstraints);
        //Check to make sure there is another solution set that exists
        while(this.runNAE(this.newSpec, this.model, this.rt, this.mode) == true){
            //For each element in currentConstraints: Build the spec file from scratch without current element.  If contradiction still exists, continue.  Else, put element back in set and continue.
            for(String s : currentConstraints){
                remainingConstraints.remove(s);
                buildCurrentSpecCon(remainingConstraints);
            if(this.runNAE(this.newSpec, this.model, this.rt, this.mode) == true){
                    continue;
                }
                else{
                remainingConstraints.add(s);
                }
            }
            conSolutionSets.add(new HashSet<String>(remainingConstraints));
            System.out.print("Constraint Set:" + "\n" + remainingConstraints + "\n");
            currentConstraints.removeAll(remainingConstraints);
            remainingConstraints.clear();
            remainingConstraints.addAll(currentConstraints);
            buildCurrentSpecCon(remainingConstraints);
        }
    }

    private void buildCurrentSpecExp(Set<Experiment> experimentSet) throws IOException{
        StringBuilder spec = new StringBuilder();
        spec.append(specTemplate);
        for(Experiment experiment : experimentSet){
            spec.append(experiment.getConstraints() + "\n");
        }
        PrintWriter pr = new PrintWriter(this.newSpec, "UTF-8");
        pr.print(spec.toString());
        pr.close();
    }

    private void buildCurrentSpecCon(Set<String> constraintSet) throws IOException{
        StringBuilder spec = new StringBuilder();
        spec.append(specTemplate);
        for(String s : constraintSet){
            spec.append(s + "\n");
        }
        PrintWriter pr = new PrintWriter(this.newSpec, "UTF-8");
        pr.print(spec.toString());
        pr.close();
    }

    private boolean runNAE(String completeSpecFile, String modelFile, Runtime rt, String mode) throws IOException {
        Process pr = rt.exec("java -jar NAE.jar 1 " + modelFile + " " + completeSpecFile + " " + mode);
        BufferedReader reader = new BufferedReader(new InputStreamReader(pr.getInputStream()));
        return (reader.readLine().equals("No Solutions Found"));
    }
}