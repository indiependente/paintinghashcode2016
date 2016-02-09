import hashcode as hc
import numpy as np
import sys
m = hc.read_image(sys.argv[1])


best_score = 0
best_delta = 0

for delta in np.nditer(np.arange(0, 0.3, 0.01)):
    m_work, all_commands = hc.algo(m, np.zeros(np.shape(m)), delta)

    print 'Dimensions:',np.shape(m)
    print 'Cells:',np.shape(m)[0]*np.shape(m)[1]

    np.savetxt(sys.argv[1]+'.m_work', m_work, fmt='%1.0f')
    np.savetxt(sys.argv[1]+'.cmds', np.asarray(all_commands), fmt='%s')
    print '# commands:', len(all_commands)
    score = np.shape(m)[0]*np.shape(m)[1] - len(all_commands)
    print delta, 'Score: ', score
    if score > best_score:
        best_score = score
        best_delta = delta

print 'Best score -->', best_score
print 'Delta =', best_delta
