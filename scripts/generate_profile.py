import cv2
import numpy as np
from rembg import remove
import os

# --- 1. CONFIGURATION & DATA ---
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

    print("[2/4] Injecting local highlights via CLAHE...")
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    enhanced_bgr = cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2BGR)

    print("[3/4] Compositing to pure white mask background...")
    white_bg = np.full(enhanced_bgr.shape, 255, dtype=np.uint8)
    mask = cv2.merge([alpha.astype(float)/255.0]*3)
    fg = cv2.multiply(enhanced_bgr.astype(float), mask)
    bg = cv2.multiply(white_bg.astype(float), 1.0 - mask)
    
    final_bgr = cv2.add(fg, bg).astype(np.uint8)
    return cv2.cvtColor(final_bgr, cv2.COLOR_BGR2GRAY)

# --- 3. ASCII ART GENERATOR ---
def image_to_ascii(gray_img, cols=50, scale=0.43):
    h, w = gray_img.shape
    img_w = w / cols
    img_h = img_w / scale
    rows = int(h / img_h)
    
    resized = cv2.resize(gray_img, (cols, rows))
    ascii_matrix = []
    for row in resized:
        line = [ASCII_CHARS[int(pixel / 256 * len(ASCII_CHARS))] for pixel in row]
        ascii_matrix.append(line)
    return ascii_matrix

#--- 4. ANIMATION FRAME ENGINE ---
def generate_readme_frames(ascii_matrix, bio_text, frames=5):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ascii_width = len(ascii_matrix)

    for frame in range(frames):
        markdown_output = []
        markdown_output.append("<table>")
        markdown_output.append("<tr>")
        
        markdown_output.append('<td valign="top" width="50%">\n\n```text')
        for row in ascii_matrix:
            shifted_row = [row[(j + frame) % ascii_width] for j in range(ascii_width)]
            markdown_output.append("".join(shifted_row))
        markdown_output.append("```\n\n</td>")
        
        markdown_output.append(f'<td valign="top" width="50%">\n\n{bio_text}\n\n</td>')
        
        markdown_output.append("</tr>")
        markdown_output.append("</table>")
        
        frame_path = os.path.join(OUTPUT_DIR, f"readme_frame_{frame}.md")
        with open(frame_path, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_output))
            
    print(f"[4/4] Side-by-side layout generated successfully in '{OUTPUT_DIR}/'!")

if __name__ == "__main__":
    processed_gray = process_source_image(IMAGE_PATH)
    matrix = image_to_ascii(processed_gray, cols=50)
    generate_readme_frames(matrix, BIO_MARKDOWN, frames=FRAME_COUNT)
