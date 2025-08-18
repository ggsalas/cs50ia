import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for x, domain in self.domains.items():
            length = x.length
            new_domain = set()
            for word in domain:
                if (len(word) == length):
                    new_domain.add(word)
            self.domains[x] = new_domain


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.

        It sounds like you have a good understanding of the process! 
        Checking if x and y overlap is a great first step. 
        If they do overlap, you can then check if the words in their domains have consistent letters at the overlapping positions. 
        If a word in the domain of x has a different letter at the overlapping position than any word in the domain of y, 
            you should remove that word from the domain of x.
        """
        revision_made = False
        x_neighbors = self.crossword.neighbors(x)
        for neighbor in x_neighbors:
            if neighbor == y:
                # returned as (position for first var, position for second var)
                overlaps = self.crossword.overlaps[x, neighbor]
                x_overlap = overlaps[0]
                y_overlap = overlaps[1]
                new_x_domain = self.domains[x].copy()
                for x_domain in self.domains[x]:
                    x_overlap_letter = x_domain[x_overlap]
                    some_y_domain_matches_with_x_domain = False
                    for y_domain in self.domains[y]:
                        y_overlap_letter = y_domain[y_overlap]
                        if x_overlap_letter == y_overlap_letter:
                            some_y_domain_matches_with_x_domain = True

                    if some_y_domain_matches_with_x_domain == False:
                        new_x_domain.remove(x_domain)
                        revision_made = True
                self.domains[x] = new_x_domain
        return revision_made


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        all_arcs = list()
        for x in self.domains:
            neighbors = self.crossword.neighbors(x)
            for neighbor in neighbors:
                all_arcs.append((x, neighbor))

        if arcs == None:
            arcs = all_arcs

        while len(arcs) != 0:
            for arc in arcs:
                x = arc[0]
                y = arc[1]
                arcs.remove(arc)
                rev = self.revise(x, y)

                if rev:
                    # if a revision has been made
                    # add x neighbors to the queue to ensure arc consistency with new x domain
                    for z in self.crossword.neighbors(x):
                        arcs.append((z, x))
                else:
                    # if no revision has been made
                    # check if x domain is empty, means there is no solution possible
                    if len(self.domains[x]) == 0:
                        return False
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.

        > assignment is a dictionary of Variable: word, not a set of words
        it assume that each variable has a single word
        """
        is_complete = True
        for x, _ in self.domains.items():
            if x not in assignment:
                is_complete = False

        return is_complete

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        all_x_distinct = True
        for i, i_value in assignment.items():
            for j, j_value in assignment.items():
                if (i_value == j_value and i != j):
                    all_x_distinct = False

        all_x_length = True
        for x, val in assignment.items():
            if (len(val) != x.length):
                all_x_length = False

        no_neighboring_conflicts = True
        for x, x_val in assignment.items():
            x_neighbors = self.crossword.neighbors(x)
            for n in x_neighbors:
                    # returned as (position for first var, position for second var)
                    overlaps = self.crossword.overlaps[x, n]
                    x_overlap = overlaps[0]
                    n_overlap = overlaps[1]
                    if n in assignment:
                        n_val = assignment[n]
                        x_overlap_letter = x_val[x_overlap]
                        n_overlap_letter = n_val[n_overlap]
                        if (x_overlap_letter != n_overlap_letter):
                            no_neighboring_conflicts = False

        if (all_x_distinct and all_x_length and no_neighboring_conflicts):
            return True
        else:
            return False
                    

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.

        least-constraining values heuristics
            - number of values ruled out for neighboring unassigned variables
        """
        neighbors = self.crossword.neighbors(var)

        unassigned_neighbors = list()
        for x in neighbors:
            if x not in assignment:
                unassigned_neighbors.append(x)


        count_n_ruled_out_values = dict()
        for value in self.domains[var]:
            count_n_ruled_out_values[value] = 0

        # count the neighbor out values per each value
        for value in self.domains[var]:
            for neighbor in unassigned_neighbors:
                    # calculate the overlap of each neighbor and the var
                    overlaps = self.crossword.overlaps[var, neighbor]
                    var_overlap = overlaps[0]
                    neighbor_overlap = overlaps[1]
                    # calculate the overlap letter for each value in neighbor domain
                    for n_value in self.domains[neighbor]:
                        var_overlap_letter = value[var_overlap]
                        neighbor_overlap_letter = n_value[neighbor_overlap]
                        # If the overlap letter do not match, this word can be ruled out
                        if var_overlap_letter != neighbor_overlap_letter:
                            count_n_ruled_out_values[value] += 1

        def get_value(item):
            value = item[1]
            return (value == 0, value)

        sorted_items = sorted(count_n_ruled_out_values.items(), key=get_value)
        sorted_keys = list()
        for key, _ in sorted_items:
            sorted_keys.append(key)

        return sorted_keys

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        u_vars = list()
        for x, _ in self.domains.items():
            if x not in assignment:
                u_vars.append(x)

        # order by fewest number of values in domain
        # and less neighbors
        u_vars_domain_count = dict()
        for x in u_vars:
            u_vars_domain_count[x] = (len(self.domains[x]), len(self.crossword.neighbors(x)))

        def get_value(item):
            domain_count = item[1][0]
            neighbors_count = item[1][1]
            return (domain_count, neighbors_count)
        u_vars_domain_ordered = sorted(u_vars_domain_count.items(), key=get_value)

        return u_vars_domain_ordered[0][0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        is_complete = self.assignment_complete(assignment)
        if is_complete == True:
            return assignment

        x = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(x, assignment):
            new_assignment = assignment.copy()
            new_assignment[x] = value
            if self.consistent(new_assignment): 
                assignment[x] = value
                result = self.backtrack(assignment)
                if result != False:
                    return result
                else: 
                    assignment.remove(x)
                    return False
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
