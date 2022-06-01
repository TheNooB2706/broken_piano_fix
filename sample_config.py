#rename file to config.py before use

autoconnect = True #boolean: True=autoconnect, False=do not autoconnect
autoconn_in_only = False #boolean: only autoconnect input or otherwise
autoconn_name_in = "PSR-295/293" #str: Name of the input client
autoconn_name_out = "LinuxSampler" #str: Name of the output client
buffer_size = 15 #str: size of buffer stored for extrapolating
debug = False #boolean: turn on or off debug print function
extrapolator_algorithm = "multivar_linear" #str: name of extrapolator algorithm, either linear, multivar_linear, cubic, or multivar_cubic
naive_value = 50 #int: 0<=x<=127, this value is returned instead of extrapolating if buffer is not full
note_list = {"B2":85, "F#4":70, "B3":85, "B1":90, "F#3":80, "C6":105, "C5":105, "F#5":85, "C3":105, "C2":105, "B5":105, "B4":105, "B6":105, "G#4":95, "G#3":95} #dict: notes and its threshold value, note named using alphabet and octave, and sharp (not flat). In the form of note:threshold
vel_curve = {8:0, 9:6, 19:8, 32:18, 47:35, 61:45, 77:66, 93:95, 115:127} #dict: velocity curve, automatically linear interpolated when initialising, only need to put on point you want to edit. input_vel:output_vel
