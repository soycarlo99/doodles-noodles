# Doodles Noodles

Doodles Noodles is a playful machine learning project that combines deep learning and classical ML approaches to recognize doodles of **crabs 🦀** and **fish 🐟** from the [Google QuickDraw Dataset](https://console.cloud.google.com/storage/browser/quickdraw_dataset/full/numpy_bitmap;tab=objects?prefix=&forceOnObjectsSortingFiltering=false).  
It also features a real-time interactive web app where users can draw their creatures and watch them come alive on the dance floor.

---

## Features

- **Dataset**: Uses QuickDraw `.npy` bitmap drawings of crabs and fish.
- **Models**:
  - Convolutional Neural Network (CNN) built with TensorFlow/Keras.
  - Classical ML models (Logistic Regression, Random Forest, Extra Trees, SVM, and a Voting Classifier) built with scikit-learn.
- **Web App**:
  - Built with Flask + Flask-SocketIO.
  - Users can doodle crabs or fish in a canvas.
  - Predictions are made with the trained model, and creatures are animated in a fun "rave" environment with background music.
- **Visualization**:
  - Training history plots (loss/accuracy).
  - Confusion matrix and classification reports for classical models.

---

## visit [doodle noodle](https://doodlenoodle.echowords.xyz/)

## Dataset Setup

The dataset comes from the [Google QuickDraw project](https://quickdraw.withgoogle.com/).  
To download the classes used here:

```bash
# Using wget
wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/crab.npy -O crab.npy
wget https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/fish.npy -O fish.npy

# On macOS / Unix with curl
curl -o crab.npy https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/crab.npy
curl -o fish.npy https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/fish.npy
```

Place the `.npy` files into a folder named `quickdraw_simplified/`.

---

## Credits

- **Dataset**: [Google QuickDraw](https://quickdraw.withgoogle.com/).
- **Music**: [Crab Rave by Noisestorm](https://www.monstercat.com/release/MCS447).
- **Frameworks**: TensorFlow, Keras, scikit-learn, Flask, Flask-SocketIO.

---

## License

This project is for **educational and fun purposes**.
