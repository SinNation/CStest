Assumptions:
CS tests makes some assumptions about the structure of the game code it is testing.
1) It assumes that temporary variables are declared on an earlier row than they care called
2) It assumes that no variable names use symbols that are commonly use in code (e.g. < !)
3) It assumed that a variable with an _ is used in an array and is therefore handled differently
4) Occurences of AND, OR, TRUE, FALSE are deemed to be part of the code and never variable names

