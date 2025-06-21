import os
import subprocess
import sys

def print_color(text, color):
    """Print colored text."""
    colors = {
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'blue': '\033[94m',
        'reset': '\033[0m'
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")

def check_tts():
    """Check if TTS can be imported correctly."""
    print_color("Checking TTS installation...", "blue")
    try:
        from TTS.api import TTS
        print_color("✅ TTS is correctly installed!", "green")
        return True
    except ImportError as e:
        print_color(f"❌ TTS import error: {str(e)}", "red")
        return False

def setup():
    """Set up the application environment."""
    print_color("🎙️ Setting up Local-TTS-Runner", "green")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print_color(f"✅ Created output directory at {output_dir}", "green")
    
    # Ensure models_data directory exists for backwards compatibility
    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models_data")
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    
    # Handle old TTS directory conflicts
    old_tts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TTS")
    if os.path.exists(old_tts_dir):
        print_color("⚠️ Found old TTS directory that may cause conflicts with Python package", "yellow")
        print_color("⚠️ Consider removing the old TTS directory to prevent import conflicts", "yellow")
    
    # Check and install TTS if needed
    if not check_tts():
        print_color("Installing TTS...", "yellow")
        try:
            # Try to uninstall first if it exists but has issues
            try:
                subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "TTS"], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except:
                pass
                
            subprocess.run([sys.executable, "-m", "pip", "install", "TTS==0.17.0"], check=True)
            if check_tts():
                print_color("✅ TTS installed successfully!", "green")
            else:
                print_color("❌ TTS installation failed. Try installing manually:", "red")
                print_color("pip install TTS==0.17.0", "yellow")
        except Exception as e:
            print_color(f"❌ Error installing TTS: {str(e)}", "red")
    
    # Create .env file from template if needed
    if not os.path.exists(".env") and os.path.exists(".env.example"):
        with open(".env.example", "r") as src:
            with open(".env", "w") as dst:
                dst.write(src.read())
        print_color("✅ Created .env file from .env.example", "green")
    
    print_color("\n🚀 Setup complete! Run the application with:", "green")
    print_color("python app.py", "blue")

if __name__ == "__main__":
    setup()
