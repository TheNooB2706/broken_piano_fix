import jack
import struct
import config
import extrapolator

#-------Const-----------
NOTEON = 0x9 # First 4 bits of status byte
#-------Callback--------
def callback(frames):
    global config
    mid_send.clear_buffer()
    for offset, indata in mid_recv.incoming_midi_events():
        if len(indata) == 3:
            status, pitch, vel = struct.unpack("3B", indata)
            if (status >> 4 == NOTEON):
                if (pitch in note_list):
                    if (vel >= config.threshold):
                        vel = extrapolator.extrapolate((client.last_frame_time+offset, pitch), note_buffer) if (note_buffer.length() == config.buffer_size) else config.naive_value
                        dprint(f"Note {pitch} exceed {config.threshold}, changing to {vel}")
                    else:
                        note_buffer.add((client.last_frame_time+offset, pitch, vel))
                else:
                    note_buffer.add((client.last_frame_time+offset, pitch, vel))
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
    temp_list = []
    for i in note_list:
        notes = parse_note(i)
        temp_list += notes
    return temp_list

def dprint(string):
    if config.debug:
        print(string)
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

client.set_process_callback(callback)
client.activate()

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
