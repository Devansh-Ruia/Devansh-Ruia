import os

OUTPUT_DIR = "data"
FRAME_COUNT = 5

# Hand-traced ASCII structural design for clean, sharp vector moth wings and edges
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

def generate_readme_frames(art_lines, bio_text, frames=5):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    bio_lines = [line.rstrip() for line in bio_text.split("\n")]
    art_height = len(art_lines)
    art_width = len(art_lines[0])
    total_height = max(art_height, len(bio_lines))

    for frame in range(frames):
        markdown_output = []
        markdown_output.append("<table>")
        markdown_output.append("<tr>")
        
        # Left column: Clean vector codeblock
        markdown_output.append('<td valign="top" width="50%">\n\n```text')
        
        for i in range(total_height):
            # Render the stationary hand-traced vector artwork
            if i < art_height:
                art_part = art_lines[i]
            else:
                art_part = " " * art_width
                
            # Add a subtle vertical shimmer to the texture blocks inside the wings
            animated_chars = []
            for idx, char in enumerate(art_part):
                if char in ["#", "@", "%", "*"]:
                    # Pulse the structural characters to give it life without losing shape
                    shimmer_pool = ["*", "%", "@", "#"]
                    pool_idx = (shimmer_pool.index(char) + frame) % len(shimmer_pool)
                    animated_chars.append(shimmer_pool[pool_idx])
                else:
                    animated_chars.append(char)
            
            art_line = "".join(animated_chars)
            bio_part = bio_lines[i] if i < len(bio_lines) else ""
            
            # Combine sides seamlessly with an absolute layout separator column
            markdown_output.append(f"{art_line}   ¦  {bio_part}")
            
        markdown_output.append("```\n\n</td>")
        markdown_output.append("</tr>")
        markdown_output.append("</table>")
        
        frame_path = os.path.join(OUTPUT_DIR, f"readme_frame_{frame}.md")
        with open(frame_path, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_output))
            
    print(f"[Success] Structural vector artwork layout compiled successfully in '{OUTPUT_DIR}/'!")

if __name__ == "__main__":
    generate_readme_frames(MOTH_ART, BIO_MARKDOWN, frames=FRAME_COUNT)
