# APC524 Final Project

[![Build Status](https://travis-ci.com/PrincetonUniversity/apc_524_robotic_path_planning.svg?token=s3m3VSxYkggvyCzmtTnX&branch=development)](https://travis-ci.com/PrincetonUniversity/apc_524_robotic_path_planning)

# Team: Edvard Bruun, Vivek Kumar, Jessica Flores

# Title: Robotic Path Planning Algorithm

## Executing Program

Please see the Sphinx documentation (Section: Program Execution) for instructions on how to execute the program.

## Creating Documentation Files

Ensure that ghostscript installed if ps2pdf error for latex `make`

```
https://command-not-found.com/ps2pdf
```

### Design Document

```
$ cd apc_524_robotic_path_planning/documentation/design_document
$ make
```

### UML class diagram

* UML Class Diagram: Uses tikz-uml package for LaTeX. Documentation can be found at: https://perso.ensta-paris.fr/~kielbasi/tikzuml/var/files/html/web-tikz-uml-userguide.html

```
$ cd apc_524_robotic_path_planning/documentation/uml_class_diagram
$ make
```

### Project report

```
$ cd apc_524_robotic_path_planning/documentation/final_report
$ make
```

### Sphinx documentation

Creates all out in `build` directory

for PDF:
```
$ cd apc_524_robotic_path_planning/documentation/doc_spinx
$ make latexpdf
```

for html:
```
$ cd apc_524_robotic_path_planning/documentation/doc_spinx
$ make html
```





  
