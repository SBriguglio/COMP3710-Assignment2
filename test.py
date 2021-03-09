"""
Created by Spencer Briguglio
"""
import time
import Part2
import numpy as np

if __name__ == '__main__':
    # If you uncomment out this code, it will solve a random 8-puzzle
    """
    t = Part2.Graph(mode=2)
    t.add_vertex('0', state=t.start_state)
    t.nodes += 1
    t.add_vertex('G', t.goal_state)
    t.nodes += 1
    # t.generate_play_graph(t.get_vertex('0'))
    ts = time.time()
    print(t.start_state)
    t.a_star(t.get_vertex('0'), t.get_vertex('G'))
    print("Solution")
    i = 0
    for n in t.exact:
        i += 1
        print("Step {}:".format(i))
        Part2.display_8puzzle(n.state)
    print(t.goal_state)
    te = time.time()
    print("Time: {}".format((te-ts)/1000))
    print("States: {}".format(len(t.vertexes)))
    print("Steps: {}".format(i-1))
    """
    # This code solves 5 solvable 8-puzzles
    a = np.array([[6, 8, 5],
                  [1, 0, 2],
                  [4, 3, 7]])
    b = np.array([[7, 4, 5],
                  [2, 3, 8],
                  [1, 6, 0]])
    c = np.array([[0, 1, 7],
                  [2, 8, 3],
                  [4, 6, 5]])
    d = np.array([[5, 6, 8],
                  [3, 0, 1],
                  [7, 4, 2]])
    e = np.array([[6, 2, 3],
                  [7, 8, 1],
                  [5, 4, 0]])
    s = [a, b, c, d, e]
    time_results = np.empty((3, 5))
    costs = np.empty((3, 5))
    moves = np.empty((3, 5))
    j = 0
    for st in s:
        for mode in range(0, 3):
            if mode == 0:
                print("== Misplaced ==")
            elif mode == 1:
                print("== Manhattan Distance ==")
            elif mode == 2:
                print("== Max-Mis-Man ==")
            else:
                exit(-1)
            t = Part2.Graph(mode=mode, start_state=st)
            t.add_vertex('0', state=t.start_state)
            t.nodes += 1
            t.add_vertex('G', t.goal_state)
            t.nodes += 1
            ts = time.time()
            t.a_star(t.get_vertex('0'), t.get_vertex('G'))
            Part2.display_8puzzle(t.start_state)
            print("Solution")
            i = 0
            for n in t.exact:
                print("Step {}:".format(i))
                Part2.display_8puzzle(n.state)
                i += 1
            te = time.time()
            td = te - ts
            time_results[mode, j] = td
            costs[mode, j] = i-1
            moves[mode, j] = len(t.vertexes)
            print("Time: {}".format(td / 1000))
        j += 1
    print("Run Times")
    print(time_results)
    print("Costs")
    print(costs)
    print("Moves")
    print(moves)
