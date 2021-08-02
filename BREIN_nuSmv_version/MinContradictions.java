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
    private String specTemplate;
    private Map<String, Experiment> experiments;
    private Set<HashSet<Experiment>> expSolutionSets;
    private Set<HashSet<String>> conSolutionSets;
    private Runtime rt;
    private boolean constraints;

    /**
     * The program, in its current state, must be generated from the main method.
     * Note: all file paths are assumed to be relative.
     *
     * @param  args the model.net file, observation.spec file, and algorithm
     * mode, respectively
     */
    public static void main(String[] args) throws IOException {
        if(args[1].contains("ltl") || args[1].contains("ctl")) {
            throw new IllegalArgumentException("Minimal solution sets cannot be found for temporal logic models");
        }
        if(!args[2].equals("e") && !args[2].equals("c") && !args[2].equals("ec")){
            throw new IllegalArgumentException("Algorithm type must be a \"e\" or \"ec\" or \"c\"");
        }
        //Boot up NAE
        Runtime rt = Runtime.getRuntime();
        Process pr1 = rt.exec("javac NAE/*.java validate/*.java");
        Process pr2 = rt.exec("jar cvfm NAE.jar NAE/manifest.txt NAE/*.class validate/*.class");
        new MinContradictions(rt, args[0], args[1], args[2]);
    }

    /**
     * Class constructor specifying user args.
     *
     * @param  algMode specifies whether the algorithm detects minimal sets:
     *                  a) of experiments; b) of experiments on the constraint
     *                  level of granularity; c) of constraints, irrespective
     *                  of experiments
     * @param  rt      runtime environment with booted NAE program
     * @param  model   model.net file path
     * @param  newSpec observation1.spec file path, to be edited in each
     *                 iteration of the program
     */
    private MinContradictions(Runtime rt, String model, String originalSpec, String algMode) throws IOException{
        if(algMode.equals("ec")){
            this.constraints = true;
        }
        this.rt = rt;
        this.model = model;
        //Copy spec file to prevent tampering with original
        this.newSpec = originalSpec + "//..//" + "observations1.spec";
        PrintWriter pr = new PrintWriter(this.newSpec, "UTF-8");
        String content = Files.readString(Paths.get(originalSpec));
        pr.print(content);
        pr.close();

        this.mode = "time_step";
        this.experiments = new HashMap<String, Experiment>();
        this.expSolutionSets = new HashSet<HashSet<Experiment>>();
        this.conSolutionSets = new HashSet<HashSet<String>>();

        //Run Program
        this.readObservation(this.newSpec);
        if(algMode.equals("c")) {
            this.findMinConSets(new HashSet<Experiment>(this.experiments.values()));
        }
        else{
            this.findMinExpSets();
        }
    }

    /**
     * Parses the spec file into its macros, stored as specTemplate, and its
     * experimental data.
     *
     * @param  specFileName file path of spec file to be parsed
     */
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

    /**
     *  If the user either specified 'e' or 'ec' as the algorithm mode, find
     *  minimal sets of contradictory experiments.
     * @see #MinContradictions
     */
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

    /**
     *  If the user either specified 'ec' or 'c' as the algorithm mode, find
     *  minimal sets of contradictory constraints.
     *  <p>
     *  In case of algorithm mode 'c', all experiments will be inputted, and in
     *  case of mode 'ec', one minimal set of contradictory experiments will be
     *  inputted.
     *
     * @param  exps the set of experiments that contain the desired constraints
     * @see #MinContradictions
     */
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

    /**
     *  Given a set of experiments, rebuild the observation1.spec file to only
     *  contain given experiments (where each experiment can contain many
     *  constraints).
     *
     * @param experimentSet the set of experiments for the spec file
     */
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

    /**
     *  Given a set of constraints, rebuild the observation1.spec file to only
     *  contain given constraints.
     *
     * @param constraintSet the set of constraints for the spec file
     */
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

    /**
     *  Executes NAE.
     *
     * @param completeSpecFile spec file path containing specTemplate as well
     *                         as a set of constraints
     * @param modelFile        model.net file path
     * @param rt               runtime environment with booted NAE program
     * @param mode             BRE:IN mode, which must be 'time_step' when
     *                         finding minimal sets of contradictory data
     */
    private boolean runNAE(String completeSpecFile, String modelFile, Runtime rt, String mode) throws IOException {
        Process pr = rt.exec("java -jar NAE.jar 1 " + modelFile + " " + completeSpecFile + " " + mode);
        BufferedReader reader = new BufferedReader(new InputStreamReader(pr.getInputStream()));
        return (reader.readLine().equals("No Solutions Found"));
    }
}