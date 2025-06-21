import os
import sys
import traceback
import datetime
import re
import gradio as gr
import numpy as np
import torch
from dotenv import load_dotenv
from pathlib import Path
from TTS.api import TTS
from logger import debug, info, warning, error, critical

# Load environment variables
load_dotenv()

# Application constants
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "tts_models/en/ljspeech/tacotron2-DDC")
MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", "500"))
MODELS_CACHE_DIR = os.getenv("MODELS_CACHE_DIR", "")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Configure TTS cache directory if specified
if MODELS_CACHE_DIR:
    os.environ["TTS_HOME"] = MODELS_CACHE_DIR

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)





def list_available_models():
    """Get list of available English TTS models."""
    try:
        all_models = TTS().list_models()
        models = [model for model in all_models if isinstance(model, str) 
                  and model.startswith("tts_models/en")]
        
        info(f"Found {len(models)} English TTS models")
        return models
    except Exception as e:
        error(f"Failed to list models: {str(e)}")
        if DEBUG:
            error(traceback.format_exc())
        return [DEFAULT_MODEL]


def get_speaker_ids(model_name):
    """Get available speaker IDs for multi-speaker models."""
    try:
        temp_tts = TTS(model_name=model_name)
        
        if hasattr(temp_tts, 'is_multi_speaker') and temp_tts.is_multi_speaker:
            speaker_ids = list(range(len(temp_tts.speakers)))
            debug(f"Model {model_name} has {len(speaker_ids)} speakers")
            return speaker_ids
        
        return []
    except Exception as e:
        warning(f"Could not get speakers for model {model_name}: {str(e)}")
        return []


def load_tts_model(model_name):
    """Load a TTS model with GPU acceleration if available."""
    try:
        info(f"Loading TTS model: {model_name}")
        
        use_cuda = torch.cuda.is_available()
        device_info = {"device": "CUDA" if use_cuda else "CPU"}
        debug("Initializing model", device_info)
        
        tts_model = TTS(model_name=model_name, gpu=use_cuda)
        
        info(f"Model {model_name} loaded successfully", device_info)
        return tts_model
    except Exception as e:
        error(f"Failed to load model {model_name}: {str(e)}")
        if DEBUG:
            error(traceback.format_exc())
        raise


def text_to_speech(text, model_name, speaker_id=None, speed=1.0):
    """Convert text to speech using selected model and save to output directory."""
    if not text or text.isspace():
        warning("Empty text input received")
        return None, "Please enter some text to convert to speech."
    
    if len(text) > MAX_TEXT_LENGTH:
        warning(f"Text exceeds maximum length: {len(text)}/{MAX_TEXT_LENGTH} characters")
        return None, f"Text is too long. Maximum length is {MAX_TEXT_LENGTH} characters."
    
    try:
        context = {
            "model": model_name,
            "speaker_id": speaker_id,
            "speed": speed,
            "text_len": len(text)
        }
        info("Starting text-to-speech conversion", context)
            
        tts_model = load_tts_model(model_name)
        
        speaker_id = int(speaker_id) if speaker_id is not None else None
        debug(f"Converting text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        # Generate filename from text content and timestamp
        safe_text = re.sub(r'\W+', '_', text.strip()[:30]).strip('_')
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{timestamp}_{safe_text}.wav"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Generate speech and save to file
        if hasattr(tts_model, 'is_multi_speaker') and tts_model.is_multi_speaker and speaker_id is not None:
            speaker_name = tts_model.speakers[speaker_id]
            tts_model.tts_to_file(
                text=text,
                speaker=speaker_name,
                speed=speed,
                file_path=output_path
            )
        else:
            tts_model.tts_to_file(
                text=text,
                speed=speed,
                file_path=output_path
            )
        
        info("Speech generated successfully", {"output_file": output_path})
        return output_path, f"Speech generated successfully. Saved to {output_filename}"
    except Exception as e:
        error_msg = str(e)
        error_context = {"model": model_name, "error_type": type(e).__name__}
        error(f"Failed to generate speech: {error_msg}", error_context)
        
        if DEBUG:
            error(traceback.format_exc())
            
        return None, f"Error generating speech: {error_msg}"


def create_ui():
    """Create Gradio UI for TTS application."""
    models = list_available_models()
    default_model = DEFAULT_MODEL if DEFAULT_MODEL in models else models[0]
    
    with gr.Blocks(title="Local TTS Runner") as app:
        # Header and instructions
        gr.Markdown("# 🎙️ Local TTS Runner")
        gr.Markdown(
            f"""
            Convert text to speech using locally running Coqui TTS models.
            
            ### Instructions:
            1. Enter the text you want to convert to speech
            2. Select a TTS model (will be downloaded on first use)
            3. Adjust optional settings if available for the selected model
            4. Click 'Generate Speech' and wait for the audio to be produced
            5. Play the audio directly or download it
            
            All processing happens locally on your machine - no data is sent to external servers.
            
            All generated audio is saved to the `{OUTPUT_DIR}` folder.
            """
        )
        
        # Main interface
        with gr.Row():
            # Input column
            with gr.Column():
                text_input = gr.Textbox(
                    label="Text to convert to speech",
                    placeholder="Enter text here...",
                    lines=5
                )
                
                model_selector = gr.Dropdown(
                    label="TTS Model",
                    choices=models,
                    value=default_model
                )
                
                with gr.Group():
                    speaker_selector = gr.Number(
                        label="Speaker ID (only for multi-speaker models)",
                        value=None,
                        precision=0,
                        visible=True
                    )
                    
                    speed_slider = gr.Slider(
                        label="Speed",
                        minimum=0.5,
                        maximum=1.5,
                        value=1.0,
                        step=0.1
                    )
                
                generate_btn = gr.Button("Generate Speech", variant="primary")
            
            # Output column
            with gr.Column():
                output_audio = gr.Audio(label="Generated Speech")
                output_message = gr.Textbox(label="Status")
        
        # Event handlers
        def update_speaker_visibility(model_name):
            speaker_ids = get_speaker_ids(model_name)
            return {speaker_selector: gr.update(visible=len(speaker_ids) > 0)}
        
        generate_btn.click(
            fn=text_to_speech,
            inputs=[text_input, model_selector, speaker_selector, speed_slider],
            outputs=[output_audio, output_message]
        )
        
        model_selector.change(
            fn=update_speaker_visibility,
            inputs=[model_selector],
            outputs=[speaker_selector]
        )
        
    return app


if __name__ == "__main__":
    # Server configuration from environment
    server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    server_name = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    enable_sharing = os.getenv("ENABLE_SHARING", "false").lower() == "true"
    open_browser = os.getenv("OPEN_BROWSER", "true").lower() == "true"
    
    # Log startup information
    server_context = {
        "server_name": server_name,
        "server_port": server_port,
        "sharing_enabled": enable_sharing,
        "auto_open_browser": open_browser,
        "python_version": sys.version.split()[0]
    }
    info("Starting Local TTS Runner", server_context)
    
    # Debug information
    if DEBUG:
        debug(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            debug(f"CUDA device: {torch.cuda.get_device_name(0)}")
        if MODELS_CACHE_DIR:
            debug(f"Using custom models cache directory: {MODELS_CACHE_DIR}")
    
    try:
        info("Initializing Gradio web interface")
        app = create_ui()
        info(f"Launching web server at http://{server_name}:{server_port}")
        app.launch(
            server_name=server_name, 
            server_port=server_port, 
            share=enable_sharing, 
            inbrowser=open_browser
        )
    except Exception as e:
        critical(f"Failed to start application: {str(e)}")
        if DEBUG:
            critical(traceback.format_exc())
        sys.exit(1)
