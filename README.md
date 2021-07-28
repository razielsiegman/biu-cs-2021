# BIU/YU Summer Research Program | Computer Science Students
Under the guidance of Dr. Hillel Kugler

*NOTE: this README assumes prior familiarity with [RE:IN](https://www.microsoft.com/en-us/research/project/reasoning-engine-for-interaction-networks-rein/) and [BRE:IN](https://github.com/kuglerh/BREIN).*

## Projects
### BRE:IN Enhancements
A number of new features and improvements were implemented in the BRE:IN tool itself. These changes are reflected in the "BREIN_nuSmv_version" directory. Changes include:
- Broader support for regulation condition input syntax, i.e. the combination of comma-separated function numbers and '..' separated ranges
- Capability to define uniqueness of solutions by regulatory conditions used (as opposed to concrete interactions)
- Support for showing the user which regulatory conditions were used in each solution, with the option to export solutions to the BooleSim simulator or an R BoolNet network object
- A copy of the BRE:IN tool that utilizes the new [nuXmv](https://nuxmv.fbk.eu/) model checker in place of [NuSMV](https://nusmv.fbk.eu/), located in the "BREIN_nuXmv_version" directory
### Programs Built On Top of BRE:IN
We built 2 programs as abstractions on top of BRE:IN
- Pertubation Predictor
- Minimal-Contradictory-Core Identifier
### Inter-tool Conversions
- [BioTapestry](http://www.biotapestry.org/) (.btp) Conversions
    - BioTapestry2Brein allows conversion from a visual BioTapestry network model to a .net input file to be fed into BRE:IN. This includes support for specification of optional interactions (represented by dotted or dashed lines in BioTapestry)
    - BioTapestry2Rules opens the option of generating a simulatable model using 2 inputs: the network defined in a .btp file, and the regulatory conditions defined in a .rcspec file
- RE:IN to BRE:IN
    - FileSplitter.py script is a simple program to parse a RE:IN input file (.rein) and produce the 2 corresponding input files that BRE:IN expects (namely, .net and .spec)

## Usage


## Details
