import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time


class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.edge_lengths = [np.linalg.norm(self.vertices[e[0]]-self.vertices[e[1]]) for e in self.edges]
        self.car1 = self.Car(0, [0,0,1,1,2], 2, self)
        while(self.car1.update(0.2) != 1):
            print(self.car1.coordinaties())
            time.sleep(1)
    def plot(self):
        x, y = self.vertices.T
        x1 = [self.vertices[i[0]][0] for i in self.edges]
        x2 = [self.vertices[i[1]][0] for i in self.edges]
        y1 = [self.vertices[i[0]][1] for i in self.edges]
        y2 = [self.vertices[i[1]][1] for i in self.edges]
        plt.plot(x1, y1, x2, y2, marker = 'o')
        plt.show()
    class Car:
        def __init__(self, init_loc, designated_path, destination, graph):
            self.on_vertex = True
            self.loc_vertex = init_loc
            self.loc_edge = -1
            self.pos_edge = float(0)
            self.designated_path = designated_path
            self.destination = destination
            self.speed = float(1)
            self.graph = graph
        def update(self, interval_length):
            time_left = interval_length
            while(time_left > 0):
                if(self.on_vertex):
                    if(self.loc_vertex == self.destination):
                        return 1
                    self.adjust_path() 
                    self.adjust_speed()
                    self.designated_path = self.designated_path[1:]
                    self.on_vertex = False
                    self.loc_edge = self.designated_path[0]
                    self.pos_edge = self.speed*time_left/self.graph.edge_lengths[self.loc_edge]
                else:
                    self.pos_edge += self.speed*time_left/self.graph.edge_lengths[self.loc_edge]

                if(self.pos_edge >= 1):
                    time_left = (self.pos_edge - 1)*self.graph.edge_lengths[self.loc_edge]/self.speed
                    self.loc_vertex = self.graph.edges[self.loc_edge][1]
                    self.on_vertex = True
                    self.pos_edge = 0.0
                    self.loc_edge = -1
                    self.designated_path = self.designated_path[1:]
                else:
                    time_left = 0
            return 0

        def adjust_path(self):
            return
        def adjust_speed(self):
            return
        def coordinaties(self):
            if(self.on_vertex):
                return self.graph.vertices[self.loc_vertex]
            else:
                return (1-self.pos_edge) * self.graph.vertices[self.graph.edges[self.loc_edge][0]] + self.pos_edge * self.graph.vertices[self.graph.edges[self.loc_edge][1]]
data = np.array([
    [1, 2],
    [2, 3],
    [3, 6],
]).astype('float')
data1 = np.array([
    [0, 1],
    [1, 2]
])
g = Graph(data, data1)
g.plot()