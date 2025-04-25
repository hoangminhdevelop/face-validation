from setuptools import setup, find_packages

setup(
    name="face_validation",
    version="0.1.0",
    description="A REST API for face validation",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "flask==3.1.0",
        "opencv-python==4.11.0.86",
        "numpy==2.2.5",
        "pillow==11.2.1",
    ],
    python_requires=">=3.6",
)