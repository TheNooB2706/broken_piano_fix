import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from config import debug, extrapolator_algorithm

def dprint(string):
    if debug:
        print(string)
        
def returnvel(vel_pred, y):
    if 0 <= vel_pred <= 127:
        return vel_pred
    else:
        return round(np.mean(y))

def linear_extrapolator(events, buffer_obj):
    """Predict velocity with simple linear model.
Parameters
----------
events: tuple
    Length of 2, consist of offset, pitch.
buffer_obj: Buffer
    Buffer of the note events declared in broken-piano-fix"""
    target_offset, pitch = events
    x = np.array([i[0]-buffer_obj.buff[0][0] for i in buffer_obj.buff]).reshape((-1, 1))
    y = np.array([i[2] for i in buffer_obj.buff])
    dprint(x)
    dprint(y)
    model = LinearRegression().fit(x, y)
    vel_pred = round(model.predict([[target_offset-buffer_obj.buff[0][0]]])[0])
    #dprint(f"R^2: {model.score(x, y)}")
    dprint(f"Predicted: {vel_pred}")
    return returnvel(vel_pred, y)
        
def multivar_linear_extrapolator(events, buffer_obj):
    """Predict velocity with multivariable (pitch) linear model.
Parameters
----------
events: tuple
    Length of 2, consist of offset, pitch.
buffer_obj: Buffer
    Buffer of the note events declared in broken-piano-fix"""
    target_offset, pitch = events
    x = [[i[0]-buffer_obj.buff[0][0], i[1]] for i in buffer_obj.buff]
    y = [i[2] for i in buffer_obj.buff]
    x, y = np.array(x), np.array(y)
    dprint(x)
    dprint(y)
    model = LinearRegression().fit(x, y)
    vel_pred = round(model.predict([[target_offset-buffer_obj.buff[0][0], pitch]])[0])
    #dprint(f"R^2: {model.score(x, y)}")
    dprint(f"Predicted: {vel_pred}")
    return returnvel(vel_pred, y)
    
def cubic_extrapolator(events, buffer_obj):
    """Predict velocity with simple cubic model.
Parameters
----------
events: tuple
    Length of 2, consist of offset, pitch.
buffer_obj: Buffer
    Buffer of the note events declared in broken-piano-fix"""
    target_offset, pitch = events
    x = np.array([i[0]-buffer_obj.buff[0][0] for i in buffer_obj.buff]).reshape((-1, 1))
    y = np.array([i[2] for i in buffer_obj.buff])
    transformer = PolynomialFeatures(degree=3, include_bias=False)
    transformer.fit(x)
    x_ = transformer.transform(x)
    dprint(x_)
    dprint(y)
    model = LinearRegression().fit(x_, y)
    vel_pred = round(model.predict(transformer.transform([[target_offset-buffer_obj.buff[0][0]]]))[0])
    #dprint(f"R^2: {model.score(x_, y)}")
    dprint(f"Predicted: {vel_pred}")
    return returnvel(vel_pred, y)

def multivar_cubic_extrapolator(events, buffer_obj):
    """Predict velocity with simple cubic model.
Parameters
----------
events: tuple
    Length of 2, consist of offset, pitch.
buffer_obj: Buffer
    Buffer of the note events declared in broken-piano-fix"""
    target_offset, pitch = events
    x = [[i[0]-buffer_obj.buff[0][0], i[1]] for i in buffer_obj.buff]
    y = [i[2] for i in buffer_obj.buff]
    x, y = np.array(x), np.array(y)
    transformer = PolynomialFeatures(degree=3, include_bias=False)
    transformer.fit(x)
    x_ = transformer.transform(x)
    dprint(x_)
    dprint(y)
    model = LinearRegression().fit(x_, y)
    vel_pred = round(model.predict(transformer.transform([[target_offset-buffer_obj.buff[0][0], pitch]]))[0])
    #dprint(f"R^2: {model.score(x_, y)}")
    dprint(f"Predicted: {vel_pred}")
    return returnvel(vel_pred, y)

func_dict = {
    "simple_linear": linear_extrapolator,
    "multivar_linear": multivar_linear_extrapolator,
    "simple_cubic": cubic_extrapolator,
    "multivar_cubic": multivar_cubic_extrapolator,
    }
extrapolate = func_dict[extrapolator_algorithm]
