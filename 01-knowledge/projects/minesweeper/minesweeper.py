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
            j = random.randrange(width)
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
        If the count equals the number of cells, every cell is a mine.
        """
        if len(self.cells) == self.count and self.count != 0:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        If the count is 0, every cell must be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
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

        # 1) Mark the cell as a move made and 2) mark it as safe.
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # 3) Determine the neighboring cells that are neither known safe nor known mines.
        i, j = cell
        neighbors = set()
        for ni in range(i - 1, i + 2):
            for nj in range(j - 1, j + 2):
                if (ni, nj) == cell:
                    continue
                if 0 <= ni < self.height and 0 <= nj < self.width:
                    if (ni, nj) in self.safes or (ni, nj) in self.mines:
                        continue
                    neighbors.add((ni, nj))

        # Adjust count by subtracting the known mines among neighbors.
        for ni in range(i - 1, i + 2):
            for nj in range(j - 1, j + 2):
                if (ni, nj) == cell:
                    continue
                if 0 <= ni < self.height and 0 <= nj < self.width:
                    if (ni, nj) in self.mines:
                        count -= 1

        # Only add a sentence if there are undetermined neighbor cells.
        if len(neighbors) > 0:
            new_sentence = Sentence(neighbors, count)
            self.knowledge.append(new_sentence)

        # 4) Repeatedly update the knowledge base with new inferences until no more can be made.
        updated = True
        while updated:
            updated = False
            safes_to_add = set()
            mines_to_add = set()

            # Determine any cells that are safe or mines.
            for sentence in self.knowledge:
                safes_found = sentence.known_safes()
                mines_found = sentence.known_mines()
                if safes_found:
                    safes_to_add |= safes_found
                if mines_found:
                    mines_to_add |= mines_found

            # Mark any new safe cells.
            if safes_to_add:
                for safe in safes_to_add:
                    if safe not in self.safes:
                        self.mark_safe(safe)
                        updated = True

            # Mark any new mines.
            if mines_to_add:
                for mine in mines_to_add:
                    if mine not in self.mines:
                        self.mark_mine(mine)
                        updated = True

            # 5) Infer new sentences from existing ones.
            new_sentences = []
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1 == sentence2:
                        continue
                    # If sentence1 is a subset of sentence2, then we can infer a new sentence.
                    if sentence1.cells and sentence1.cells.issubset(sentence2.cells):
                        new_cells = sentence2.cells - sentence1.cells
                        new_count = sentence2.count - sentence1.count
                        new_sentence = Sentence(new_cells, new_count)
                        if new_sentence not in self.knowledge and new_sentence not in new_sentences and len(new_sentence.cells) > 0:
                            new_sentences.append(new_sentence)
            if new_sentences:
                self.knowledge.extend(new_sentences)
                updated = True

        # Optional clean-up: Remove any empty sentences.
        self.knowledge = [s for s in self.knowledge if s.cells]

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_moves = {(i, j) for i in range(self.height) for j in range(self.width)}
        # Exclude moves already made and known mines.
        choices = list(all_moves - self.moves_made - self.mines)
        if choices:
            return random.choice(choices)
        return None
