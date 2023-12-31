import os
import glob
import csv

def read_captions():
    captions = {}
    try:
        with open('contents/captions.csv', mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:  # Sla lege rijen over
                    continue 
                filepath, caption = row
                filename = os.path.basename(filepath)  # Haal alleen de bestandsnaam eruit
                captions[filename.lower()] = caption  # Sla op in kleine letters
    except FileNotFoundError:
        print("Geen captions.csv gevonden.")
    return captions

def generate_html():
    captions = read_captions()
    
    # Debug: Print de inhoud van de captions dictionary
    print(f"Captions: {captions}")

    extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(f'contents/fotos/*.{ext}'))

    # Debug: Print de verzamelde image files
    print(f"Image files: {image_files}")
    
    image_files.sort()
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Foto Slideshow</title>
    <meta name="apple-mobile-web-app-capable" content="yes">
    <style>
    body {
    background-color: black;
    margin: 0;
    padding: 0;
    }
    .slide img {
    max-width: 100%;
    max-height: 100vh;
    height: auto;
    width: auto;
    object-fit: contain;
    margin: auto;
    display: block;
    }    
    .slide {
    position: relative;
    display: none;
    }
    .slide p {
    position: absolute;
    bottom: 0;  
    left: 0;
    right: 0;
    color: white;
    background-color: rgba(0,0,0,0.6);  
    padding: 10px;
    width: 100%;
    box-sizing: border-box;
    font-family: 'Brush Script MT', cursive;
    font-size: 4em;
    text-align: center;
    }
    </style>
    <meta http-equiv="refresh" content="3600">
    </head>
    <body>
    <div id="slideshow">
    """

    for image_file in image_files:
        rel_path = os.path.relpath(image_file, start='.')
        filename = os.path.basename(image_file).lower() 
        caption = captions.get(filename, '')  
        html_content += f'    <div class="slide" style="display:none;">\n'
        html_content += f'        <img src="{rel_path}" alt="{rel_path}">\n'
        if caption:  # Alleen toevoegen als er een caption is
            html_content += f'        <p>{caption}</p>\n'
        html_content += f'    </div>\n'
        
    html_content += """
    </div>
    <script>
    function checkTime() {
        var now = new Date();
        var hour = now.getHours();
        var slideshow = document.getElementById("slideshow");
        if (hour >= 21 || hour < 9) {
            slideshow.style.display = "none";
            document.body.style.backgroundColor = "black";
        } else {
            slideshow.style.display = "block";
            document.body.style.backgroundColor = "black";
        }
    }
    
    var index = 0;
    function showNextImage() {
        var slides = document.querySelectorAll(".slide");
        slides[index].style.display = "none";
        index = (index + 1) % slides.length;
        slides[index].style.display = "block";
    }
    function showPrevImage() {
        var slides = document.querySelectorAll(".slide");
        slides[index].style.display = "none";
        index = (index - 1 + slides.length) % slides.length;
        slides[index].style.display = "block";
    }
    setInterval(showNextImage, 30000);
    showNextImage();
    
    document.body.addEventListener('click', function(event) {
        var x = event.clientX;
        var windowWidth = window.innerWidth;
        if (x > windowWidth / 2) {
            showNextImage();
        } else {
            showPrevImage();
        }
    });

    checkTime();
    setInterval(checkTime, 60000);
    
    </script>
    </body>
    </html>
    """
    
    with open('pagina.html', 'w') as f:
        f.write(html_content)

generate_html()
