import turtle
from matplotlib import pyplot
from math import pi, cos, sin
      
class Polygon(object):
    min_sides = 3
    default_edge_length = 1.0

    def __init__(self, sides:int= min_sides, edge_length:float = default_edge_length) -> None:
        # polygon can not have less than 3 sides
        if sides < 3: sides = 3 

        self.edges = self._create_polygon(sides, edge_length)
        self.vertices_name = None
    
    def _create_vertices_name(self, count) -> dict:
        a = ord('A')
        names = {chr(a+i):i for i in range(count)} #Dictionary Comprehension

        return names

    def set_vetices_name(self, names:dict = None) -> None:
        self.vertices_name = self._create_vertices_name(len(self.edges)) if (names is None) else names

    def display_vertices_name(self) -> None:
        x_bounds = self.get_x_bounds()
        y_bounds = self.get_y_bounds()

        if not (self.vertices_name is None):

            for name in self.vertices_name:
                x, y = self.edges[self.vertices_name[name]][0]

                text_x = x if x >= x_bounds[1] else x - 0.03
                text_y = y if y >= y_bounds[1] else y - 0.03

                pyplot.text(text_x, text_y, name, fontsize= 20, color="red")
                            
    def contains(self, x:float, y:float) -> bool:
        """
        Checks if a Point(x, y) is inside Polygon
        Parameters
            x [type: float] = X value of coordinate
            y [type: float] = Y value of coordinate

        """

        #Uses Ray Cast Algorithim
        intersection_count = 0

        #edge = ((starting position of egde), (ending position of egde))
        for edge in self.edges:
            (start_x, start_y), (end_x, end_y) = edge 

            #using to avoid Divison by 0 exception
            try: 
                intersection_x = ((y - start_y)/(end_y - start_y)) * (end_x - start_x)
            except:
                intersection_x = 0

            # Conditon 1: if y is less that both staring y coordinate and ending y coordinate or y is greater that both staring y coordinate and ending y coordinate
            # Conditon 2: Calculating interstion point between line Y = y(function argument one) and edge 
            #             and checking if that x(given as argument) is less than calculated point's x(start_x + intersection_x)
            if ((y < start_y) != (y < end_y)) and (x < start_x + intersection_x):
                intersection_count += 1

        return intersection_count%2 == 1

    def _rotate_polygon(self, verticies: list[tuple[float]], theta:float) -> list[tuple[float]]:
        """
        Rotates the Polygon Anti-Clockwise using Rotation Matrix by given theta in radians

        Parameters:
            verticies [type: list] = all the coordinates of the corner/vertex of polygon
            theta [type: float] = angle in radians

        """
        rotation_matrix = [[cos(theta), -sin(theta)], [sin(theta), cos(theta)]]

        for i in range(len(verticies)):
            x = rotation_matrix[0][0] * verticies[i][0] + rotation_matrix[0][1] * verticies[i][1]
            y = rotation_matrix[1][0] * verticies[i][0] + rotation_matrix[1][1] * verticies[i][1]

            verticies[i] = [x, y]

    def _create_polygon(self, sides:int, edge_len: float) -> list[tuple]:
        """
        Create a Polygon using Turtle Graphics.

        Parametres:
            sides: Number of sides of Polygon
            side_length: Length of Sides of a Polygon

        Returns:
            List of Edges of Polygon
            Example:
                Square Edges = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]
                Element inside list represents coordinates of verticies. (x, y)
        """
        interior_angle = ((sides - 2) * pi) / sides # angle between two edges
        radius = edge_len/(2*cos(interior_angle/2)) # from centre of polygon to vertex

        #drawing polygon
        turtle.speed(0)
        turtle.begin_poly()
        turtle.circle(radius, steps=sides)
        turtle.end_poly()

        #geting coordinates of verticies of polygon
        verticies = list(turtle.get_poly())
        turtle.bye()

        self._rotate_polygon(verticies,  -(pi - interior_angle) / 2)

        pyplot.plot(*zip(*verticies), color= 'k')

        edges = []
 
        for i in range(len(verticies)):
            verticies[i] = (round(verticies[i][0],3), round(verticies[i][1],3))

        # creating edges
        for idx, vertex in enumerate(verticies[:-1]):
            edges.append((vertex, verticies[idx+1]))

        return edges

    def get_x_bounds(self) -> tuple[float]:
        """
        Returns Smallest and Biggest x value polygon reaches. 

        Example:
            coords = [(0,0), (1,0), (0.5,1), (0,0)]

            returns (0, 1)
        """

        biggest_xcor = 0
        for edge in self.edges:
            if edge[0][0] > biggest_xcor: biggest_xcor = edge[0][0]

        smallest_xcor = 0
        for edge in self.edges:
            if edge[0][0] < smallest_xcor: smallest_xcor = edge[0][0]

        return (smallest_xcor, biggest_xcor)

    def get_y_bounds(self) -> tuple[float]:
        """
        Returns Lowest and Highest y value polygon reaches. 

        Example:
            coords = [(0,0), (1,0), (0.5,1), (0,0)]

            returns (0, 1)
        """

        biggest_ycor = 0 
        for edge in self.edges:
            if edge[0][1] > biggest_ycor: biggest_ycor = edge[0][1]
             
        smallest_ycor = 0
        for edge in self.edges:
            if edge[0][1] < smallest_ycor: smallest_ycor = edge[0][1]


        return (smallest_ycor, biggest_ycor)