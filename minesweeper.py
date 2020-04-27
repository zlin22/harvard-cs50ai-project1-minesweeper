import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
        # i = 1
            j = random.randrange(width)
        # j = 1
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if {cell}.issubset(self.cells):
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if {cell}.issubset(self.cells):
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1
        self.moves_made.add(cell)

        # 2
        self.mark_safe(cell)

        # 3
        neighbor_cells = set()
        # if cell is in row 0
        if cell[0] == 0:
            neighbor_cells.add((cell[0] + 1, cell[1]))
            # if cell is in col 0
            if cell[1] == 0:
                neighbor_cells.add((cell[0] + 1, cell[1] + 1))
                neighbor_cells.add((cell[0], cell[1] + 1))
            # if cell is in last col
            elif cell[1] == self.width - 1:
                neighbor_cells.add((cell[0] + 1, cell[1] - 1))
                neighbor_cells.add((cell[0], cell[1] - 1))
            else:
                neighbor_cells.add((cell[0] + 1, cell[1] + 1))
                neighbor_cells.add((cell[0], cell[1] + 1))
                neighbor_cells.add((cell[0] + 1, cell[1] - 1))
                neighbor_cells.add((cell[0], cell[1] - 1))
        # if cell is in last row
        elif cell[0] == self.height - 1:
            neighbor_cells.add((cell[0] - 1, cell[1]))
            # if cell is in col 0
            if cell[1] == 0:
                neighbor_cells.add((cell[0] - 1, cell[1] + 1))
                neighbor_cells.add((cell[0], cell[1] + 1))
            # if cell is in last col
            elif cell[1] == self.width - 1:
                neighbor_cells.add((cell[0] - 1, cell[1] - 1))
                neighbor_cells.add((cell[0], cell[1] - 1))
            else:
                neighbor_cells.add((cell[0] - 1, cell[1] + 1))
                neighbor_cells.add((cell[0], cell[1] + 1))
                neighbor_cells.add((cell[0] - 1, cell[1] - 1))
                neighbor_cells.add((cell[0], cell[1] - 1))
        # if cell is in remaining row
        else:
            neighbor_cells.add((cell[0] - 1, cell[1]))
            neighbor_cells.add((cell[0] + 1, cell[1]))
            # if cell is in col 0
            if cell[1] == 0:
                neighbor_cells.add((cell[0] - 1, cell[1] + 1))
                neighbor_cells.add((cell[0], cell[1] + 1))
                neighbor_cells.add((cell[0] + 1, cell[1] + 1))
            # if cell is in last col
            elif cell[1] == self.width - 1:
                neighbor_cells.add((cell[0] - 1, cell[1] - 1))
                neighbor_cells.add((cell[0], cell[1] - 1))
                neighbor_cells.add((cell[0] + 1, cell[1] - 1))
            else:
                neighbor_cells.add((cell[0] - 1, cell[1] + 1))
                neighbor_cells.add((cell[0], cell[1] + 1))
                neighbor_cells.add((cell[0] + 1, cell[1] + 1))
                neighbor_cells.add((cell[0] - 1, cell[1] - 1))
                neighbor_cells.add((cell[0], cell[1] - 1))
                neighbor_cells.add((cell[0] + 1, cell[1] - 1))

        unknown_cells = set()
        neighbor_mines = set()
        for cell in neighbor_cells:
            if {cell} < self.mines:
                neighbor_mines.add(cell)
            elif {cell} < self.safes:
                pass
            else:
                unknown_cells.add(cell)

        neighbor_sentence = Sentence(unknown_cells, count - len(neighbor_mines))
        self.knowledge.append(neighbor_sentence)

        # 4
        knowledge_copy = self.knowledge.copy()
        for sentence in knowledge_copy:
            if sentence.known_mines() is not None:
                known_mines = sentence.known_mines().copy()
                for mine in known_mines:
                    self.mark_mine(mine)

            if sentence.known_safes() is not None:
                known_safes = sentence.known_safes().copy()
                for safe in known_safes:
                    self.mark_safe(safe)

        # remove blanks in the knowledge
        knowledge_copy = self.knowledge.copy()
        for sentence in knowledge_copy:
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

        # de dupe knowledge
        res = [] 
        for i in self.knowledge:
            if i not in res:
                res.append(i)

        self.knowledge = res

        safe_not_made = self.safes.difference(self.moves_made)
        print(safe_not_made)
        # 5
        knowledge_copy = self.knowledge.copy()
        for sentence1 in knowledge_copy:
            for sentence2 in knowledge_copy:
                if sentence1.cells < sentence2.cells:
                    new_cells = sentence2.cells.difference(sentence1.cells)
                    new_count = sentence2.count - sentence1.count
                    new_sentence = Sentence(new_cells, new_count)
                    self.knowledge.append(new_sentence)

                elif sentence2.cells < sentence1.cells:
                    new_cells = sentence1.cells.difference(sentence2.cells)
                    new_count = sentence1.count - sentence2.count
                    new_sentence = Sentence(new_cells, new_count)
                    self.knowledge.append(new_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_cell = None
        for safe in self.safes:
            if not {safe}.issubset(self.moves_made):
                safe_cell = safe
        return safe_cell

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_cell = None
        for row in range(self.height):
            for col in range(self.width):
                current_cell = (row, col)

                if (not {current_cell}.issubset(self.mines)) and (not {current_cell}.issubset(self.moves_made)):
                    random_cell = current_cell

        return random_cell
