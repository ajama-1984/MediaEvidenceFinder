# Ahmed Jama

import jiwer
from pathlib import Path
import pandas
import shutil, random, os
from moviepy.editor import AudioFileClip
from ASR_S2T_Experiment_DeepSpeech import deepSpeechEvaluation
from ASR_S2T_Experiment_PocketSphinx import PocketSphinxEvaluation
from ASR_S2T_Experiment_Kaldi import kaldiEvaluation
import os
from fractions import Fraction as frac
from pydub import AudioSegment

def random_selection(datasetcsvfile,dirpathDataset,
                     numberOfSamplesinDataset,numberOfSamplesRequired):
    sampleFileListExists = [] # create empty Sample List
    # read all line from file
    n = sum(1 for line in open(datasetcsvfile, encoding="utf8")) - 1
    # generating random numbers to skip when retrieving CSV file
    skip = sorted(random.sample(range(1, n + 1), n -
                                numberOfSamplesinDataset))
    # creating DataFrame and skipping random number of lines
    df = pandas.read_csv(datasetcsvfile, skiprows=skip, sep='\t')
    # retriving just the filename column
    sampleFileList = df["path"].to_list()
    # Setting Counter to finish function when required samples reached
    counter = 0
    # This checks to see if for each sample, the audio files exists
    for x in sampleFileList:
        srcpath = os.path.join(dirpathDataset, x)
        if os.path.exists(srcpath) == True:
            sampleFileListExists.append(x)
            counter = counter + 1
            print(str(counter))
    # Once all files have been verified, a random sample required is selected
    list_of_random_samples_selected = random.sample(
                                    sampleFileListExists,
                                        numberOfSamplesRequired)
    print("Selection Complete! \n")
    print(list_of_random_samples_selected)
    return list_of_random_samples_selected, numberOfSamplesRequired


def sampleRetrieval(sampleFileList):
    directorypath = r'Z:\DissertationSoftwareDev\files\cv-corpus-9.0-2022-04-27\en\clips'
    destDirectoryPath = r'../dataset/commonVoice/clips'
    for fname in sampleFileList:
        sourcePath = os.path.join(directorypath, fname)
        print(sourcePath)
        print(destDirectoryPath)
        shutil.copy(sourcePath, destDirectoryPath)
    print("Complete!")

def retrieveHumanBaseline(list_of_random_samples_selected):
    print("Retrieving Human Validated Transcripts from Mozilla Common Voice Test dataset CSV")
    validated_dataset_transcripts = r"../dataset/commonVoice/tsv/test.tsv"
    datasetdirectory = r"../dataset/commonVoice/clips"
    absolutePath = os.path.abspath(datasetdirectory)
    audiodata_agregat = pandas.DataFrame()
    for file in list_of_random_samples_selected:
        f = os.path.join(absolutePath, file)
        if os.path.isfile(f):
            directory, audiofilename = os.path.split(f)
            df = pandas.read_csv(validated_dataset_transcripts, sep='\t')
            audiodata = df[df["path"] == audiofilename]
            print(audiodata)
            audioDataRow = audiodata.iloc[:,0:3]
            audiodata_agregat = audiodata_agregat.append(audioDataRow, True)

    print(audiodata_agregat)
    audiodata_agregat.to_csv('../dataset/commonVoice/validatedTranscripts/cVSampleTranscripts.csv', index=False)
    print("Human Validated Transcripts Retrieved! \n")

def extractDatasetAudio(list_of_random_samples_selected):
    print("Extracting & Converting media files to 16-bit Mono WAV File for transcription using each ASR Engine")
    datasetdirectory = r"../dataset/commonVoice/clips"
    extractedAudioDirectory = os.path.abspath("../dataset/commonVoice")
    test1 = os.path.abspath(datasetdirectory)
    testlist = []
    for file in list_of_random_samples_selected:
        f = os.path.join(datasetdirectory, file)
        if os.path.isfile(f):
            datasetfilepath = os.path.abspath(f)
            filename = Path(datasetfilepath).stem
            extractedAudioPath = extractedAudioDirectory + "\\extractedAudio\\" + filename + ".wav"
            print("Extracted Audio Path: " + os.path.normpath(extractedAudioPath))
            testlist.append(os.path.normpath(extractedAudioPath))
            audioclip = AudioFileClip(datasetfilepath)
            audioclip.write_audiofile(extractedAudioPath, nbytes=2, codec='pcm_s16le',
                                      ffmpeg_params=["-ac", "1", "-ar", "16000"])
    print("Extraction and Conversion Complete! \n")
    return testlist

def ASREval(ground_truth ,hypothesis, asrengine, transcription_time, sampleAudioLength):
    transformation = jiwer.Compose([
        jiwer.ToLowerCase(),
        jiwer.RemoveWhiteSpace(replace_by_space=True),
        jiwer.RemoveMultipleSpaces(),
        jiwer.ReduceToListOfListOfWords(word_delimiter=" ")
    ])

    ground_truth = jiwer.RemovePunctuation()(ground_truth)
    hypothesis = jiwer.RemovePunctuation()(hypothesis)
    ground_truth = jiwer.Strip()(ground_truth)
    hypothesis = jiwer.Strip()(hypothesis)
    ground_truth = jiwer.ToLowerCase()(ground_truth)
    hypothesis = jiwer.ToLowerCase()(hypothesis)
    ground_truth = jiwer.RemoveEmptyStrings()(ground_truth)
    hypothesis = jiwer.RemoveEmptyStrings()(hypothesis)

    wer = jiwer.wer(ground_truth, hypothesis, truth_transform=transformation, hypothesis_transform=transformation)
    mer = jiwer.mer(ground_truth, hypothesis, truth_transform=transformation, hypothesis_transform=transformation)
    wil = jiwer.wil(ground_truth, hypothesis, truth_transform=transformation, hypothesis_transform=transformation)
    rtf = frac(int(transcription_time), int(sampleAudioLength))
    return wer,mer,wil,asrengine,rtf

def getAudioLength(filename):
    audio = AudioSegment.from_file(filename)
    audioLength = audio.duration_seconds
    print(audioLength)
    return audioLength

def runASREvaluation(testlist, numberOfSamples):
    resultsList = []
    counter = 0
    for i in testlist:
        print(str(counter) + " out of " + str(numberOfSamples) + " samples randomly selected from the Mozilla Common Voice Dataset has been processed!")
        filename = str(Path(i).stem)
        print(filename)
        sampleAudioLength = getAudioLength(i)
        deepspeechResult,deepspeechTranscriptionTime  = deepSpeechEvaluation(i)
        PocketSphinxResult, pocketSphinxTranscriptionTime = PocketSphinxEvaluation(i)
        kaldiResult, kaldiTranscriptionTime = kaldiEvaluation(i)
        validatedTranscripts = r"../dataset/commonVoice/validatedTranscripts/cVSampleTranscripts.csv"
        df = pandas.read_csv(validatedTranscripts, index_col=False)
        try:
            audiodata = df[df["path"].str.contains(filename)]
            # audioDataRow = audiodata['sentence'].head()
            # print(audioDataRow)
            validatedHypothesis = str(audiodata['sentence'].values[0])
            print(validatedHypothesis)
        except:
            continue
        print("Assessing ASR Generated Transcript against Human Validated Transcript")
        DSWER, DSMER, DSWIL, ASREngine, DSrtf = ASREval(validatedHypothesis,deepspeechResult, "Deepspeech", deepspeechTranscriptionTime, sampleAudioLength)
        PSWER, PSMER, PSWIL, ASREngine, PSrtf = ASREval(validatedHypothesis, PocketSphinxResult, "PocketSphinx", pocketSphinxTranscriptionTime, sampleAudioLength)
        KDWER, KDMER, KDWIL, ASREngine, KDrtf = ASREval(validatedHypothesis, kaldiResult, "Kaldi", kaldiTranscriptionTime, sampleAudioLength)

        results = {'filename':filename,'Ground_Truth':validatedHypothesis,'Kaldi_Hypothesis':kaldiResult,'PocketSphinx_Hypothesis':PocketSphinxResult,'DeepSpeech_Hypothesis':deepspeechResult,'Kaldi_WER':KDWER,'Kaldi_MER':KDMER,
                 'Kaldi_WIL':KDWIL,'Kaldi_RTF':KDrtf,'PocketSphinx_WER':PSWER,'PocketSphinx_MER':PSMER,'PocketSphinx_WIL':PSWIL, 'PocketSphinx_RTF':PSrtf,'DeepSpeech_WER':DSWER,'DeepSpeech_MER':DSMER,'DeepSpeech_WIL':DSWIL, 'eepSpeech_RTF':DSrtf}

        resultsList.append(results)
        counter = counter + 1

    resultsdf2 = pandas.DataFrame(resultsList)
    resultsdf2.to_csv('../dataset/commonVoice/validatedTranscripts/results.csv', index=False)

if __name__ == '__main__':
    datasetcsvfile = r"../dataset/commonVoice/tsv/test.tsv"
    dirpathDataset = r'Z:\DissertationSoftwareDev\files\cv-corpus-9.0-2022-04-27\en\clips'
    numberOfSamplesinDataset = 5
    numberOfSamplesRequired = 1

    sampleFileList, numberOfSamples = random_selection(datasetcsvfile,dirpathDataset,
                     numberOfSamplesinDataset,numberOfSamplesRequired)
    sampleRetrieval(sampleFileList)
    retrieveHumanBaseline(sampleFileList)
    testlist = extractDatasetAudio(sampleFileList)
    runASREvaluation(testlist, numberOfSamples)