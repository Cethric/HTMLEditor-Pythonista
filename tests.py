import notification
import motion

motion.start_updates()

old = None 

for _ in range(0, 100):
    curr = motion.get_attitude()
    if old != None:
        x = old[0] - curr[0]
        y = old[1] - curr[1]
        z = old[2] - curr[2]
        print x, y, z
    old = curr
    
motion.stop_updates()
