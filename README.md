# ShefJam X - OS, Remove?
A game which delets your files...


FONTS:
https://github.com/tonsky/FiraCode

beatmaptxtformat : 
"""
audio-path: <audiopath.mp3>
hit-timings: [<timing-1>, <timing-2>]
zones: [(<timing-1>, <timing-2>, [<enemy-spawn-types>])]
"""

HitTiming:
    Attributes:
        timing point within the song
    Methods:
        GetHitScore(timepoint) - great / perfect / miss depending on the timepoint given


Beatmap:
    Attributes:
        song - Song instance
        hitTimings - List of timings to hit
        arena? - the arena we are playing in
        zoneTimings - zone timings
    Methods:
        LoadFromFile(txt) - loads a saved beatmap from a text file
        Play()
        Update() - swaps zones, enemy spawn logic etc

BeatmapRenderer (Scene):
    Attributes:
        beatmap - beatmap to play
    Methods:
        Start()
        Render()
        Update()
        TakeInput()