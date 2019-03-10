import itertools
from copy import deepcopy
import numpy as np

class JABoard:

    def __init__(self, board_dimensions=(3,3)):
        self.board_dimensions = board_dimensions
        self._edges = np.array(self.board_dimensions)
        self._squares = np.zeros((self.board_dimensions[0]-1, self.board_dimensions[1]-1), dtype=np.int)
        self.edges = {}
        self.squares = {}
        self.turn = 0
        self._score = 0
        self._nodes = np.array(self.board_dimensions)
        self._edges = np.zeros(self.board_dimensions + self.board_dimensions, dtype=np.int)

    def connect_nodes(self, n1, n2):
        self._edges[n1[0],n1[1],n2[0], n2[1]] = 1

    def disconnect_nodes(self, n1, n2):
        self._edges[n1[0],n1[1],n2[0], n2[1]] = 0

    def nodes_connected(self, n1, n2):
        return self._edges[n1[0],n1[1],n2[0], n2[1]]

    def _v_edge(self, I, J):
        node1 = (I,J)
        node2 = (I+1,J)
        return node1, node2

    def _h_edge(self, I, J):
        node1 = (I,J)
        node2 = (I,J+1)
        return node1, node2

    def _square_is_surrounded(self, I, J):
        return (self._edges[I,J,I+1,J]
                and self._edges[I,J,I,J+1]
                and self._edges[I+1,J,I+1,J+1]
                and self._edges[I,J+1,I+1,J+1])

    @property
    def score(self):
        return np.sum(self._squares)

    def in_board(self, point):
        return (0 <= point[0] < self.board_dimensions[0]
                and 0 <= point[1] < self.board_dimensions[1])

    def edge_is_legal(self, edge):
        if not (self.in_board(edge[0])
                and self.in_board(edge[1])):
            return False

        di = edge[0][0] - edge[1][0]
        dj = edge[0][1] - edge[1][1]
        if not ((abs(di) == 1 and dj == 0)
                or (abs(dj) == 1 and di == 0)):
            return False

        return True

    def moves(self):
        for i in range(self.board_dimensions[0]):
            for J in range(self.board_dimensions[1] - 1):
                yield self._h_edge(i,J)
        for I in range(self.board_dimensions[0] - 1):
            for j in range(self.board_dimensions[1]):
                yield self._v_edge(I,j)

    def possible_moves(self):
        for n1, n2 in self.moves():
            if not self.nodes_connected(n1, n2):
                yield n1, n2

    def get_max(self, depth):
        moves = []
        for m in self.possible_moves():
            new_marked = self.play_edge(m,1)
            moves.append((m, self.get_value(depth), 1))
            self.unplay_edge(m,1,new_marked)

        if not moves:
            return (None, self.score, 1)

        return max(moves, key=lambda m: m[1])

    def get_min(self, depth):
        moves = []
        for m in self.possible_moves():
            new_marked = self.play_edge(m,-1)
            moves.append((m, self.get_value(depth), -1))
            self.unplay_edge(m,-1, new_marked)
        if not moves:
            return (None, self.score, 1)
        return min(moves, key=lambda m: m[1])

    def get_value(self, depth=0):
        if not self.possible_moves():
            return self.score
        if self.turn == 0:
            return self.get_max(depth+1)[1]
        elif self.turn == 1:
            return self.get_min(depth+1)[1]

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
        assert(player == -1 or player == 1)
        di = last_edge_played[0][0] - last_edge_played[1][0]
        dj = last_edge_played[0][1] - last_edge_played[1][1]
        new_marked = []
        if di == 0:
            minj = min(last_edge_played[0][1], last_edge_played[1][1])
            i = last_edge_played[0][0]
            upper_square = (i - 1, minj)
            lower_square = (i, minj)
            if i < self.board_dimensions[0] - 1 and self._square_is_surrounded(i, minj):
                # TODO Make a numpy array for this
                if not self._squares[i,minj]:
                    self._squares[i,minj] = player
                    new_marked.append((i,minj))

            if upper_square[0] >= 0 and self._square_is_surrounded(i-1, minj):
                if not self._squares[i-1,minj]:
                    self._squares[i-1,minj] = player
                    new_marked.append((i-1,minj))

        if dj == 0:
            mini = min(last_edge_played[0][0], last_edge_played[1][0])
            j = last_edge_played[0][1]
            left_square = (mini, j - 1)
            right_square = (mini, j)
            if (j < self.board_dimensions[1] -1
                    and self.square_is_surrounded(right_square)):
                if not self._squares[mini, j]:
                    new_marked.append((mini,j))
                    self._squares[mini, j] = player

            if left_square[1] >= 0 and self.square_is_surrounded(left_square):
                if not self._squares[mini, j-1]:
                    new_marked.append((mini,j-1))
                    self._squares[mini, j-1] = player

        return new_marked



    def play_edge(self, edge, player):
        assert not self.nodes_connected(edge[0], edge[1]), "edge = {}".format(edge)
        assert(self.edge_is_legal(edge))
        self.edges[edge] = True
        self.connect_nodes(edge[0], edge[1])
        new_marked = self.mark_completed_squares(player, edge)

        self.turn = 0 if self.turn == 1 else 1
        return new_marked

    def unplay_edge(self, edge, player, new_marked):
        self.disconnect_nodes(edge[0], edge[1])
        for square in new_marked:
            self._squares[square[0], square[1]] = 0
        self.turn = 0 if self.turn == 1 else 1


    def try_edge(self, edge, player):
        board = deepcopy(self)
        board.play_edge(edge, player)
        return board

    def v_edge(self, I, J):
        return ((I,J),(I+1,J))

    def h_edge(self, I, J):
        return ((I,J),(I, J+1))

    def __str__(self):
        lines = []
        def dots_line(i):
            dl = ""
            for j in range(self.board_dimensions[1]):
                dl += "*"
                if j < self.board_dimensions[1] - 1:
                    n1, n2 = self._h_edge(i,j)
                    if self.nodes_connected(n1,n2):
                        dl += " - "
                    else:
                        dl += "   "
            return dl

        def squares_and_edges_line(I):
            sel = ""
            for j in range(self.board_dimensions[1]):
                n1, n2 = self._v_edge(I,j)

                if self.nodes_connected(n1, n2):
                    sel += "|"
                else:
                    sel += " "

                if j < self.board_dimensions[1] - 1:
                    owner = self._squares[I,j]
                    if owner == -1:
                        sel += " {}".format(owner)
                    else:
                        sel += " {} ".format(owner)
            return sel


        for I in range(self.board_dimensions[0] - 1):
            dl = dots_line(I)
            sel = squares_and_edges_line(I)

            lines.append(dl)
            lines.append(sel)

        lines.append(dots_line(self.board_dimensions[0]-1))

        return '\n'.join(lines)


