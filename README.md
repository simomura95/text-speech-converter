# Text speech converter
GUI app to convert text into audio file and vice versa. Requires ffmpeg installed and added to PATH environment variable.

3 types of conversion are supported:

**1. Text to speech (.pdf, .doc or .txt file to .mp3)** <br>
The file is read and converted to plain text (with PyPDF2 package if a .pdf file), then it is converted to .mp3 with gtts (Google text-to-speech) package.

**2. input to speech (a .mp3 file is created from user input)** <br>
A temporary file is created from the textbox and then converted as described above. The temporary file is deleted after finishing.

**3. speech to text (.mp3 to .doc file)** <br>
The .mp3 file is first converted into a temporary .wav with the function AudioSegment of the Pydub package (which requires ffmpeg installed).
Then it is used as source for conversion into plain text with the Speech recognition package and written into a .doc file.

Although the code is functioning correctly, I found the accuracy of the results pretty poor, especially going from audio to text.
I think i's because of the package used; probably using an API or an AI service it could be greatly improved, but that goes beyond this project.
