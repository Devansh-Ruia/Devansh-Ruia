import os

OUTPUT_DIR = "data"
FRAME_COUNT = 5

# Hand-traced ASCII moth artwork matching the crisp structure of the reference style
MOTH_ART = [
    "                      .                      ",
    "                     /|\\                     ",
    "                    / | \\                    ",
    "                   /  |  \\                   ",
    "                  /   |   \\                  ",
    "              .---'   |   '---.              ",
    "             /  %@##  |  ##@%  \\             ",
    "            /  %@###  |  ###@%  \\            ",
    "           /  %####   |   ####%  \\           ",
    "          /  #####:   |   :#####  \\          ",
    "         /  #####: .--|--. :#####  \\         ",
    "        /  #####: /   |   \\ :#####  \\        ",
    "       /  #####: |    |    | :#####  \\       ",
    "      /  #####:   \\   |   /   :#####  \\      ",
    "     /  #####:     '--|--'     :#####  \\     ",
    "    '=======-.        |        .-======='    ",
    "      \\  ####\\        |        /####  /      ",
    "       \\  ####\\       |       /####  /       ",
    "        \\  ####\\      |      /####  /        ",
    "         \\  ####\\     |     /####  /         ",
    "          \\  ####\\    |    /####  /          ",
    "           \\  ####\\   |   /####  /           ",
    "            '------'  |  '------'            ",
    "                      '                      "
]

# Standardized flat-text layout for a perfect terminal look inside a raw codeblock
BIO_LINES = [
    "Devansh Ruia",
    "---------------------------------------------",
    "OS:             Northeastern Linux (CS Core)",
    "Focus:          Mechanistic Interpretability",
    "Mission:        Explaining how neural nets work using",
    "                the networks that won't explain themselves.",
    "",
    "What I'm Working On Now:",
    "  - Function Vectors to Tool Selection (Todd et al.)",
    "    Isolated a vector making GPT-J act like it read instructions,",
    "    breaks moving across model families.",
    "  - Blackout Markets (Shadow-mode cost/carbon optimizer)",
    "    Provides cloud recommendations operators can ignore.",
    "  - Sparse Autoencoders (Because free time is an issue)",
    "",
    "Previously:",
    "  - Reproduced function vectors on GPT-J using nnsight",
    "  - Built Blackout Markets repo up to 62 passing tests",
    "",
    "The Stack:",
    "  - Research: Python, PyTorch, nnsight, HF Transformers",
    "  - Product:  TypeScript, Express, React, Vite, Vercel",
    "",
    "Highlights:",
    "  - Documenting the Cross-Family Transfer Gap numbers",
    "  - Presenting the reproduction at ACM Research Hour"
]

def generate_readme_frames(art_lines, bio_text_lines, frames=5):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    art_height = len(art_lines)
    bio_height = len(bio_text_lines)
    total_height = max(art_height, bio_height)
    
    # Get the fixed length of the artwork lines to ensure text alignment doesn't stagger
    art_width = len(art_lines[0])

    for frame in range(frames):
        markdown_output = []
        markdown_output.append("```text") # Open a single top-level code container
        
        for i in range(total_height):
            # 1. Fetch artwork row
            if i < art_height:
                art_part = art_lines[i]
            else:
                art_part = " " * art_width
                
            # Subtle vertical noise shimmer loop inside texture patches only
            animated_chars = []
            for char in art_part:
                if char in ["#", "@", "%", "*"]:
                    shimmer_pool = ["*", "%", "@", "#"]
                    pool_idx = (shimmer_pool.index(char) + frame) % len(shimmer_pool)
                    animated_chars.append(shimmer_pool[pool_idx])
                else:
                    animated_chars.append(char)
            
            clean_art_line = "".join(animated_chars)
            
            # 2. Fetch bio content row
            bio_part = bio_text_lines[i] if i < bio_height else ""
            
            # 3. Piece together using fixed string padding
            markdown_output.append(f"{clean_art_line}   |  {bio_part}")
            
        markdown_output.append("```")
        
        frame_path = os.path.join(OUTPUT_DIR, f"readme_frame_{frame}.md")
        with open(frame_path, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_output))
            
    print(f"[Success] Pure terminal layout files generated in '{OUTPUT_DIR}/'!")

if __name__ == "__main__":
    generate_readme_frames(MOTH_ART, BIO_LINES, frames=FRAME_COUNT)
