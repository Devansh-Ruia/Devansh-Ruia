import os

OUTPUT_DIR = "data"
FRAME_COUNT = 5

# Hand-traced ASCII moth artwork matching the structure of your requested layout
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

# Your exact requested profile information
BIO_LINES = [
    "Devansh Ruia",
    "--------------------------------------------",
    "OS:       Northeastern Linux, CS core",
    "Kernel:   mechanistic interpretability",
    "Uptime:   sophomore year",
    "Mission:  explain how neural nets work using the",
    "          networks that won't explain themselves",
    "",
    "now:",
    "  Function vectors, extended to tool selection.",
    "  A vector makes GPT-J act like it read the",
    "  instructions, then quits at the family border.",
    "  Blackout Markets, a shadow-mode cost and carbon",
    "  optimizer that ships advice operators can ignore.",
    "  Sparse autoencoders next, since free time had",
    "  become a problem.",
    "",
    "previously:",
    "  Reproduced function vectors on GPT-J with nnsight.",
    "  Built Blackout Markets to 62 passing tests.",
    "",
    "stack:",
    "  research: Python, PyTorch, nnsight, HF Transformers",
    "  product:  TypeScript, Express, React, Vite, Vercel",
    "",
    "highlights:",
    "  The cross-family transfer gap, numbers in progress.",
    "  Presenting the reproduction at ACM Research Hour."
]

def generate_readme_frames(art_lines, bio_text_lines, frames=5):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    art_height = len(art_lines)
    bio_height = len(bio_text_lines)
    total_height = max(art_height, bio_height)
    art_width = len(art_lines[0])

    for frame in range(frames):
        markdown_output = []
        markdown_output.append("```text")
        
        for i in range(total_height):
            # 1. Fetch artwork row
            if i < art_height:
                art_part = art_lines[i]
            else:
                art_part = " " * art_width
                
            # Shimmer loop cycling inside texture blocks only
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
            
            # 3. Combine with alignment pipe layout matching your example
            markdown_output.append(f"{clean_art_line}  |  {bio_part}")
            
        markdown_output.append("```")
        
        frame_path = os.path.join(OUTPUT_DIR, f"readme_frame_{frame}.md")
        with open(frame_path, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_output))
            
    print(f"[Success] Updated frames generated in '{OUTPUT_DIR}/'!")

if __name__ == "__main__":
    generate_readme_frames(MOTH_ART, BIO_LINES, frames=FRAME_COUNT)
