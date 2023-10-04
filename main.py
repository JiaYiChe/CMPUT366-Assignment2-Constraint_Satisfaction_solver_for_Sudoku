import matplotlib.pyplot as plt
import numpy as np
import time

class PlotResults:
    """
    Class to plot the results. 
    """
    def plot_results(self, data1, data2, label1, label2, filename):
        """
        This method receives two lists of data point (data1 and data2) and plots
        a scatter plot with the information. The lists store statistics about individual search 
        problems such as the number of nodes a search algorithm needs to expand to solve the problem.

        The function assumes that data1 and data2 have the same size. 

        label1 and label2 are the labels of the axes of the scatter plot. 
        
        filename is the name of the file in which the plot will be saved.
        """
        _, ax = plt.subplots()
        ax.scatter(data1, data2, s=100, c="g", alpha=0.5, cmap=plt.cm.coolwarm, zorder=10)
    
        lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
        np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
        ]
    
        ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
        ax.set_aspect('equal')
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        plt.xlabel(label1)
        plt.ylabel(label2)
        plt.grid()
        plt.savefig(filename)

class Grid:
    """
    Class to represent an assignment of values to the 81 variables defining a Sudoku puzzle. 

    Variable _cells stores a matrix with 81 entries, one for each variable in the puzzle. 
    Each entry of the matrix stores the domain of a variable. Initially, the domains of variables
    that need to have their values assigned are 123456789; the other domains are limited to the value
    initially assigned on the grid. Backtracking search and AC3 reduce the the domain of the variables 
    as they proceed with search and inference.
    """
    def __init__(self):
        self._cells = []
        self._complete_domain = "123456789"
        self._width = 9

    def copy(self):
        """
        Returns a copy of the grid. 
        """
        copy_grid = Grid()
        copy_grid._cells = [row.copy() for row in self._cells]
        return copy_grid

    def get_cells(self):
        """
        Returns the matrix with the domains of all variables in the puzzle.
        """
        return self._cells

    def get_width(self):
        """
        Returns the width of the grid.
        """
        return self._width

    def read_file(self, string_puzzle):
        """
        Reads a Sudoku puzzle from string and initializes the matrix _cells. 

        This is a valid input string:

        4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......

        This is translated into the following Sudoku grid:

        - - - - - - - - - - - - - 
        | 4 . . | . . . | 8 . 5 | 
        | . 3 . | . . . | . . . | 
        | . . . | 7 . . | . . . | 
        - - - - - - - - - - - - - 
        | . 2 . | . . . | . 6 . | 
        | . . . | . 8 . | 4 . . | 
        | . . . | . 1 . | . . . | 
        - - - - - - - - - - - - - 
        | . . . | 6 . 3 | . 7 . | 
        | 5 . . | 2 . . | . . . | 
        | 1 . 4 | . . . | . . . | 
        - - - - - - - - - - - - - 
        """
        i = 0
        row = []
        for p in string_puzzle:
            if p == '.':
                row.append(self._complete_domain)
            else:
                row.append(p)

            i += 1

            if i % self._width == 0:
                self._cells.append(row)
                row = []
            
    def print(self):
        """
        Prints the grid on the screen. Example:

        - - - - - - - - - - - - - 
        | 4 . . | . . . | 8 . 5 | 
        | . 3 . | . . . | . . . | 
        | . . . | 7 . . | . . . | 
        - - - - - - - - - - - - - 
        | . 2 . | . . . | . 6 . | 
        | . . . | . 8 . | 4 . . | 
        | . . . | . 1 . | . . . | 
        - - - - - - - - - - - - - 
        | . . . | 6 . 3 | . 7 . | 
        | 5 . . | 2 . . | . . . | 
        | 1 . 4 | . . . | . . . | 
        - - - - - - - - - - - - - 
        """
        for _ in range(self._width + 4):
            print('-', end=" ")
        print()

        for i in range(self._width):

            print('|', end=" ")

            for j in range(self._width):
                if len(self._cells[i][j]) == 1:
                    print(self._cells[i][j], end=" ")
                elif len(self._cells[i][j]) > 1:
                    print('.', end=" ")
                else:
                    print(';', end=" ")

                if (j + 1) % 3 == 0:
                    print('|', end=" ")
            print()

            if (i + 1) % 3 == 0:
                for _ in range(self._width + 4):
                    print('-', end=" ")
                print()
        print()

    def print_domains(self):
        """
        Print the domain of each variable for a given grid of the puzzle.
        """
        for row in self._cells:
            print(row)

    def is_solved(self):
        """
        Returns True if the puzzle is solved and False otherwise. 
        """
        for i in range(self._width):
            for j in range(self._width):
                if len(self._cells[i][j]) != 1:
                    return False
        return True

class VarSelector:
    """
    Interface for selecting variables in a partial assignment. 

    Extend this class when implementing a new heuristic for variable selection.
    """
    def select_variable(self, grid):
        pass

class FirstAvailable(VarSelector):
    """
    Naïve method for selecting variables; simply returns the first variable encountered whose domain is larger than one.
    """
    def select_variable(self, grid):
        # Implement here the first available heuristic
        matrix = grid.get_cells()
        for i in range(grid.get_width()):
            for j in range(grid.get_width()):
                if(len(matrix[i][j])>1):
                    thisTuple = (i,j)
                    return thisTuple

class MRV(VarSelector):
    """
    Implements the MRV heuristic, which returns one of the variables with smallest domain. 
    """
    def select_variable(self, grid):
        # Implement here the mrv heuristic
        matrix = grid.get_cells()
        checker = 10
        thisTuple=None
        for i in range(grid.get_width()):
            for j in range(grid.get_width()):
                if(len(matrix[i][j])>1):
                    if(len(matrix[i][j])<checker):
                        checker = len(matrix[i][j])
                        thisTuple = (i,j)
        #this comment out code check how many assigned variable have in current variable's row, col and 3x3 cell and add up to see which variable have the most assigned variable(mesns it have less choice to pick from)
        #please ignore these I'm just leave it to remind my self and in case need in future
        '''
                if(len(matrix[i][j])>1):
                    numInRow=0
                    numInCol=0
                    numInBlock=0

                    for value in range(grid.get_width()):
                        if(len(matrix[i][value])==1):
                            numInRow+=1
                        if(len(matrix[value][j])==1):
                            numInCol+=1
                    for x in range(3):
                        for y in range(3):
                            if(len(matrix[(i//3)*3+x][(j//3)*3+y])==1):
                                numInBlock+=1
                    total = numInCol+numInRow+numInBlock
                    checker.append([(i,j),total])
                    
        max = checker[0][1]
        thisTuple = checker[0][0]
        for item in checker:
            if item[1]>max:
                max = item[1]
                thisTuple = item[0]
        '''
        return thisTuple



class AC3:
    """
    This class implements the methods needed to run AC3 on Sudoku. 
    """
    def remove_domain_row(self, grid, row, column):
        """
        Given a matrix (grid) and a cell on the grid (row and column) whose domain is of size 1 (i.e., the variable has its
        value assigned), this method removes the value of (row, column) from all variables in the same row. 
        """
        variables_assigned = []

        for j in range(grid.get_width()):
            if j != column:
                new_domain = grid.get_cells()[row][j].replace(grid.get_cells()[row][column], '')

                if len(new_domain) == 0:
                    return None, True

                if len(new_domain) == 1 and len(grid.get_cells()[row][j]) > 1:
                    variables_assigned.append((row, j))

                grid.get_cells()[row][j] = new_domain
        
        return variables_assigned, False

    def remove_domain_column(self, grid, row, column):
        """
        Given a matrix (grid) and a cell on the grid (row and column) whose domain is of size 1 (i.e., the variable has its
        value assigned), this method removes the value of (row, column) from all variables in the same column. 
        """
        variables_assigned = []

        for j in range(grid.get_width()):
            if j != row:
                new_domain = grid.get_cells()[j][column].replace(grid.get_cells()[row][column], '')
                
                if len(new_domain) == 0:
                    return None, True

                if len(new_domain) == 1 and len(grid.get_cells()[j][column]) > 1:
                    variables_assigned.append((j, column))

                grid.get_cells()[j][column] = new_domain

        return variables_assigned, False

    def remove_domain_unit(self, grid, row, column):
        """
        Given a matrix (grid) and a cell on the grid (row and column) whose domain is of size 1 (i.e., the variable has its
        value assigned), this method removes the value of (row, column) from all variables in the same unit. 
        """
        variables_assigned = []

        row_init = (row // 3) * 3
        column_init = (column // 3) * 3

        for i in range(row_init, row_init + 3):
            for j in range(column_init, column_init + 3):
                if i == row and j == column:
                    continue

                new_domain = grid.get_cells()[i][j].replace(grid.get_cells()[row][column], '')

                if len(new_domain) == 0:
                    return None, True

                if len(new_domain) == 1 and len(grid.get_cells()[i][j]) > 1:
                    variables_assigned.append((i, j))

                grid.get_cells()[i][j] = new_domain
        return variables_assigned, False

    def pre_process_consistency(self, grid):
        """
        This method enforces arc consistency for the initial grid of the puzzle.

        The method runs AC3 for the arcs involving the variables whose values are 
        already assigned in the initial grid. 
        """
        # Implement here the code for making the CSP arc consistent as a pre-processing step; this method should be called once before search
        
        Q=[]
        for i in range(grid.get_width()):
            for j in range(grid.get_width()):
                if len(grid.get_cells()[i][j]) ==1:
                    Q.append((i,j))
        
        self.consistency(grid,Q)







    def consistency(self, grid, Q):
        """
        This is a domain-specific implementation of AC3 for Sudoku. 

        It keeps a set of variables to be processed (Q) which is provided as input to the method. 
        Since this is a domain-specific implementation, we don't need to maintain a graph and a set 
        of arcs in memory. We can store in Q the cells of the grid and, when processing a cell, we
        ensure arc consistency of all variables related to this cell by removing the value of
        cell from all variables in its column, row, and unit. 

        For example, if the method is used as a preprocessing step, then Q is initialized with 
        all cells that start with a number on the grid. This method ensures arc consistency by
        removing from the domain of all variables in the row, column, and unit the values of 
        the cells given as input. Like the general implementation of AC3, the method adds to 
        Q all variables that have their values assigned during the propagation of the contraints. 

        The method returns True if AC3 detected that the problem can't be solved with the current
        partial assignment; the method returns False otherwise. 
        """
        # Implement here the domain-dependent version of AC3.
        
        while len(Q) >0:
            var = Q.pop()

            list1, answer1 = self.remove_domain_row(grid,var[0],var[1])

            list2, answer2 = self.remove_domain_column(grid,var[0],var[1])

            list3, answer3 = self.remove_domain_unit(grid,var[0],var[1])

            if answer1 or answer2 or answer3:
                return False

            if list1:
                Q.extend(list1)
            if list2:
                Q.extend(list2)
            if list3:
                Q.extend(list3)

        return True




class Backtracking:
    """
    Class that implements backtracking search for solving CSPs. 
    """
    #consistency function I write for second part that checks if row, column or 3x3 cell have any repetition number already exist
    def consistencyCheck(self,grid,var,d):
        for i in range(grid.get_width()):
            if grid.get_cells()[var[0]][i] == d:
                return False
            if grid.get_cells()[i][var[1]] == d:
                return False
        for x in range (3):
            for y in range (3):
                if grid.get_cells()[(var[0]//3)*3 + x][(var[1]//3)*3 + y]==d:
                    return False
        return True
                    
    def search(self, grid, var_selector):
        """
        Implements backtracking search with inference. 
        """
        # Implemente here the Backtracking search.
        if grid.is_solved():
            return grid
        var = var_selector.select_variable(grid)
        for d in grid.get_cells()[var[0]][var[1]]:
            #the function made in second part can use with the consistency, it will just make the time slower not much and professor said its fine to leave it (I choose to comment out to run faster)
            #if self.consistencyCheck(grid,var,d):
                Q=[]
                Q.append(var)

                copy_grid = grid.copy()
                copy_grid.get_cells()[var[0]][var[1]] = copy_grid.get_cells()[var[0]][var[1]].replace(copy_grid.get_cells()[var[0]][var[1]], str(d))
                if AC3().consistency(copy_grid,Q):
                    rb = self.search(copy_grid,var_selector)
                    if rb != False:
                        return rb
        return False
        


#These are the code that build plot
#file = open('tutorial_problem.txt', 'r')
file = open('top95.txt', 'r')
problems = file.readlines()

running_time_mrv = []
running_time_first_available = []
#run time of MRV
for p in problems:
    start = time.time()

    g = Grid()
    g.read_file(p)

    var_selector = MRV()
    solver = Backtracking()
    AC3().pre_process_consistency(g)
    grid = solver.search(g,var_selector)

    end = time.time()
    running_time_mrv.append(end-start)
#run time of first available
for p in problems:
    start = time.time()

    g = Grid()
    g.read_file(p)

    var_selector = FirstAvailable()
    solver = Backtracking()
    AC3().pre_process_consistency(g)
    grid = solver.search(g,var_selector)

    end = time.time()
    running_time_first_available.append(end-start)

plotter = PlotResults()
plotter.plot_results(running_time_mrv, running_time_first_available, "Running Time Backtracking (MRV)", "Running Time Backtracking (FA)", "running_time")
