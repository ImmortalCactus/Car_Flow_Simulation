import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import heapq

class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        self.edge_lengths = [np.linalg.norm(self.vertices[e[0]]-self.vertices[e[1]]) for e in self.edges]
        self.cars = []
    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect('equal', adjustable='box')
        x, y = self.vertices.T
        x1 = [self.vertices[i[0]][0] for i in self.edges]
        x2 = [self.vertices[i[1]][0] for i in self.edges]
        y1 = [self.vertices[i[0]][1] for i in self.edges]
        y2 = [self.vertices[i[1]][1] for i in self.edges]
        plt.plot(x1, y1, x2, y2, marker = 'o')
        plt.show()
    def shortest_path(self, s, t):
        distance = np.ones((self.vertices.shape[0])) * np.inf
        src = [None] * self.vertices.shape[0]
        distance[s] = 0
        done = 0
        while(done == 0):
            done = 1
            for i, e in enumerate(self.edges):
                if(distance[e[0]]+self.edge_lengths[i] < distance[e[1]]):
                    distance[e[1]] = distance[e[0]]+self.edge_lengths[i]
                    src[e[1]] = i
                    done = 0
        if distance[t] == np.inf: return []
        path = [t]
        while(path[0]!=s):
            path = [self.edges[src[path[0]]][0], src[path[0]]] + path
        return path
    
    def add_car(self, s, t):
        self.cars.append(self.Car(s, t, self.shortest_path(s, t), self))

    class Car:
        def __init__(self, init_loc, destination, designated_path, graph):
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
    [1, 1],
    [1, 2],
    [1, 3],
    [2, 1],
    [2, 2],
    [2, 3],
    [3, 1],
    [3, 2],
    [3, 3],
]).astype('float')
data1 = np.array([
    [0, 1],
    [0, 4],
    [1, 4],
    [4, 7],
    [4, 8],
    [7, 8]
])
g = Graph(data, data1)
g.plot()
print(g.shortest_path(0,8))
