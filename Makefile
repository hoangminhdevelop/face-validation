.PHONY: setup clean test run install

# Set up development environment
setup:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

# Install in development mode
install:
	. venv/bin/activate && pip install -e .

# Run the application
run:
	. venv/bin/activate && python app.py

# Clean up build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run tests (when you add them)
test:
	. venv/bin/activate && python -m unittest discover