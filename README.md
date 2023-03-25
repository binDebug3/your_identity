<a name="readme-top"></a>

<div align="center">
    <h1 align="center">Your Identity</h1>
    <p align="center">
        A face detection algorithm that uses the webcam to detect faces and 
        tell you about your identity.
    </p>
</div>

<hr>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#welcome">Welcome</a></li>
    <li><a href="#description">Description</a></li>
    <li><a href="#instructions">Instructions for Download</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


<!-- Welcome -->
## Welcome

This project was built Benj the master, Jeff the Chef, and Dallin the one that carries the team 
for the <a href='https://acm.byu.edu/'>2023 YHack</a> at BYU over the course of 24 hours. This project uses OpenCV to detect faces, 
compare them to a database of faces of celebrities, estimate your age and gender, and then tell
a story about you and your celebrity twin.

<hr>

### Description
The program starts by introducing itself and asking you to say your name. It then uses the webcam 
to take a picture of your face and compares it to a database of celebrity faces. We used selenium 
to scrape the faces of celebrities the top 1000 actors in Hollywood from IMDB. We had to center 
the faces of each of the celebrities in order to construct a database with a high quality mean 
eigenface. We then use the eigenfaces SVD technique to find the closest actor to the image captured 
from the webcam. The program then uses a text to speech engine to tell you about your celebrity 
lookalike, and estimate your age and gender. It predicts age and gender by using a pre-trained 
models from openCV. The program then uses the openAI GPT-3 API to generate a story about you and then 
say good bye.

### Instructions for Download
You'll need to start by downloading a few python packages with these commands:
```
pip install opencv
pip install numpy
pip install face_recognition
pip install selenium
pip install tkinter
pip install openai
pip install urllib
pip install pyttsx3
pip install pyaudio
pip install speech_recognition
pip install matplotlib
pip install scipy
pip install imageio
```

<!-- CONTACT -->
## Contact

Dallin Stewart - dallinpstewart@gmail.com

Jeff Hansen - jeffxhansen@gmail.com

Benj McMullin