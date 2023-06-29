from gtts import gTTS  # uses google services for text-to-speech
from PyPDF2 import PdfReader  # to work with pdf
from customtkinter import *
import speech_recognition as sr  # to convert wav into text, using google services
from pydub import AudioSegment  # support package to work with audio segment (here used to convert mp3 into wav)
import os

# AudioSegment.converter = "C:/ffmpeg/bin"  # not needed if ffmpeg path is added to environment variable PATH

# app to convert:
# - a text file (.pdf, .doc, .txt or from user input) to .mp3 file (text to speech)
# - a .mp3 file to .doc file (speech to text).
# Text-to-speech result seems to be pretty good, while speech-to-text not so much. Both use google services utilities


# --------------------- CTK CLASS with all needed functions -------------------------
class TextSpeech(CTk):
    def __init__(self):
        super().__init__()
        self.title('Text to speech app')  # master window
        self.config(padx=30, pady=30)
        self.start_path = None
        self.end_path = None
        self.text = ''

        self.text_to_speech = CTkButton(self, text="File to mp3", command=self.file_to_text)
        self.text_to_speech.grid(row=0, column=0)

        self.speech_to_text = CTkButton(self, text="Mp3 to file", command=self.mp3_to_file)
        self.speech_to_text.grid(row=0, column=1)

        self.label_bt1 = CTkLabel(master=self, text='Supported files: .txt, .doc, .pdf')
        self.label_bt1.grid(row=1, column=0)

        self.label_bt2 = CTkLabel(master=self, text='Output file format: .doc')
        self.label_bt2.grid(row=1, column=1)

        self.label_text = CTkLabel(master=self, text='or type text to convert to mp3 below:')
        self.label_text.grid(row=2, column=0, columnspan=2, pady=(30, 0))

        self.textbox = CTkTextbox(master=self, width=600, height=200, wrap=WORD)
        self.textbox.grid(row=3, column=0, columnspan=2)

        self.input_to_speech = CTkButton(self, text="Convert text", command=self.input_to_text)
        self.input_to_speech.grid(row=4, column=0, columnspan=2, pady=(10, 0))

    def file_to_text(self):
        """Acquire a txt, doc or pdf file and convert it to plain text"""
        self.start_path = filedialog.askopenfilename(filetypes=[('File', '*.txt'), ('File', '*.doc'), ('File', '*.pdf')])
        # print(self.start_path)
        if self.start_path[-4:] == ".pdf":  # if pdf file
            reader = PdfReader(self.start_path)
            self.text = "".join([reader.pages[p].extract_text(0) for p in range(len(reader.pages))]).replace('\n', '')
        else:  # if doc or txt file
            with open(self.start_path, encoding="utf8") as file:
                self.text = file.read()
        # print(self.text)
        self.text_to_mp3()

    def mp3_to_file(self):
        """Acquire a mp3 file and converts it into a wav file, which then is used for generating plaint text and the resulting .doc file.
        Conversion uses google services, but quality seems to be pretty low"""
        self.start_path = filedialog.askopenfilename(filetypes=[('File', '*.mp3')])
        print(self.start_path)

        # convert mp3 file to wav
        sound = AudioSegment.from_mp3(self.start_path)
        path_wav = f"{self.start_path[:-4]}.wav"
        sound.export(path_wav, format="wav")
        file_audio = sr.AudioFile(path_wav)

        # use the wav file as the audio source
        r = sr.Recognizer()
        with file_audio as source:
            audio_text = r.record(source)
        self.text = r.recognize_google(audio_text)
        os.remove(path_wav)  # remove the temporary wav file

        # save file
        self.end_path = f"{self.start_path[:-4]}.doc"
        with open(self.end_path, 'w') as output_file:
            output_file.write(self.text)

    def input_to_text(self):
        """Get input from user"""
        self.text = self.textbox.get(1.0, "end-1c")
        self.start_path = "app_output.doc"
        with open(self.start_path, "w") as text_file:
            text_file.write(self.text)
        self.text_to_mp3()

    def text_to_mp3(self):
        """Convert text into mp3. Uses Google text-to-speech (gTTS) service"""
        my_tts = gTTS(text=self.text, lang='en', slow=False)
        self.end_path = f"{self.start_path[:-4]}.mp3"
        # print(self.end_path)
        my_tts.save(self.end_path)

    def finish(self):
        """After conversion, open resulting file and close GUI"""
        os.system(self.end_path)
        self.destroy()


# --------------------------------- MAIN PROGRAM: create master window and the first frame -----------------------
root = TextSpeech()

root.mainloop()
