
class JABoard:

    def __init__(self, board_dimensions=(3,3)):
        self.board_dimensions = board_dimensions
        self.edges = {}
        self.squares = {}
        self.score = 0

    def in_board(self, point):
        return (0 <= point[0] < self.board_dimensions[0]
                and 0 <= point[1] < self.board_dimensions[1])


    def edge_is_legal(self, edge):
        if not isinstance(edge, (tuple,tuple)):
            return False

        if not (self.in_board(edge[0])
                and self.in_board(edge[1])):
            return False

        di = edge[0][0] - edge[1][0]
        dj = edge[0][1] - edge[1][1]
        if not ((abs(di) == 1 and dj == 0)
                or (abs(dj) == 1 and di == 0)):
            return False

        return True


    def square_is_surrounded(self, square):
        I, J = square
        if not (0 <= I < self.board_dimensions[0] - 1
                and 0 <= J < self.board_dimensions[1] - 1):
            raise IndexError("Square {} is not in board".format(square))

        edge1 = ((I,J), (I+1,J))
        edge2 = ((I,J), (I,J+1))

        edge3 = ((I,J+1), (I+1,J+1))
        edge4 = ((I+1,J), (I+1,J+1))

        return (edge1 in self.edges
                and edge2 in self.edges
                and edge3 in self.edges
                and edge4 in self.edges)

    def mark_completed_squares(self, player, last_edge_played):
        print("last edge played", last_edge_played)
        di = last_edge_played[0][0] - last_edge_played[1][0]
        dj = last_edge_played[0][1] - last_edge_played[1][1]
        if di == 0:
            minj = min(last_edge_played[0][1], last_edge_played[1][1])
            i = last_edge_played[0][0]
            upper_square = (i - 1, minj)
            lower_square = (i, minj)
            if self.square_is_surrounded(lower_square):
                if not lower_square in self.squares:
                    self.squares[lower_square] = player

            if upper_square[0] >= 0 and self.square_is_surrounded(upper_square):
                if not upper_square in self.squares:
                    self.squares[upper_square] = player
        if dj == 0:
            mini = min(last_edge_played[0][0], last_edge_played[1][0])
            j = last_edge_played[0][1]
            left_square = (mini, j - 1)
            right_square = (mini, j)
            if self.square_is_surrounded(right_square):
                if not right_square in self.squares:
                    self.squares[right_square] = player

            if left_square[1] >= 0 and self.square_is_surrounded(left_square):
                if not left_square in self.squares:
                    self.squares[left_square] = player



    def play_edge(self, edge, player):
        assert(edge not in self.edges)
        assert(self.edge_is_legal(edge))
        self.edges[edge] = True
        self.mark_completed_squares(player, edge)