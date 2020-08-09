import random
import sys

#function to read file
def read_file(filename):
    f = open(filename,"r")
    file = f.readlines()
    return(file)

#function to read the problem line
def read_problem_line(file):
    for i in range(len(file)):
        if file[i][0] == 'c':
            continue
        if file[i][0] == 'p':
            problem = file[i].strip().split(' ')
            # print(problem)
            k = [j for j in problem if j == '\n' or j == ' ' or j == '']
            for l in k:
                problem.remove(l)
            # print(problem)
            variables = int(problem[2])
            clauses = int(problem[3])
            clause_start = i
            break
    return variables, clauses, clause_start


#function to check if the truth values assigned to the variables satisfy the problem
def check_solution(clauses, clause_start, file, variable_bool):

    no_satisfied_clauses = 0
    unsatisfied = []
    satisfied_clauses = []
    p = clause_start + 1
    no_clause = 0

    while p <= len(file):
        clause = file[p].strip().split(' ')

        if clause == ['%']:
            break

        #if the last element in the line is not 0
        while clause[-1] != str(0):
            p += 1
            clause.extend(file[p].strip().split(' '))

        if clause[-1] == str(0):
            no_clause += 1
            clause.remove(str(0))
            satisfied = []
            for q in clause:
                if int(q) > 0:
                    satisfied.append(variable_bool[abs(int(q))])
                elif int(q) < 0:
                    if variable_bool[abs(int(q))] == True:
                        satisfied.append(False)
                    else:
                        satisfied.append(True)
            if True in satisfied:
                no_satisfied_clauses += 1
                satisfied_clauses.append(clause)
            else:
                unsatisfied.append(clause)
            p += 1

    if clauses !=  no_clause:
        print("Not correct no. of clauses")
        sys.exit(0)

    if no_satisfied_clauses == clauses:
        return (True, unsatisfied, satisfied_clauses)
    else:
        return (False, unsatisfied, satisfied_clauses)

#read command-line arguments else use default values
if len(sys.argv) > 1:
    filename = sys.argv[1]
    executions = int(sys.argv[2])
    restarts = int(sys.argv[3])
    iterations = int(sys.argv[4])
    wp = float(sys.argv[5])
    tl = int(sys.argv[6])
else:
    filename = "uf20-01.cnf"
    executions = 30
    restarts = 10
    iterations = 1000
    wp = 0.4
    tl = 5

#read the file and problem-line
file = read_file(filename)
variables, clauses, clause_start = read_problem_line(file)

#WALK-SAT implementation
#executions loop
for exe in range(1, executions + 1):

    random.seed(183771 * exe)
    print("Execution :", exe)

    try:
        #restars loop
        for i in range(1, restarts + 1):

            #assign truth values to variables
            variable_bool = {}
            for var in range(1, variables + 1):
                variable_bool[var] = random.choice([True, False])

            #initialize the tabu age of variables to -2* tl
            tabu_age = {}
            for tb in range(1, variables + 1):
                tabu_age[tb] = -2 * tl

            #maximum flips loop
            for j in range(1, iterations + 1):

                #check if the current truth values assigned to the variables satisfies th problem
                sol, unsatisfied, satisfied_clauses = check_solution(clauses, clause_start, file, variable_bool)
                if sol == True:
                    print("solution found in ", j, "th iteration of the ", i, " restart.")
                    print(variable_bool, "\n")
                    raise StopIteration


                neg_gain = -clauses - 1
                variable_flipped = -1
                neg_gain_var = []
                min_neg_gain_var = {}

                #select a random unsatisfied clause
                random_clause = random.choice(unsatisfied)

                #for every variable in the clause calculate negative gain
                for k in random_clause:
                    k = abs(int(k))

                    #the variable is selected only if it is not tabu
                    if tabu_age[k] + tl < j:
                        variable_bool[k] = not (variable_bool[k])
                        sol, unsatisfied_flip, satisfied_clauses_flip = check_solution(clauses, clause_start, file,
                                                                                       variable_bool)

                        #calculate negative gain
                        sat_clauses = set(map(tuple, satisfied_clauses))
                        sat_clauses_flip = set(map(tuple, satisfied_clauses_flip))
                        neg_gain = len(sat_clauses) - len(set(sat_clauses).intersection(set(sat_clauses_flip)))

                        if neg_gain == 0:
                            neg_gain_var.append(k)
                        else:
                            min_neg_gain_var[k] = neg_gain

                        #flip back the selected variable to do the same process with the next variable
                        variable_bool[k] = not (variable_bool[k])

                #if any of the variables in the unsat clause have negative gain = 0, select a random variable with neg gain = 0 to flip and update its tabu age
                if len(neg_gain_var):
                    variable_flipped = random.choice(neg_gain_var)
                    variable_bool[variable_flipped] = not (variable_bool[variable_flipped])
                    tabu_age[variable_flipped] = j

                #if none of the variables in the unsat clause have negative gain = 0
                elif len(min_neg_gain_var):

                    #generate a random number
                    p = random.uniform(0, 1)

                    #randomly choose a variable from the list of variables that are not tabu and update its tabu age
                    if p < wp:
                        variable_flipped = random.choice(list(min_neg_gain_var.keys()))
                        variable_bool[variable_flipped] = not (variable_bool[variable_flipped])
                        tabu_age[variable_flipped] = j

                    #select a variable with minimum negative gain and update its tabu age
                    else:
                        neg_gains = []
                        neg_var = []
                        for key, value in min_neg_gain_var.items():
                            neg_gains.append(value)
                            neg_var.append(key)
                        minimum_gain = min(neg_gains)
                        variable_flipped = neg_var[neg_gains.index(minimum_gain)]
                        variable_bool[variable_flipped] = not (variable_bool[variable_flipped])
                        tabu_age[variable_flipped] = j

                #if all variables in the selected unsat clause are tabued, goto the next iteration
                else:
                    continue

        print("No Solution found")

    except StopIteration:
        pass

