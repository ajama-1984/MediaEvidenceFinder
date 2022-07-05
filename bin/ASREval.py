import jiwer
from pathlib import Path
from audio_extraction import splitAudio, convertMillis

def ASREval():
    target_test = r"C:\Users\Ahmed\MediaEvidenceFinder\TESTCASE001\Transcripts\transcribed_audio_speech16bit2a.txt"
    target_pred = r"C:\Users\Ahmed\MediaEvidenceFinder\TESTCASE001\Transcripts\transcribed_audio_speech16bit2.txt"

    target_test = target_test.replace('\\n', '\n')
    target_pred = target_pred.replace('\\n', '\n')

    with open(target_test) as pred:
        preds1 = Path(target_test).read_text()
        print(preds1)

    with open(target_pred) as test:
        refs1 = Path(target_pred).read_text()
        print(refs1)

    transformation = jiwer.Compose([
        jiwer.ToLowerCase(),
        jiwer.RemoveWhiteSpace(replace_by_space=True),
        jiwer.RemoveMultipleSpaces(),
        jiwer.ReduceToListOfListOfWords(word_delimiter=" ")
    ])

    wer_score = jiwer.wer(refs1, preds1, truth_transform=transformation, hypothesis_transform=transformation)

    print("WER = " + (str(int(wer_score * 100)) + "%"))


if __name__ == '__main__':
    casepath = r"C:\Users\Ahmed\MediaEvidenceFinder\TESTCASE001"
    filename = r"C:\Users\Ahmed\MediaEvidenceFinder\TESTCASE001\ExtractedAudioFiles\7mgSPHdxooaudio.wav"
    chunklist, lengthaudio, counter = splitAudio(filename,casepath)
    print(chunklist)
    convertMillis()