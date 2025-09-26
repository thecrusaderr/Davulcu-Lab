# README

**scaling_participants.ipynb:** Jupyter notebook for scaling analysis of participants. Takes combined transcripts, applies a Masked ABSA model (from [this paper](https://imyday.github.io/pub/asonam2024/pdf/papers/1219_001.pdf)) to extract stances toward selected keywords, then uses ANCO-HITS co-scaling to position participants along a scale.  
- **Input:** Excel file containing all participants’ transcriptions.  
- **Output:** Scaled participant scores for analysis or visualization.  

**transcription_diarization.py:** Script for audio transcription with speaker diarization. Converts `.m4a` to `.wav`, separates speaker segments using `pyannote.audio`, and transcribes each segment with OpenAI Whisper.  
- **Input:** `.m4a` audio files.  
- **Output:** JSON files with speaker labels, timestamps, and transcribed text.  

**Participant.ipynb:** Jupyter notebook to get stances of participants for different claims/statements.  
- **Input:** PDF file containing single participant transcription.  
- **Output:** CSV file with explanation and stance(Support/Oppose/No Evidence Found) for claims.  
