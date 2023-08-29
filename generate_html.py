import os
import glob

def generate_html():
    # Vind alle bestanden met de gegeven extensies
    extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(f'contents/fotos/*.{ext}'))

    # Sorteer de bestanden (optioneel)
    image_files.sort()

    # Begin met het genereren van HTML
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Foto Slideshow</title>
    <style>
        /* Zorg ervoor dat de afbeelding altijd op het scherm past */
        #slideshow img {
            max-width: 100%;
            max-height: 100vh;
            object-fit: contain;
        }
    </style>
    <meta http-equiv="refresh" content="3600">
</head>
<body>

<div id="slideshow">
"""

    # Voeg afbeeldingen toe aan HTML
    for image_file in image_files:
        rel_path = os.path.relpath(image_file, start='.')
        html_content += f'    <img src="{rel_path}" alt="{rel_path}" style="display:none;">\n'

    # Voeg script toe voor het wisselen van de foto's
    html_content += """
</div>

<script>
    var index = 0;
    function showNextImage() {
        var images = document.querySelectorAll("#slideshow img");
        images[index].style.display = "none";
        index = (index + 1) % images.length;
        images[index].style.display = "block";
    }
    setInterval(showNextImage, 2000);
    // Toon de eerste afbeelding
    showNextImage();
</script>

</body>
</html>
"""

    # Schrijf de HTML naar een bestand
    with open('pagina.html', 'w') as f:
        f.write(html_content)

# Roep de functie aan
generate_html()
