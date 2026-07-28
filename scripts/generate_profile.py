import cv2
import numpy as np
from rembg import remove
import os

# --- 1. CONFIGURATION & DATA ---
# Dark mode ramp: Dark/empty areas map to spaces, bright highlights map to dense blocks
ASCII_CHARS = [" ", ".", ":", "-", "=", "+", "*", "%", "@", "#"]
IMAGE_PATH = r"C:\Users\super\OneDrive\Pictures\Screenshots 1\Screenshot 2026-07-27 143529.png"
OUTPUT_DIR = "data"
FRAME_COUNT = 5

BIO_MARKDOWN = """# Devansh Ruia

**CS at Northeastern.** I do mechanistic interpretability, which is the practice of explaining how neural networks work using, among other things, the same neural networks that won't explain themselves.

### What I'm Working On Now
* **Function Vectors to Tool Selection:** Extending Todd et al.'s work. I isolated a vector that makes GPT-J act like it read the instructions, then watched it stop transferring the moment I changed model families. *The place it breaks is the interesting part.*
* **Blackout Markets:** A shadow-mode cost and carbon optimizer for GPU clouds. It hands operators recommendations they are completely free to ignore. Whether they ignore them is, itself, data.
* **Sparse Autoencoders:** Next up, on the theory that one unsolved problem was leaving me with too much free time.

### Previously
* Reproduced function vectors on GPT-J with `nnsight` and Hugging Face transformers. It worked on the first clean run, which I found suspicious enough to check twice.
* Took Blackout Markets from an empty repo to 62 passing tests. I mention the number knowing it will not survive contact with the next feature.

### The Stack
* **Research:** Python, PyTorch, `nnsight`, Hugging Face transformers, GPT-J when it feels like cooperating.
* **Product:** TypeScript, Express, React, Vite, shipped on Vercel. *Determinism is a house rule, not a suggestion.*

### Highlights
* **The Cross-Family Transfer Gap:** Function vectors hold up inside GPT-J and fall apart across model families. I'm writing it up with the actual numbers, because a transfer claim without numbers is a horoscope.
* **ACM Research Hour:** Presenting the reproduction this fall, as practice for the people who will later ask harder questions and mean it.
"""

# --- 2. IMAGE PREPROCESSING (rembg + CLAHE) ---
def process_source_image(img_path):
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Could not open image at {img_path}")
        
    print("[1/4] Stripping background...")
    rgba_img = remove(img)
    bgr = rgba_img[:, :, 0:3]
    alpha = rgba_img[:, :, 3]

    print("[2/4] Boosting local features via CLAHE...")
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    
    # Aggressive clip limit ensures faint features register clearly over the dark canvas background
    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
    cl_gray = clahe.apply(gray)
    
    return cl_gray, alpha

# --- 3. DYNAMIC SHIMMER MATRIX GENERATOR ---
def generate_readme_frames(gray_img, alpha, bio_text, cols=75, scale=0.43, frames=5):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    h, w = gray_img.shape
    img_w = w / cols
    img_h = img_w / scale
    rows = int(h / img_h)
    
    resized_gray = cv2.resize(gray_img, (cols, rows))
    resized_alpha = cv2.resize(alpha, (cols, rows))

    for frame in range(frames):
        markdown_output = []
        markdown_output.append("<table>")
        markdown_output.append("<tr>")
        
        markdown_output.append('<td valign="top" width="55%">\n\n```text')
        
        for r_idx, row in enumerate(resized_gray):
            line_chars = []
            for c_idx, pixel in enumerate(row):
                # Check background transparency mask threshold directly
                if resized_alpha[r_idx, c_idx] < 30:
                    line_chars.append(" ")
                else:
                    # Subtle ambient noise ripple across vertical channels over time
                    shimmer_offset = int(np.sin((r_idx / 6.0) + (frame * 0.9)) * 15)
                    adjusted_pixel = np.clip(pixel + shimmer_offset, 0, 255)
                    char_idx = int(adjusted_pixel / 256 * len(ASCII_CHARS))
                    line_chars.append(ASCII_CHARS[char_idx])
                    
            markdown_output.append("".join(line_chars))
            
        markdown_output.append("```\n\n</td>")
        markdown_output.append(f'<td valign="top" width="45%">\n\n{bio_text}\n\n</td>')
        markdown_output.append("</tr>")
        markdown_output.append("</table>")
        
        frame_path = os.path.join(OUTPUT_DIR, f"readme_frame_{frame}.md")
        with open(frame_path, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_output))
            
    print(f"[4/4] Dark mode optimization engine successfully baked in '{OUTPUT_DIR}/'!")

if __name__ == "__main__":
    processed_gray, alpha_channel = process_source_image(IMAGE_PATH)
    generate_readme_frames(processed_gray, alpha_channel, BIO_MARKDOWN, cols=75, frames=FRAME_COUNT)
