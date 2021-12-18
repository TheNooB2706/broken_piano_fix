import jack
import struct
from config import *
#-------Vars------------

#-------Const-----------
NOTEON = 0x9 # First 4 bits of status byte
#-------Callback--------
def callback(frames):
    mid_send.clear_buffer()
    for offset, indata in mid_recv.incoming_midi_events():
        if len(indata) == 3:
            status, pitch, vel = struct.unpack("3B", indata)
            if (status >> 4 == NOTEON) and (pitch in note_list) and (vel >= threshold):
                vel = 50 #naively change velocity to something constant
            mid_send.write_midi_event(offset, (status, pitch, vel))
        else:
            mid_send.write_midi_event(offset, indata)
#-------Funcs-----------
def connect_port(port_obj, port_list, portname):
    if port_list:
        port_obj.connect(port_list[0])
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

client = jack.Client("Broken Piano Filter")

mid_recv = client.midi_inports.register("midi_in")
mid_send = client.midi_outports.register("midi_out")

client.set_process_callback(callback)
client.activate()

if autoconnect:
    conn_in = client.get_ports(name_pattern=autoconn_name_in, is_input=True, is_midi=True)
    connect_port(mid_recv, conn_in, autoconn_name_in)
    if not autoconn_in_only:
        conn_out = client.get_ports(name_pattern=autoconn_name_out, is_output=True, is_midi=True)
        connect_port(mid_send, conn_out, autoconn_name_out)

note_list = initialise_note_list(note_list)
    
input("Enter to exit")
