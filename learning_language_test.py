from learning_language import MergeSubtitle


path = '/Users/guiesi/Downloads/torrent/Penny.Dreadful.S03E04.720p.HDTV.x264-AVS[rarbg]/'
merge_subs = MergeSubtitle(path + 'Penny.Dreadful.S03E04.720p.HDTV.x264-AVS.en.srt',
                          path + 'Penny.Dreadful.S03E04.720p.HDTV.x264-AVS.pt.srt')
merge_subs.merge_subtitles(path + 'teste.srt')

path = '/Users/guiesi/Downloads/torrent/The.Flash.2014.S02E23.HDTV.x264-LOL[ettv]/'
merge_subs = MergeSubtitle(path + 'the.flash.2014.223.hdtv-lol[ettv].en.srt',
                           path + 'the.flash.2014.223.hdtv-lol[ettv].pt.srt')
merge_subs.merge_subtitles(path + 'teste.srt')