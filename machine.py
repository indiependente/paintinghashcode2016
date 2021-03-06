import numpy as np
import sys
import hashcode as hc

def parse_and_execute_command(command, matrix):
    cmds = {'PAINT_SQUARE' : hc.PAINT_SQUARE,
            'PAINT_LINE' : hc.PAINT_LINE,
            'ERASE_CELL' : hc.ERASE_CELL
    }
    cmds[command[0]](*map(int, command[1:]), matrix = matrix)

def execute(commands, N, M):
    m = np.zeros((N, M))
    n = int(commands[0]) + 1
    for i in xrange(1, n):
        parse_and_execute_command(commands[i].split(' '), m)
    return m

def check(result, original_img):
    return (result == original_img).all()

def main(cmds_path, img_path):
    img_matrix = hc.read_image(img_path)
    N = np.shape(img_matrix)[0]
    M = np.shape(img_matrix)[1]
    with open(cmds_path) as f:
        if check(execute(f.readlines(), N, M), img_matrix):
            print 'Match.'
        else:
            print '>>> Mismatch!'

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])
