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

# Function that verify if the asked folder exists in the given path
# If not, create it, if yes, verify if it is empty, if not -> ERROR
##########################################################################
def verify_folder(directory,folder):
    # folders_list = ordering_files(directory)
    path=directory+folder
    if os.path.exists(path):
        print()
        print("Folder \""+folder+"\" already existing at "+path)
        if(len(os.listdir(path)) != 0):
            print("ERROR : Folder \""+folder+"\" is not empty !")
            erase = input("Do you want to erase the existing content ? Y/N :")
            if erase == 'Y' or erase == 'y' :
                os.makedirs(path, exist_ok=True)
                print("Folder "+folder+" created at "+path)
                return path,1
            elif erase == 'N' or erase == 'n' :
                newfolder = input("Do you want to create a new folder ? Y/N :")
                if newfolder == 'Y' or newfolder == 'y' :
                    newname = input("Please, enter a new folder name :")
                    if newfolder.endswith("/"):
                        path=directory+newname
                        os.makedirs(path, exist_ok=True)
                        print("Folder \""+newname+"\" created at "+path)
                        return path,1
                    else:
                        print("ERROR : Invalid folder name. Please ensure that folder name ends with \'/\'")
                        return 0,0

                elif newfolder == 'N' or newfolder == 'n' :
                    print("The old folder \""+ folder+"\" is kept with its actual content at "+path)
                    return path,2
            else:
                print("ERROR : Invalid answer")
                return 0,0
        else:
            return path,1
    else:
        os.makedirs(path, exist_ok=True)
        print("Folder \""+folder+"\" created at "+path)
        return path,1
##########################################################################
