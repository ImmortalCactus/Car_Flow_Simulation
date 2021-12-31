import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import random
import time
import copy

ALPHA = 0.1
class Graph:
    def __init__(self, vertices, edges, time_interval):
        self.timer = 0
        self.vertices = vertices
        self.edges = edges
        self.edge_lengths = np.array([np.linalg.norm(self.vertices[e[0]]-self.vertices[e[1]]) for e in self.edges])
        self.edge_cost = self.edge_lengths.copy()
        self.cars = []
        self.time_interval = time_interval
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect('equal', adjustable='box')
    def plot(self):
        for e in self.edges:
            plt.plot([self.vertices[e[0]][0], self.vertices[e[1]][0]],[self.vertices[e[0]][1], self.vertices[e[1]][1]], color="blue")
        ani = animation.FuncAnimation(self.fig, self.update, frames = 1200, interval=self.time_interval, blit = True)
        plt.show()
    def shortest_path(self, s, t):
        distance = np.ones((self.vertices.shape[0])) * np.inf
        src = [None] * self.vertices.shape[0]
        distance[s] = 0
        done = 0
        while(done == 0):
            done = 1
            for i, e in enumerate(self.edges):
                if(distance[e[0]]+self.edge_cost[i] < distance[e[1]]):
                    distance[e[1]] = distance[e[0]]+self.edge_cost[i]
                    src[e[1]] = i
                    done = 0
                # assume bidirectional edge
        if distance[t] == np.inf:
            return []
        path = [t]
        while(path[0]!=s):
            path = [self.edges[src[path[0]]][0], src[path[0]]] + path
        return path
    
    def add_car(self, s, t, start_time):
        self.cars.append(self.Car(s, t, start_time, self.shortest_path(s, t), self))

    def update(self, i):
        new_cost = self.edge_lengths.copy()
        for c in self.cars:
            if not c.on_vertex:
                new_cost[c.loc_edge]+=self.edge_lengths[c.loc_edge]
        self.edge_cost = (1-ALPHA)*self.edge_cost + (ALPHA)*new_cost
        l = []
        for c in self.cars:
            if self.timer >= c.start_time:
                c.update()
                coord = c.coordinates()
                c.dot.set_data(coord[0],coord[1])
                l.append(c.dot)
        self.timer += self.time_interval
        return l
    class Car:
        def __init__(self, init_loc, destination, start_time, designated_path, graph):
            self.start_time = start_time
            self.on_vertex = True
            self.loc_vertex = init_loc
            self.loc_edge = -1
            self.pos_edge = float(0)
            self.designated_path = designated_path
            self.destination = destination
            self.speed = float(1)
            self.graph = graph
            self.dot, = self.graph.ax.plot([],[],marker="o", linestyle='', markersize=5, color = "red")
        def update(self):
            time_left = self.graph.time_interval
            while(time_left > 0):
                if(self.on_vertex):
                    if(self.loc_vertex == self.destination):
                        return 1
                    self.adjust_path() 
                    self.designated_path = self.designated_path[1:]
                    self.on_vertex = False
                    if(len(self.designated_path) == 0):
                        return 1
                    self.loc_edge = self.designated_path[0]
                    
                self.adjust_speed()
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
            self.designated_path = self.graph.shortest_path(self.designated_path[0],self.designated_path[-1])
            return
        def adjust_speed(self):
            count = 0
            for c in self.graph.cars:
                if(c.loc_edge == self.loc_edge and c.pos_edge > self.pos_edge):
                    count = count + 1
            self.speed = 1/(count+1)
            return
        def coordinates(self):
            if(self.on_vertex):
                return self.graph.vertices[self.loc_vertex]
            else:
                return (1-self.pos_edge) * self.graph.vertices[self.graph.edges[self.loc_edge][0]] + self.pos_edge * self.graph.vertices[self.graph.edges[self.loc_edge][1]]

d = []
for i in range(10):
    for j in range(10):
        d.append([i,j])

data = np.array(d)

d=[]
for i in range(100):
    if(i%10 != 9):
        if(random.uniform(0,1)>0.2):
            d.append([i,i+1])
            d.append([i+1,i])
    if(i<90):
        if(random.uniform(0,1)>0.2):
            d.append([i,i+10])
            d.append([i+10,i])
data1 = np.array(d)
g = Graph(data, data1, 0.01)

for i in range(100):
    g.add_car(0, 99, 0.3*i)

g.plot()
