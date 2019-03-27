import os
# Function that returns the number of lines from a given file
###########################################################################
def nb_lines(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
##########################################################################


# Function that returns the number of files from a given directory
###########################################################################
def nb_files (directory):
    return(len(os.listdir(directory)))

##########################################################################

# Function that return an alphabetically ordered list
# of the files included in a given directory
###########################################################################
def ordering_files(directory):
    return(sorted(os.listdir(directory)))
##########################################################################
