import jiwer
from pathlib import Path
import pandas
import shutil, random, os
from moviepy.editor import AudioFileClip
from ASR_S2T_Experiment_DeepSpeech import deepSpeechEvaluation
from ASR_S2T_Experiment_PocketSphinx import PocketSphinxEvaluation
from ASR_S2T_Experiment_Kaldi import kaldiEvaluation

# def random_file_selection():
#     filename = r"../dataset/commonVoice/tsv/validated.tsv"
#     n = sum(1 for line in open(filename, encoding="utf8")) - 1
#     s = 5  # desired sample size
#     skip = sorted(random.sample(range(1, n + 1), n - s))
#     df = pandas.read_csv(filename, skiprows=skip, sep='\t')
#     testfiles = df["path"]
#     print(testfiles)
#     return testfiles
#
# def find(filelist, folderpath):
#     for i in filelist:
#         for root, dirs, files in os.walk(folderpath):
#             if i in files:
#                 print("File " + i + " Has been found in the dataset folder")
#                 return os.path.join(root, i)


def randomFileSelector():
    dirpath = r'Z:\DissertationSoftwareDev\files\cv-corpus-9.0-2022-04-27\en\clips'
    destDirectory = r'C:\Users\Ahmed\PycharmProjects\SpeechTranscription\dataset\commonVoice\clips'
    filenames = random.sample(os.listdir(dirpath), 5)
    for fname in filenames:
        srcpath = os.path.join(dirpath, fname)
        print(srcpath)
        print (destDirectory)
        shutil.copy(srcpath, destDirectory)

def retrieveHumanBaseline():
    validated_dataset_transcripts = r"../dataset/commonVoice/tsv/validated.tsv"
    datasetdirectory = r"../dataset/commonVoice/clips"
    audiodata_agregat = pandas.DataFrame()
    for datasetfiles in os.listdir(datasetdirectory):
        f = os.path.join(datasetdirectory, datasetfiles)
        if os.path.isfile(f):
            directory, audiofilename = os.path.split(f)
            df = pandas.read_csv(validated_dataset_transcripts, sep='\t')
            audiodata = df[df["path"] == audiofilename]
            audioDataRow = audiodata.iloc[:,1:3]
            audiodata_agregat = audiodata_agregat.append(audioDataRow, True)

    print(audiodata_agregat)
    audiodata_agregat.to_csv('../dataset/commonVoice/validatedTranscripts/cV50SampleTranscripts', index=False)

def extractDatasetAudio():
    datasetdirectory = r"../dataset/commonVoice/clips"
    extractedAudioDirectory = os.path.abspath("../dataset/commonVoice")
    test1 = os.path.abspath(datasetdirectory)
    testlist = []
    for datasetfiles in os.listdir(datasetdirectory):
        f = os.path.join(datasetdirectory, datasetfiles)
        if os.path.isfile(f):
            datasetfilepath = os.path.abspath(f)
            filename = Path(datasetfilepath).stem
            extractedAudioPath = extractedAudioDirectory + "\\extractedAudio\\" + filename + ".wav"
            print("Extracted Audio Path: " + os.path.normpath(extractedAudioPath))
            testlist.append(os.path.normpath(extractedAudioPath))
            audioclip = AudioFileClip(datasetfilepath)
            audioclip.write_audiofile(extractedAudioPath, nbytes=2, codec='pcm_s16le',
                                      ffmpeg_params=["-ac", "1", "-ar", "16000"])
    return testlist

# def ASREval(target_test,target_pred):
#     target_test = r"C:\Users\Ahmed\MediaEvidenceFinder\TESTCASE001\Transcripts\transcribed_audio_speech16bit2a.txt"
#     target_pred = r"C:\Users\Ahmed\MediaEvidenceFinder\TESTCASE001\Transcripts\transcribed_audio_speech16bit2.txt"
#
#     target_test = target_test.replace('\\n', '\n')
#     target_pred = target_pred.replace('\\n', '\n')
#
#     with open(target_test) as pred:
#         preds1 = Path(target_test).read_text()
#         print(preds1)
#
#     with open(target_pred) as test:
#         refs1 = Path(target_pred).read_text()
#         print(refs1)
#
#     transformation = jiwer.Compose([
#         jiwer.ToLowerCase(),
#         jiwer.RemoveWhiteSpace(replace_by_space=True),
#         jiwer.RemoveMultipleSpaces(),
#         jiwer.ReduceToListOfListOfWords(word_delimiter=" ")
#     ])
#
#     wer_score = jiwer.wer(refs1, preds1, truth_transform=transformation, hypothesis_transform=transformation)
#
#     print("WER = " + (str(int(wer_score * 100)) + "%"))



def ASREval(ground_truth ,hypothesis, asrengine):
    transformation = jiwer.Compose([
        jiwer.ToLowerCase(),
        jiwer.RemoveWhiteSpace(replace_by_space=True),
        jiwer.RemoveMultipleSpaces(),
        jiwer.ReduceToListOfListOfWords(word_delimiter=" ")
    ])

    ground_truth = jiwer.RemovePunctuation()(ground_truth)
    hypothesis = jiwer.RemovePunctuation()(hypothesis)
    # ground_truth = jiwer.ReduceToListOfListOfWords()(ground_truth)
    # hypothesis = jiwer.ReduceToListOfListOfWords()(hypothesis)
    ground_truth = jiwer.Strip()(ground_truth)
    hypothesis = jiwer.Strip()(hypothesis)
    ground_truth = jiwer.ToLowerCase()(ground_truth)
    hypothesis = jiwer.ToLowerCase()(hypothesis)
    ground_truth = jiwer.RemoveEmptyStrings()(ground_truth)
    hypothesis = jiwer.RemoveEmptyStrings()(hypothesis)


    print("ASR Transcript from" + asrengine + " = " + hypothesis)
    print("Human Validated Transcript = " + ground_truth)

    wer = jiwer.wer(ground_truth, hypothesis, truth_transform=transformation, hypothesis_transform=transformation)
    mer = jiwer.mer(ground_truth, hypothesis, truth_transform=transformation, hypothesis_transform=transformation)
    wil = jiwer.wil(ground_truth, hypothesis, truth_transform=transformation, hypothesis_transform=transformation)

    return wer,mer,wil,asrengine

def runASREvaluation(testlist):
    for i in testlist:
        filename = str(Path(i).stem)
        print(filename)
        deepspeechResult = str(deepSpeechEvaluation(i))
        PocketSphinxResult = str(PocketSphinxEvaluation(i))
        kaldiResult = str(kaldiEvaluation(i))
        validatedTranscripts = r"../dataset/commonVoice/validatedTranscripts/cV50SampleTranscripts"
        df = pandas.read_csv(validatedTranscripts, index_col=False)
        audiodata = df[df["path"].str.contains(filename)]
        audioDataRow = audiodata['sentence'].head()
        validatedHypothesis = str(audiodata['sentence'].values[0])
        DSWER, DSMER, DSWIL, ASREngine = ASREval(validatedHypothesis,deepspeechResult, "Deepspeech")
        PSWER, PSMER, PSWIL, ASREngine = ASREval(validatedHypothesis, PocketSphinxResult, "PocketSphinx")
        KDWER, KDMER, KDWIL, ASREngine = ASREval(validatedHypothesis, kaldiResult, "Kaldi")

        print("WER DeepSpeech = " + (str(int(DSWER*100)) + "%"))
        print("WER DeepSpeech = " + (str(int(DSWER*100)) + "%"))
        print("WER DeepSpeech = " + (str(int(DSWER*100)) + "%"))
        print()
        print("WER PocketSphinx = " + (str(int(PSWER*100)) + "%"))
        print("WER PocketSphinx = " + (str(int(PSMER*100)) + "%"))
        print("WER PocketSphinx = " + (str(int(PSWIL*100)) + "%"))

        print("WER Kaldi = " + (str(int(KDWER*100)) + "%"))
        print("WER Kaldi = " + (str(int(KDMER*100)) + "%"))
        print("WER Kaldi = " + (str(int(KDWIL*100)) + "%"))




if __name__ == '__main__':
    testlist = extractDatasetAudio()
    runASREvaluation(testlist)