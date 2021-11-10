# -Physical-Review-Latex
Parses latex files to the format needed for thesis submission.

Input:
Recives a path to a directory where all latex files are in.
The directory should include a main file, which includes "\input" command, which indicate
the names of the different files which should be included in the output file.

Output:
A single output file (which it's name can be chosen by the user of the program)
which is the original main file supplied, but now instead of "\input{filename}" commands
it contains the content of each one of those files, by the same order they were listed in main file.
At the end of all those files are all the images which appear in the files (this is the needed format), again,
in the same order they appeared in the original files.
