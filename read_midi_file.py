import mido

if __name__ == '__main__':
    mid = mido.MidiFile('music/simple_test.mid')
    print(mid)
    for msg in mid.tracks[0]:
        match msg:
            case mido.MetaMessage(type='time_signature'):
                print(f'time_signature={msg.numerator}/{msg.denominator}')
            case mido.MetaMessage(type='set_tempo'):
                print(f'tempo={msg.tempo}')
