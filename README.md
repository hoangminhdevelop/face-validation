# Face Validation API

A simple REST API for face validation using Python, Flask, and OpenCV.

## Features

- Validates images containing human faces
- Ensures exactly one face is present in the image
- Rejects blurry images
- Rejects cartoon/fake faces
- Supports JPG and PNG image formats

## Requirements

- Python 3.x
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hoangminhdevelop/face-validation.git
cd face-validation
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python app.py
```

2. The API will be available at http://localhost:5000

3. To validate a face, send a POST request to `/validate-face` with an image file:
```bash
curl -X POST -F "image=@/path/to/your/image.jpg" http://localhost:5000/validate-face
```

## API Response

The API returns a JSON response with the validation result:

- Valid face:
```json
{
  "valid": true,
  "message": "Valid human face detected"
}
```

- Invalid face:
```json
{
  "valid": false,
  "reason": "Expected 1 face, found 0"
}
```

## License

MIT