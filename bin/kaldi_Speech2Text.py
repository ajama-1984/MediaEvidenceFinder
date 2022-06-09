from vosk import Model, KaldiRecognizer
import wave
import json
import os
from tqdm.notebook import tqdm
wav_file = r"C:\Users\Ahmed\Documents\Audio Evidence\test.wav"

wf = wave.open(wav_file, "rb")
model = Model(r"C:\Users\Ahmed\PycharmProjects\SpeechTranscription\models\Kaldi")
recogniser  = KaldiRecognizer(model,16000)
file_size = os.path.getsize(wav_file)

pbar = tqdm(total=file_size)
rec = KaldiRecognizer(model, wf.getframerate())

transcription = []

while True:
    data = wf.readframes(4000)
    pbar.update(len(data)) # PROGRESS BAR NOT WORKING - IN TO-DO LIST
    if len(data) == 0:
        pbar.set_description("Transcription finished")
        break
    if rec.AcceptWaveform(data):
        # Convert json output to dict
        result_dict = json.loads(rec.Result())
        print (result_dict)
        # Extract text values and append them to transcription list
        transcription.append(result_dict.get("text", ""))
        print (transcription)

# Get final bits of audio and flush the pipeline
final_result = json.loads(rec.FinalResult())
transcription.append(final_result.get("text", ""))

# merge or join all list elements to one big string
transcription_text = ' '.join(transcription)
print(transcription_text)

