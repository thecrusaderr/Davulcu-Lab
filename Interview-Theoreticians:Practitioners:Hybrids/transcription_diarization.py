from pyannote.audio import Pipeline
from pydub import AudioSegment
import os
import torch
import whisper
import ffmpeg
import json

torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

def convert_m4a_to_wav(input_path, output_path, ffmpeg_path="<provide ffmpeg_path>"):
    try:
        os.environ["PATH"] = f"{os.path.dirname(ffmpeg_path)}:{os.environ['PATH']}"
        
        print(f"Using FFmpeg from: {ffmpeg_path}")
        print(f"Converting {input_path} to {output_path}...")
        
        (
            ffmpeg
            .input(input_path)
            .output(output_path, format="wav")
            .run(overwrite_output=True)
        )
        
        print(f"Conversion completed: {output_path}")
    except ffmpeg.Error as e:
        print(f"Error during conversion: {e.stderr.decode()}")

def diarize_and_combine_speakers(input_audio_path, output_dir, use_gpu=True):

    device = torch.device("cuda:3" if use_gpu and torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    wav_audio = '<wav_audio_path>/audio.wav'
    convert_m4a_to_wav(input_audio_path, wav_audio) 

    print("Loading pre-trained speaker diarization pipeline...")
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token="<hg_auth_token>")
    pipeline.to(device)
    
    input_audio_path = wav_audio

    print("Performing speaker diarization...")
    diarization = pipeline(input_audio_path)

    print("Loading audio file for processing...")
    audio = AudioSegment.from_file(input_audio_path)

    os.makedirs(output_dir, exist_ok=True)

    model = whisper.load_model("medium",device=device)

    print("Processing speaker segments...")
    transcribe = []
    for segment, _, speaker in diarization.itertracks(yield_label=True):
        start_time = int(segment.start * 1000) 
        end_time = int(segment.end * 1000)

        speaker_audio = audio[start_time:end_time]
        
        temp = '<temp path>/temp.wav'
        speaker_audio.export(temp, format="wav")
        result = model.transcribe(temp, language="en")
        os.remove(temp)

        start_time_seconds = segment.start
        end_time_seconds = segment.end
        print(f"Speaker {speaker}: {start_time_seconds:.2f}s to {end_time_seconds:.2f}s transcript: {result['text']}")
        data ={
            "frame_number": 0,
            "speaker": f"{speaker}",
            "timestamp": f'{start_time_seconds:.2f}', # in seconds
            "length": f'{(end_time_seconds-start_time_seconds):.2f}', # in seconds
            "value": f"{result['text']}"
        }
        transcribe.append(data)
        
    base_name = os.path.basename(file_path)
    file_name_without_extension = os.path.splitext(base_name)[0]
        
    with open(f"{output_dir}/{file_name_without_extension}.json", "w") as f:
        json.dump(transcribe, f)
    os.remove(wav_audio)


for root, _, files in os.walk('<provide audio files path>'):
    for file in files:
        if file.endswith('.m4a'):
            file_path = os.path.join(root, file)
            diarize_and_combine_speakers(file_path, "<output path>", use_gpu=True)
