#### PART 1 ####
# final_grade: Calculates the final grade for each student, and writes the output (while eliminating illegal
# rows from the input file) into the file in `output_path`. Returns the average of the grades.
#   input_path: Path to the file that contains the input
#   output_path: Path to the file that will contain the output

def checkArgs(parameters):
    if parameters[0][0] == '0' or len(parameters[0]) != 8:
        return False
    if not (parameters[1].isalpha() or parameters[1] == ""):
        return False
    if int(parameters[2]) < 1:
        return False
    if int(parameters[3]) <= 50 or int(parameters[2]) > 100:
        return False
    return True

def final_grade(input_path: str, output_path: str) -> int:
    in_file = open(input_path, 'r') #open file on read mode
    lines = in_file.readlines();
    in_file.close() #close file

    students = {}
    for line in lines:
        line = line.replace(" ", "") #remove all spaces
        parameters = line.split(",") #split string by comma and insert into list
        if not checkArgs(parameters): #check arguments
            continue
        key = int(parameters[0])
        student_grade = ((key % 100) + int(parameters[3])) // 2 #compute final grade
        value = [int(parameters[3]), student_grade]
        students[key] = value #update student to last record or insert a new student

    out_file = open(output_path, 'w') #open file on write mode
    class_avg = 0
    for key in sorted(students): #iterate in an ordered way
        class_avg += students[key][1] ##cumulative sum
        #construct string 
        str_to_print = "{id}, {homework_avg}, {final_grade}\n".format(id=key, homework_avg=students[key][0], 
                                                                final_grade=students[key][1])
        out_file.write(str_to_print) #print new string to output file
    out_file.close() #close file

    return class_avg // len(students) #return average


#### PART 2 ####
# check_strings: Checks if `s1` can be constructed from `s2`'s characters.
#   s1: The string that we want to check if it can be constructed
#   s2: The string that we want to construct s1 from
def check_strings(s1: str, s2: str) -> bool:
    s1 = s1.lower()
    s2 = s2.lower()

    for letter in s1:
        #if the occurences of a letter is greater in s1 than in s2, s2 can't be constructed from s1
        if s1.count(letter) > s2.count(letter): 
            return False
    
    return True