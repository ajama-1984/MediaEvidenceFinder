import setuptools
from setuptools import setup

setup(
    name='SpeechTranscription',
    version='0.0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/ajama-1984/SpeechTranscription',
    license='Apache 2.0',
    author='Ahmed Jama',
    author_email='ahmed.jama@warwick.ac.uk',
    description='Transcription Tool to transcribe and find keywords on Audio-based evidence',

    install_requires=["moviepy==1.0.3"
                    "pocketsphinx>=0.1.15"
                    "vosk==0.3.42"
                    "future~=0.18.2"
                    "self~=2020.12.3"
                    "ffmpeg~=1.4"
                    "hachoir~=3.1.3"
                    "setuptools==62.6.0"
                    "yaspin~=2.1.0"
                    "pydub~=0.25.1"
                    "jiwer~=2.3.0"
                    "pandas~=1.4.3"
                    "deepspeech~=0.9.3"
                    "numpy~=1.22.3"
                    "librosa~=0.9.2"]
)
