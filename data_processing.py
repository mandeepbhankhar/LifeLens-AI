import numpy as np
def completion_rate(done,total): return float(np.clip(done/total*100,0,100)) if total else 0.0
