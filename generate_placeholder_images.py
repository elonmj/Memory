
import re
from PIL import Image, ImageDraw, ImageFont

def generate_placeholder_images(log_file):
    """
    Generates placeholder images for missing files reported in a LaTeX log file.
    """
    missing_files = ["images/specificites_benin/composition_parc",
                     "images/specificites_benin/types_routes",
                     "images/specificites_benin/gap_filling"]
    # with open(log_file, 'r', encoding='utf-8') as f:
    #     for line in f:
    #         match = re.search(r"LaTeX Error: File `(.*?)' not found", line)
    #         if match:
    #             missing_files.append(match.group(1))

    for file_path in missing_files:
        # Extract the filename from the path
        file_name = file_path.split('/')[-1]
        
        # Define image size and create a new image
        img_width = 600
        img_height = 400
        img = Image.new('RGB', (img_width, img_height), color='lightgrey')
        d = ImageDraw.Draw(img)

        # Choose a font and font size
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            font = ImageFont.load_default()

        # Calculate text size and position
        text = f"Placeholder: {file_name}"
        bbox = d.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (img_width - text_width) // 2
        text_y = (img_height - text_height) // 2

        # Add text to the image
        d.text((text_x, text_y), text, fill='black', font=font)

        # Create the directory if it doesn't exist
        import os
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Save the image as a PNG file
        img.save(file_path + ".png")
        print(f"Generated placeholder image for {file_path}")

if __name__ == "__main__":
    generate_placeholder_images("memoire.log")
