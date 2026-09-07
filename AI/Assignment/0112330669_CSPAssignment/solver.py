import time
from collections import deque


class SudokuCSP:

    def __init__(self, board):
        self.board = board
        
        # variables 
        self.variables = [(r, c) for r in range(9) for c in range(9)]
        # domains
        self.domains = {}
        for r in range(9):
            for c in range(9):

                if board[r][c] != 0:
                    self.domains[(r,c)] = {board[r][c]}

                else:
                    self.domains[(r,c)] = set(range(1,10))
        self.neighbors = {}

        self.create_neighbors()


        self.node_expansion = 0

    # Create row column box neighbors
    def create_neighbors(self):

        for cell in self.variables:

            r,c = cell

            neighbour = set()


            # Row
            for col in range(9):
                if col != c:
                    neighbour.add((r,col))

            # Column
            for row in range(9):
                if row != r:
                    neighbour.add((row,c))


            # 3x3 box
            box_row = r//3*3
            box_col = c//3*3

            for i in range(box_row, box_row+3):
                for j in range(box_col, box_col+3):

                    if (i,j) != cell:
                        neighbour.add((i,j))

            self.neighbors[cell] = neighbour

    # AC-3 Algorithm
    def AC3(self):
        queue = deque()
        for Xi in self.variables:
            for Xj in self.neighbors[Xi]:
                queue.append((Xi,Xj))
        while queue:
            Xi,Xj = queue.popleft()
            if self.revise(Xi,Xj):
                if len(self.domains[Xi]) == 0:
                    return False
                for Xk in self.neighbors[Xi]:
                    if Xk != Xj:
                        queue.append((Xk,Xi))


        return True




    # Remove invalid values

    def revise(self,Xi,Xj):

        revised=False
        remove_values=set()
        for x in self.domains[Xi]:

            valid=False
            for y in self.domains[Xj]:

                if x != y:
                    valid=True


            if not valid:
                remove_values.add(x)

        for value in remove_values:

            self.domains[Xi].remove(value)
            revised=True

        return revised




    # Check constraints

    def consistent(self,var,value):

        for neighbour in self.neighbors[var]:

            if len(self.domains[neighbour])==1:

                if value in self.domains[neighbour]:
                    return False


        return True




    # MRV heuristic

    def select_variable(self):

        unassigned=[]


        for var in self.variables:

            if len(self.domains[var]) > 1:

                unassigned.append(var)



        if not unassigned:
            return None
        
        #MRV OFF
        return unassigned[0]

     
        """    
        #MRV ON
        return min(
            unassigned,
            key=lambda var:len(self.domains[var])
        )

        """

    # Backtracking Search

    def backtrack(self):

        self.node_expansion +=1


        var=self.select_variable()


        if var is None:

            return True



        current_domain=list(self.domains[var])



        for value in current_domain:


            if self.consistent(var,value):


                backup={}

                for key in self.domains:
                    backup[key]=self.domains[key].copy()



                self.domains[var]={value}


            #recursive step abar AC3 chalacche,MRV onek slow 
            if self.AC3():

                    if self.backtrack():
                        return True
            """
            #AC3 remove 
            if self.backtrack():
                    return True
 
            """
            self.domains=backup



        return False




    def solve(self):

        if self.AC3():

            if self.backtrack():
                return True


        return False




    def get_solution(self):

        result=""


        for r in range(9):

            for c in range(9):

                result += str(
                    next(iter(self.domains[(r,c)]))
                )


        return result




# Convert string to board

def create_board(line):

    board=[]


    index=0


    for i in range(9):

        row=[]

        for j in range(9):

            row.append(
                int(line[index])
            )

            index+=1


        board.append(row)


    return board




# Main program

def main():

    input_file="puzzles.txt"
    output_file="solutions.txt"


    output=open(output_file,"w")



    with open(input_file,"r") as file:


        puzzles=file.readlines()



    for puzzle in puzzles:


        puzzle=puzzle.strip()


        if not puzzle:
            continue



        board=create_board(puzzle)



        sudoku=SudokuCSP(board)



        start=time.time()


        solved=sudoku.solve()


        end=time.time()



        if solved:

            solution=sudoku.get_solution()

            output.write(solution+"\n")


            print("Solved:")
            print(solution)

        else:

            output.write("No Solution\n")



        print(
            "Time:",
            end-start,
            "Nodes:",
            sudoku.node_expansion
        )



    output.close()



if __name__=="__main__":

    main()