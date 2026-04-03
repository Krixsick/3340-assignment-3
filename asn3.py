import os
import sys

class Heap:
    
    def __init__(self, number, keys):
        """ initialize heap with keys of number + 1"""
        self.keys = keys[:]
        self.number = number
        self.size = number
        self.heap = [0] + list(range(1, number + 1))
        # Position array: pos[id] = position in heap
        self.pos = [0] + list(range(1, number + 1))
        # Track whether each id is in the heap
        self.in_heap_flag = [False] + [True] * number
        self.__construct_heap()
    def __construct_heap(self):
        """construct the heap"""
        for number in range(self.size // 2, 0, -1):
            self.__shift_down(number)
 
    def __shift_up(self, position):
        """Helper function that moves elements up to restore heap"""
        while position > 1:
            parent_node = position // 2
            if self.keys[self.heap[position]] < self.keys[self.heap[parent_node]]:
                self._swap(position, parent_node)
                position = parent_node
            else:
                break
 
    def __shift_down(self, position):
        """Helper function that moves elements down to restore heap"""
        while 2 * position <= self.size:
            child_node = 2 * position
            if child_node + 1 <= self.size and self.keys[self.heap[child_node + 1]] < self.keys[self.heap[child_node]]:
                child_node += 1
            if self.keys[self.heap[child_node]] < self.keys[self.heap[position]]:
                self._swap(child_node, position)
                position = child_node
            else:
                break
    def _swap(self, pointer_1, pointer_2):
        """Helper function to swap elements in heap and update their positions"""
        heap_id_1 = self.heap[pointer_1]
        heap_id_2 = self.heap[pointer_2]
        self.heap[pointer_1], self.heap[pointer_2] = self.heap[pointer_2], self.heap[pointer_1]
        self.pos[heap_id_1], self.pos[heap_id_2] = self.pos[heap_id_2], self.pos[heap_id_1]
    
    def in_heap(self, id):
        """Returns true if element with that id is located in heap"""
        return self.in_heap_flag[id]
    def is_empty(self):
        """Returns to see if the heap is empty or not"""
        return self.size == 0
    def min_key(self):
        """Returns the minimum key in the heap"""
        return self.keys[self.heap[1]]
    def min_id(self):
        """Returns id of element with minimum key"""
        return self.heap[1]
    def key(self,id):
        """Returns key of given id in heap"""
        return self.keys[id]
    def delete_min(self):
        """Deletes and returns the element with the minimum key"""
        if self.is_empty():
            return None
        min_id = self.heap[1]
        #Move the last element to the root
        self._swap(1, self.size)
        #Remove the minimum element
        self.in_heap_flag[min_id] = False
        self.pos[min_id] = -1
        self.size -= 1
        if self.size > 0:
            self.__shift_down(1)
        return min_id
    def decrease_key(self, id, new_key):
        """Decreases the key of element id to new_key if new_key is smaller"""
        if new_key < self.keys[id]:
            self.keys[id] = new_key
            self.__shift_up(self.pos[id])
def prims_mst_algorithm(node, adjacent):
    """Prim's algorithm to find minimum"""
    INF = float('inf')
    keys = [INF] * (node + 1)
    keys[1] = 0
    parent = [0] * (node + 1)
    parent[1] = -1 
    mst_edges = []
    total_weight = 0
    min_heap = Heap(node, keys)
    while not min_heap.is_empty():
        min_vertex = min_heap.delete_min()
        if parent[min_vertex] != -1:
            parent_node = parent[min_vertex]
            weight_node = min_heap.key(min_vertex)
            mst_edges.append((parent_node, min_vertex, weight_node))
            total_weight += weight_node
        for u_neighbors, weight in adjacent[min_vertex]:
            if min_heap.in_heap(u_neighbors) and weight < min_heap.key(u_neighbors):
                min_heap.decrease_key(u_neighbors, weight)
                parent[u_neighbors] = min_vertex

    return mst_edges, total_weight

def main():
    lines = sys.stdin.read().strip().split('\n')
    #gets num of vertices and creates a nested list of len(vertices)
    num_vertices = int(lines[0].strip())
    adjacent = [[] for i in range(num_vertices + 1)]
    
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) == 3:
            i, j, w = int(parts[0]), int(parts[1]), int(parts[2])
            adjacent[i].append((j, w))
            adjacent[j].append((i, w))
 
    #Adjacency List
    print("Adjacency List Representation:")
    for min_vertex in range(1, num_vertices + 1):
        neighbors = ", ".join(f"{v} (weight: {w})" for v, w in adjacent[min_vertex])
        print(f"  Vertex {min_vertex}: {neighbors}")
    print()
    mst_edges, total_weight = prims_mst_algorithm(num_vertices, adjacent)
 
    #MST Edges
    print("Minimum Spanning Tree Edges:")
    for parent, child, weight in mst_edges:
        print(f"  ({parent}, {child}) : {weight}")
    print()
    #Weight of minimum spanning Tree
    print(f"Total weight of the minimum spanning tree is {total_weight}")
 
 
if __name__ == "__main__":
    main()