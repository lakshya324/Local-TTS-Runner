# Local-TTS-Runner

A lightweight, easy-to-use interface for running Coqui TTS models locally. This project enables offline text-to-speech generation using Coqui TTS, with support for model selection, voice customization, and runs fully offline. Ideal for developers, hobbyists, and anyone needing private, local speech synthesis.

## Features

- 100% offline text-to-speech synthesis
- Gradio-based web interface
- Support for various Coqui TTS models
- Adjustable speech parameters (speed, speaker ID)
- Audio playback and download options
- Direct model loading from TTS library

## Requirements

- Python 3.8 or higher
- Sufficient disk space for TTS models (varies by model)
- Internet connection for initial model download only

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/Local-TTS-Runner.git
   cd Local-TTS-Runner
   ```

2. Create a virtual environment (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment configuration:

   ```bash
   cp .env.example .env
   # Edit .env file as needed with your preferred settings
   ```

## Usage

1. Start the application:

   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:7860` (or the URL displayed in the terminal).

3. Enter text, select a model, adjust settings if desired, and click "Generate Speech".

4. The first time you use a specific model, it will be downloaded automatically (requires internet connection).

5. After the initial download, the application works completely offline.

6. All generated audio is saved to the `output` directory (or the directory specified in `OUTPUT_DIR`).

## Output Files

All generated audio files are automatically saved to the `output` directory (configurable via the `OUTPUT_DIR` environment variable). Files are saved using the following naming convention:

```text
YYYYMMDD_HHMMSS_first_few_words_of_text.wav
```

For example: `20230515_142322_hello_world.wav`

This makes it easy to organize and find your generated audio files for later use.

## Models

By default, the application uses `tts_models/en/ljspeech/tacotron2-DDC`, but you can select from various English TTS models available in the Coqui TTS model library.

Different models have different characteristics:

- Some models support multiple speakers
- Quality and generation speed vary by model
- Some advanced models support emotional speech

The application uses Coqui TTS's built-in model loading system, so all models available in the TTS library can be used directly without any additional configuration.

## Environment Configuration

The application can be configured using environment variables through a `.env` file. A template file `.env.example` is provided - copy it to `.env` to use:

```bash
cp .env.example .env
```

Available environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `GRADIO_SERVER_PORT` | Web server port | `7860` |
| `GRADIO_SERVER_NAME` | Server hostname/IP | `0.0.0.0` |
| `ENABLE_SHARING` | Enable temporary public URL | `false` |
| `OPEN_BROWSER` | Auto-open browser at startup | `true` |
| `DEFAULT_MODEL` | Initial TTS model to load | `tts_models/en/ljspeech/tacotron2-DDC` |
| `DEBUG` | Enable verbose logging | `false` |
| `MAX_TEXT_LENGTH` | Maximum characters to process | `500` |
| `MODELS_CACHE_DIR` | Custom cache for downloaded models | (empty) |
| `OUTPUT_DIR` | Directory to save generated audio files | `output` |
| `LOG_LEVEL` | Logging verbosity level | `INFO` |
| `LOG_FILE` | Path to save logs (console only if empty) | (empty) |

## Troubleshooting

- If you encounter CUDA/GPU errors, the application will automatically fall back to CPU.
- For very long text inputs, consider breaking them into smaller paragraphs.
- If a model fails to load, try another model from the dropdown list.

### TTS Version Compatibility

This application is designed to work with Coqui TTS version 0.17.0. If you encounter errors related to TTS imports or API incompatibilities:

1. Ensure you're using the exact version specified in requirements.txt:

   ```bash
   pip install TTS==0.17.0
   ```

2. If you see error messages about models not loading correctly, run the setup script to check your installation:

   ```bash
   python setup.py
   ```

3. If using a virtual environment (recommended), make sure it's activated before running the app:

   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

## Logging

The application includes a comprehensive colored logging system that helps track operations and diagnose issues:

- **Color-coded messages**: Different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) are displayed in distinct colors
- **Contextual information**: Logs include relevant context for easier troubleshooting
- **File and console output**: Logs can be sent to a file, console, or both
- **Configurable verbosity**: Control log detail level via environment variables

To configure logging:

1. Set `LOG_LEVEL` in your `.env` file to one of:
   - `DEBUG` (most verbose)
   - `INFO` (default)
   - `WARNING`
   - `ERROR`
   - `CRITICAL` (least verbose)

2. Optionally set `LOG_FILE` to a file path to save logs to disk

Example for detailed logging:

```env
LOG_LEVEL=DEBUG
LOG_FILE=local_tts_runner.log
```

## License

See the [LICENSE](LICENSE) file for more information.
