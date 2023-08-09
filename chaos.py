from random import randint, uniform
from polygon import Polygon
from time import time
from matplotlib import pyplot
from numpy import array

def randcor(x_bounds:  tuple[float], y_bounds:  tuple[float]) -> tuple[float]:
    """
    Parametres:
        x_bounds [type: tuple(float)] = (lowest, highest) values of X
        y_bounds [type: tuple(float)] = (lowest, highest) values of Y

    Returns a randomly generated coordinates between given bounds.
    """
    return (uniform(*x_bounds), uniform(*y_bounds))

def load_filedata(file_path: str):
    """
    Load and cleans all the data from a file at given path.

    Parametres: 
        file_path [type: str] = Location of file

    Returs:
        Data inside a file a one whole String
    """
    file_data = None
    with open (file_path, "r") as file:
        file_data = file.read().replace('\n', '')

    return file_data
   
def find_unique_char(text:str):
    """
    Finds Unique Charaters in a String

    Parameters: 
        text[type: str] = Unique Characters to be found from.

    Return:
        Dictionary contaning all unique characters.
        Key = Character
        Value = Index of Key inside Dictionary
    """

    unique_chars = {}
    for pos, char in enumerate(sorted(set(text))):
        unique_chars[char] = pos

    return unique_chars


class Chaos(object):
    """
    Designed to create fractals insides polygon with n sides. {n >= 3}
    """
    def __init__(self, num_of_points:int, r:float = 0.5,
                 polygon_sides:int = Polygon.min_sides, polygon_edge_len:float= Polygon.default_edge_length) -> None:
        pyplot.title("Random Sequence")

        self.polygon = Polygon(polygon_sides, polygon_edge_len)
        self.polygon.set_vetices_name()

        self._num_of_points = num_of_points
        self._last_choosen_vrtx = None # to create fractal when sides > 3. More explanation in _choose_rand_vertex()
        self.r = r

    def _get_cor_in_polygon(self) -> tuple[float]:
        """
        Return:
            Coordinate (x, y) that lies inside polygon.
        """
        x_bounds = self.polygon.get_x_bounds()
        y_bounds = self.polygon.get_y_bounds()

        random_point = randcor(x_bounds, y_bounds)
        while not self.polygon.contains(*random_point):
            random_point = randcor(x_bounds, y_bounds)

        return random_point

    def _choose_rand_vertex(self) -> int:
        """
        Chooses a Random Vertex based on number of edges.

        Return:
        type: int = Vertex's index
        """

        # When Sides = 3 Choose a random vertex straight away.
        # When Sides > 3 it make sure same vertex is not choosen twice in a row.
        # Because for a fractal to be formed inside a square condition above must be applied.7
        # For sides > 4 diffrent fractal froms when condition is applied and when it is not.

        if (self._last_choosen_vrtx is None) or (len(self.polygon.edges) == 3):
            vertex_num = randint(0, len(self.polygon.edges) - 1)

        else:    
            vertex_num = randint(0, len(self.polygon.edges) - 1)
            while vertex_num == self._last_choosen_vrtx:
                vertex_num = vertex_num = randint(0, len(self.polygon.edges) - 1)

        self._last_choosen_vrtx = vertex_num

        return vertex_num

    def move(self, starting_cor: tuple[float], move_towards: int ) -> tuple[float]:
        """
        Starting from the 'starting_cor' it moves that points some fraction of distance towards given vertex.

        Parameters: 
            starting_cor [type: tuple(float)] = coordinate (x, y) of the starting location
            move_towards [type: int] = index of vertex to move towards

        Return:
            type: tuple(float)
            Resultant coordinate after moving towards given vertex
        """
        vertex = self.polygon.edges[move_towards][0]

        dx = vertex[0] - starting_cor[0]
        dy = vertex[1] - starting_cor[1]
        new_cor = (starting_cor[0] + (dx * self.r), starting_cor[1] + (dy * self.r))

        return new_cor

    def run(self, dot_size:int = 0.01) -> None:
        """
        Randomly generates a coordinate inside polygon and move that point towards
        random vertex.

        Moves a coordinate and then saves the resultant coordinate in a list. 
        This is repeated for given number of itreations

        Once moving the coordinate is stoped. It draws a dot at all coordinates saved in list.
        """
        start = time()
        print("Calculaing Coordinates.....")

        if(self._num_of_points > 0):
            xs = [None] * self._num_of_points
            ys = [None] * self._num_of_points

            xs[0], ys[0] = self._get_cor_in_polygon()

            for idx in range(1, self._num_of_points):
                towards = self._choose_rand_vertex()
                xs[idx], ys[idx] = self.move((xs[idx-1], ys[idx-1]), towards)
            
            print("Ploting Coordinates.....")
            pyplot.scatter(array(xs), array(ys), s=dot_size, c='k')

        end = time()
        print(f"Finished in {round((end - start), 3)} sec")

        self.polygon.display_vertices_name()


class DNA(Chaos):
    """
    Inherits Chaos class

    Designed to read a gentic sequence from a text file
    and then plot that sequence
    """
    def __init__(self, file_path:str, r:float = 0.5, polygon_edge_len:float = Polygon.default_edge_length):
        pyplot.title("Genetic Sequence")
        self._genetic_seq = load_filedata(file_path)
        self.r = r

        verticies_name = find_unique_char(self._genetic_seq)
        self.polygon = Polygon(len(verticies_name), polygon_edge_len)

        self.polygon.set_vetices_name(verticies_name)

    def run(self, dot_size:int = 0.01) -> None:
        """
        Randomly generates a coordinate inside polygon and move that point towards
        given vertex in genetic sequence.

        Moves a coordinate and then saves the resultant coordinate in a list. 
        This is repeated until the whole sequence is read.

        Once whole sequence is read and moving is stoped. It draws a dot at all coordinates saved in list.
        """

        start = time()
        print("Calculaing Coordinates.....")

        arr_len = len(self._genetic_seq) + 1

        xs = [None] * arr_len
        ys = [None] * arr_len
        xs[0], ys[0] = self._get_cor_in_polygon()

        for idx, vertex_to_goto in enumerate(self._genetic_seq, 1):
            xs[idx], ys[idx] = self.move((xs[idx-1], ys[idx-1]), self.polygon.vertices_name[vertex_to_goto])

        print("Ploting Coordinates.....")
        pyplot.scatter(array(xs), array(ys), s=dot_size, c='k')

        end = time()
        print(f"Finished in {round((end - start), 3)} sec\n")

        self.polygon.display_vertices_name()
