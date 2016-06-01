from learning_language import MergeSubtitle

path = '/Users/guiesi/Downloads/Anomalisa.2015.BRRip.XviD.AC3-EVO/'
merge_subs = MergeSubtitle(path + 'Anomalisa.2015.BRRip.XviD.AC3-EVO.en.srt',
                           path + 'Anomalisa.2015.BRRip.XviD.AC3-EVO.pt.srt')
merge_subs.merge_subtitles(path + 'Anomalisa.2015.BRRip.XviD.AC3-EVO..srt')
