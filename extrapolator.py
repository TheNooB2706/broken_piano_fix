import numpy as np
from sklearn.linear_model import LinearRegression
from config import debug, extrapolator_algorithm

def dprint(string):
    if debug:
        print(string)

def linear_extrapolator(target_offset, buffer_obj):
    """Predict velocity with simple linear model.
Parameters
----------
target_offset: int
    Offset of the midi event return from jack.OwnMidiPort.incoming_midi_events()
buffer_obj: Buffer
    Buffer of the note events declared in broken-piano-fix"""
    x = np.array([i[0]-buffer_obj.buff[0][0] for i in buffer_obj.buff]).reshape((-1, 1))
    y = np.array([i[2] for i in buffer_obj.buff])
    dprint(x)
    dprint(y)
    model = LinearRegression().fit(x, y)
    vel_pred = round(model.predict([[target_offset-buffer_obj.buff[0][0]]])[0])
    dprint(vel_pred)
    if 0 <= vel_pred <= 127:
        return vel_pred
    else:
        temp_arr = [i[2] for i in buffer_obj.buff]
        return round(sum(temp_arr)/len(temp_arr))
    
func_dict = {"simple_linear":linear_extrapolator}
extrapolate = func_dict[extrapolator_algorithm]
