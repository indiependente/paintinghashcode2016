import hashcode as hc
import numpy as np
import sys
m = hc.read_image(sys.argv[1])


best_score = 0
best_delta = 0

for delta in np.nditer(np.arange(0, 0.3, 0.005)):
    m_work, all_commands = hc.algo(m, np.zeros(np.shape(m)), delta)

    print 'Dimensions:',np.shape(m)
    print 'Cells:',np.shape(m)[0]*np.shape(m)[1]


    print '# commands:', len(all_commands)
    score = np.shape(m)[0]*np.shape(m)[1] - len(all_commands)
    print delta, 'Score: ', score
    if score > best_score:
        best_score = score
        best_delta = delta
        best_cmds = all_commands

np.savetxt(sys.argv[1]+'.m_work', m_work, fmt='%1.0f')
str_cmds = [str(len(best_cmds))]
str_cmds += [' '.join(map(str,list(best_cmds[i]))) for i in xrange(len(best_cmds))]

np.savetxt(sys.argv[1]+'.cmds', str_cmds, fmt='%s')
print 'Best score -->', best_score
print 'Delta =', best_delta
print 'Best number of commands =',len(best_cmds)