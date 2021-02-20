# calc-gpa
Simple CLI program to calculate GPA, with support for some queries.

# usage
`calcgpa.py [-h] [-y YYYY] [-ub 0-100] [-lb 0-100] [-s A|B|C] datafile`
- `-h` is for displaying help
- `-y` is for selecting courses of a specific year, e.g: `-y 2018`
- `-s` is for selecting courses of a specific semester, e.g: `-s A`
- `-ub` & `lb` is for selecting courses whose grades are withing a specific range, e.g. : `-lb 70 -ub 100` means the grade should be above 70 & below 100
- `datafile` is the file that contains the info about the courses (most importantly, their grades).

The program scans the datafile, filters some courses according to the specified query, then prints the filtered courses and the calculated GPA in a pretty format.

# examples
## datafile examples

Short example for the contents of `datafile`:
```
 Sem  | Course ID | Pts |            Course Name             | Grade
______|___________|_____|____________________________________|______
2018B | 0368-1118 |  6  | Discrete Math                      |  98
------|-----------|-----|------------------------------------|------
2019A | 0368-1105 |  6  | Extended Intro To Computer Science |  67
2019B | 0366-1111 |  7  | Linear Algebra 1a                  |  100
------|-----------|-----|------------------------------------|------
2020A | 0366-1101 |  7  | Calculus 1a                        |  78
2020A | 0368-2157 |  4  | Software 1                         |  89
2020B | 0366-2010 |  5  | Intro To Probability               |  ???
2020B | 0368-2158 |  4  | Data Structures                    |  ???
```
This example makes use of the program's ignore policy: In detail, the 1st line of the input file is always ignored, and so is every line that begins with `'_'`, `'-'` or `'#'`. courses with grade value `???` will also be ignored.

Therefore, the following `datafile` contents are parsed equivalently to the previous example, albeit less pretty:
```
# first line is ignored
2018B|0368-1118|6|DiscreteMath|98
2019A|0368-1105|6|ExtendedIntroToComputerScience|67
2019B|0366-1111|7|LinearAlgebra1a|100
2020A|0366-1101|7|Calculus1a|78
2020A|0368-2157|4|Software1|89
2020B|0366-2010|5|IntroToProbability|???
2020B|0368-2158|4|DataStructures|???
```

## output example
for the above `datafile` contents:
```
> python calcgpa.py -s B -lb 80 datafile.txt
 Sem  | Course ID | Pts |   Course Name   | Grade
______|___________|_____|_________________|______
2018B | 0368-1118 |  6  | DiscreteMath    | 98
2019B | 0366-1111 |  7  | LinearAlgebra1a | 100

GPA: 99.077
```
