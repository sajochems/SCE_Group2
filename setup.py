from setuptools import find_packages, setup

# Basic (bare minimum) requirements for local machine
requirements = [
    "numpy",
    "opencv-python",
    "paramiko",
    "Pillow",
    "pyaudio",
    "PyTurboJPEG",
    "pyspacemouse",
    "redis",
    "scp",
    "six",
]

# Dependencies specific to each component or server
extras_require = {
    "dialogflow": [
        "google-cloud-dialogflow",
    ],
    "face-detection-dnn": [
        "matplotlib",
        "pandas",
        "pyyaml",
        "torch",
        "torchvision",
        "tqdm",
    ],
    "face-recognition": [
        "scikit-learn",
        "torch",
        "torchvision",
    ],
    "dev": [
        "pre-commit==4.0.1",
        "isort==5.13.2",
        "black==24.10.0",
    ],
}

setup(
    name="social-interaction-cloud",
    version="2.0.13",
    author="Koen Hindriks",
    author_email="k.v.hindriks@vu.nl",
    packages=find_packages(),
    package_data={
        "sic_framework.services.face_detection": [
            "haarcascade_frontalface_default.xml",
        ],
        "lib.libturbojpeg.lib32": [
            "libturbojpeg.so.0",
        ],
    },
    install_requires=requirements,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "run-dialogflow=sic_framework.services.dialogflow:main",
            "run-face-detection=sic_framework.services.face_detection:main",
            "run-face-recognition=sic_framework.services.face_recognition_dnn:main",
        ],
    },
)
