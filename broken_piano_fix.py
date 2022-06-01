import jack
import struct
import config
import extrapolator

#-------Const-----------
NOTEON = 0x9 # First 4 bits of status byte
#-------Callback--------
def callback(frames):
    global config, count
    mid_send.clear_buffer()
    for offset, indata in mid_recv.incoming_midi_events():
        if len(indata) == 3:
            status, pitch, vel = struct.unpack("3B", indata)
            if (status >> 4 == NOTEON):
                if (pitch in note_list):
                    if (vel >= note_list[pitch]):
                        vel = extrapolator.extrapolate((client.last_frame_time+offset, pitch), note_buffer) if (note_buffer.length() == config.buffer_size) else config.naive_value
                        dprint(f"Note {pitch} exceed {note_list[pitch]}, changing to {vel}")
                        count += 1
                        print(f"This program saved your ears {count} times since ran...", end = "\r")
                    else:
                        note_buffer.add((client.last_frame_time+offset, pitch, vel))
                else:
                    note_buffer.add((client.last_frame_time+offset, pitch, vel))
                vel = map_velocity(vel, config.vel_curve)
            mid_send.write_midi_event(offset, (status, pitch, vel))
        else:
            mid_send.write_midi_event(offset, indata)
#-------Funcs-----------
def connect_port(port_obj, port_list, portname):
    if port_list:
        port_obj.connect(port_list[0])
        dprint(f"Connected {port_obj.name} to {port_list[0].name}")
    else:
        print(f"Port {portname} not found!")

def parse_note(note):
    import re
    base_notes = {"C":12, "C#":13, "D":14, "D#":15, "E":16, "F":17, "F#":18, "G":19, "G#":20, "A":21, "A#":22, "B":23}
    regex = re.compile("([a-zA-Z#]+)([0-9]+)")
    match = regex.split(note)
    if len(match) == 1:
        return [i for i in [i*12+base_notes[match[0]] for i in range(10)] if i <= 127]
    elif len(match) == 4:
        return [int(match[2])*12+base_notes[match[1]]]
    
def initialise_note_list(note_list):
    temp_dict = {}
    for i in note_list:
        notes = parse_note(i)
        for j in notes:
            temp_dict[j] = note_list[i]
    return temp_dict

def dprint(string):
    if config.debug:
        print(string)

def initialise_vel_curve(vel_curve_raw):
    vel_curve = dict(vel_curve_raw) #making a local copy
    if 0 not in vel_curve:
        vel_curve[0] = 0
    if 127 not in vel_curve:
        vel_curve[127]=127
    for i in vel_curve.items():
        if not ((0 <= i[0] <= 127) and (0 <= i[1] <= 127)):
            raise ValueError(f"MIDI velocity in velocity curve out of range: {i[0]}:{i[1]}")
    vel_curve = dict(sorted(vel_curve.items(), key=lambda x:x[0])) #sorting velocity curve dictionary
    
    temp_vel_list = [i for i in vel_curve.items()]
    for i in range(len(temp_vel_list)-1): #generating lookup table for mapping
        lower = temp_vel_list[i] #lower bound, tuple in the form of (input, mapped output)
        upper = temp_vel_list[i+1] #upper bound
        for j in range(lower[0]+1, upper[0]): #j is the input value
            mapped_output = round((j-lower[0])*(upper[1]-lower[1])/(upper[0]-lower[0])+lower[1]) #classic y=mx+c
            vel_curve[j] = mapped_output #appending into dictionary
    vel_curve = dict(sorted(vel_curve.items(), key=lambda x:x[0])) #resorting, technically not needed but just do it anyway
    return vel_curve

def map_velocity(input_vel, vel_curve):
    return vel_curve[input_vel]
#-------Class-----------
class Buffer:
    def __init__(self, size):
        """Initialise buffer object.
Parameters
----------
size: int
    Size of list of events to keep for extrapolation algorithm"""
        self.size = size
        self.buff = []
    
    def add(self, events):
        """Add events to buffer object.
Parameters
----------
events: tuple
    Length of 3, consist of offset, pitch, vel. Offset should be added with last_frame_time so that the extrapolator works across cycles."""
        self.buff.append(events)
        self.buff = self.buff[-self.size:]

    def length(self):
        return len(self.buff)
#-------Vars------------
client = jack.Client("Broken Piano Filter")

mid_recv = client.midi_inports.register("midi_in")
mid_send = client.midi_outports.register("midi_out")

note_buffer = Buffer(config.buffer_size)
count = 0

client.set_process_callback(callback)
client.activate()
dprint(f"Using {config.extrapolator_algorithm} alg.")

config.vel_curve = initialise_vel_curve(config.vel_curve)

if config.autoconnect:
    conn_in = client.get_ports(name_pattern=config.autoconn_name_in, is_output=True, is_midi=True)
    connect_port(mid_recv, conn_in, config.autoconn_name_in)
    if not config.autoconn_in_only:
        conn_out = client.get_ports(name_pattern=config.autoconn_name_out, is_input=True, is_midi=True)
        connect_port(mid_send, conn_out, config.autoconn_name_out)

note_list = initialise_note_list(config.note_list)
dprint(f"Note enabled: {note_list}")
    
print('#' * 80)
print('Press enter to quit...')
print('#' * 80)
input()
