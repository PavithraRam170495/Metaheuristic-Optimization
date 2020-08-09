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
else:
    filename = "uf20-01.cnf"
    executions = 30
    restarts = 10
    iterations = 1000
    wp = 0.4

#read the file and problem-line
file = read_file(filename)
variables, clauses, clause_start = read_problem_line(file)

#GW-SAT implementation
#executions loop
for exe in range(1, executions + 1):

    random.seed(183771 * exe)
    print("Execution :", exe)

    try:
        #restarts loop
        for i in range(1, restarts + 1):

            #assign truth values to variables
            variable_bool = {}
            for var in range(1, variables + 1):
                variable_bool[var] = random.choice([True, False])

            #maximum flips loop
            for j in range(1, iterations + 1):

                #check if the current truth values assigned to the variables satisfies th problem
                sol, unsatisfied, satisfied_clauses = check_solution(clauses, clause_start, file, variable_bool)
                if sol == True:
                    print("solution found in ", j, "th iteration of the ", i, " restart.")
                    print(variable_bool, "\n")
                    raise StopIteration

                #randomly generate value of p
                p = random.uniform(0, 1)

                #GSAT
                if p < wp:
                    net_gain = -clauses - 1
                    variable_flipped = -1
                    unsat = []

                    #for every variable calculate net gain
                    for k in variable_bool.keys():
                        variable_bool[k] = not (variable_bool[k])
                        sol, unsatisfied_flip, satisfied_clauses = check_solution(clauses, clause_start, file,
                                                                                  variable_bool)
                        gain = len(unsatisfied) - len(unsatisfied_flip)

                        #find the variable with the maximum net gain
                        if gain > net_gain:
                            net_gain = gain
                            variable_flipped = k
                        variable_bool[k] = not (variable_bool[k])

                    #flipthe variable with the maximum net gain
                    variable_bool[variable_flipped] = not (variable_bool[variable_flipped])

                #random walk
                else:

                    #pick a variable randomly from all unsatisfied clauses
                    unsat = []
                    for k in unsatisfied:
                        unsat += k
                    unique_unsat_variables = set(unsat)
                    variable_flipped = random.choice(list(unique_unsat_variables))

                    #flip that variable
                    variable_bool[abs(int(variable_flipped))] = not (variable_bool[abs(int(variable_flipped))])

        print("No Solution found")

    except StopIteration:
        pass
