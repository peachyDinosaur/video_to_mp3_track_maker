import ffmpeg
from sys import argv

""" split_wav `audio file` `time listing`

    `audio file` is any file known by local FFmpeg
    `time listing` is a file containing multiple lines of format:
        `start time` `end time` output name 

    times can be either MM:SS or S*
"""

_in_file = argv[1]
destination = argv[3]

def make_time(elem):
    # allow user to enter times on CLI
    t = elem.split(':')
    try:
        if len(t) ==2:
        # will fail if no ':' in time, otherwise add together for total seconds
            return int(t[0]) * 60 + float(t[1])
        elif len(t) ==3:
            return int(t[0])*60*60 + int(t[1])*60 + float(t[2])
    except IndexError:
        return float(t[0])

def collect_from_file():
    """user can save times in a file, with start and end time on a line"""

    time_pairs = []
    with open(argv[2]) as in_times:
        for l, line in enumerate(in_times):
            tp = line.split()
            tp[0] = make_time(tp[0])
            tp[1] = make_time(tp[1]) - tp[0]
            # if no name given, append line count
            if len(tp) < 3:
                tp.append(str(l) + '.wav')

            time_pairs.append(tp)
    return time_pairs

def main():
    for i, tp in enumerate(collect_from_file()):
        # open a file, from `ss`, for duration `t`
        stream = ffmpeg.input(_in_file, ss=tp[0], t=tp[1])
        # output to named file
        stream = ffmpeg.output(stream, "{}{}.mp3".format(destination, tp[2]))
        # this was to make trial and error easier
        ffmpeg.run(stream)


if __name__ == '__main__':
    main()