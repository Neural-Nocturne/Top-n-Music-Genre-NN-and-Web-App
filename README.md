# Top-n Music Genre Classification Neural Network and Web App

---
## Getting Started
This application is an Multi Layered Perceptron (MLP) which can classify music audio files into 10 different musical genres with 93% accuracy on the GTZAN dataset. How well will it do for you? This application can also extract music from Youtube video links and also run that through its model for classification. front_end.py is where the main program is run from. Initial setup of the program can take time as downloading machine learning dependencies can be cumbersome, as well as initializing the saved neural network parameters to make predictions. There may be significant delays on the first request made to the app as a result. Afterward there should be very small 4-5 second delays with each prediction made.

## Installation
Be sure to run in a virtual environment and install dependencies from requirements.txt. As of this writing 8/17/24 the package pytubefix is presently functional in pulling audio from YouTube videos for processing. It is likely that if this package is not maintained that this functionality will be lost, as similarly happened with this packages predecessor, pytube. In order to solve SSL requirements when sending HTTP requests, pytubefix.cli is used. 

## SSL Errors
If SSL Errors are still occuring with requests made with Youtube.com links submitted to the app, this can be remedied by running the following terminal commands on linux:

```
CERT_PATH=$(python -m certifi)
export SSL_CERT_FILE=${CERT_PATH}
export REQUESTS_CA_BUNDLE=${CERT_PATH}
```

This uses the package certifi to download the Mozilla's carefully curated certificates so that packages like requests can run smoothly without SSL issues.

---
## Authors

- Elvin Carmona
- Mark Jordan
    - GitHub: [@markyjordan](https://github.com/markyjordan)
    - LinkedIn: [in/markyjordan/](https://www.linkedin.com/in/markyjordan/)
- Michael Levins
    - GitHub: [@mclevins](https://github.com/mclevins)
    - LinkedIn: [in/michaelclevins](https://www.linkedin.com/in/michaelclevins/)

---

<br>

[Return to the Top](#top-n-music-genre-classification-neural-network-and-web-app)
