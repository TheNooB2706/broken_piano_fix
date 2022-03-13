# broken_piano_fix
TLDR; Some Python scripts to fix my broken piano keyboard.  

This program routes MIDI through JACK.  

I own a really old Yamaha PSR series 61 keys keyboard, and it has broken velocity sensors on some keys. Those key will randomly spit out notes with 127 velocity and make me deaf, so this program basically detect this and correct it. It first check if the note is above certain threshold, if so it apply regression with data from a buffer of previous note to "predict" the actual velocity. As you might have guessed I don't even know if this is a great idea at all in term of accuracy, but at least now I'm not gonna become deaf. There are several regression algorithm that can be set, but I found mutivariate linear regression seems to work best. Seriously, I don't think anyone will have the same problem with me, but I'll put this out anyway.
