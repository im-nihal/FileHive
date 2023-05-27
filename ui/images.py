from PIL import ImageTk, Image

try:
    about = ImageTk.PhotoImage(Image.open('images/about.png').resize((32, 32)))
    archive = ImageTk.PhotoImage(Image.open('images/zip.png').resize((32, 32)))
    back = ImageTk.PhotoImage(Image.open('images/back.png').resize((32, 32)))
    code = ImageTk.PhotoImage(Image.open('images/code.png').resize((32, 32)))
    desktop = ImageTk.PhotoImage(Image.open('images/desktop.png').resize((28, 29)))
    documents = ImageTk.PhotoImage(Image.open('images/documents.png').resize((30, 30)))
    downloads = ImageTk.PhotoImage(Image.open('images/downloads.png').resize((30, 30)))
    folder = ImageTk.PhotoImage(Image.open('images/folder.png').resize((30, 30)))
    frwd = ImageTk.PhotoImage(Image.open('images/forward.png').resize((32, 32)))
    github = ImageTk.PhotoImage(Image.open('images/git.png').resize((30, 30)))
    home = ImageTk.PhotoImage(Image.open('images/home.png').resize((30, 30)))
    ig = ImageTk.PhotoImage(Image.open('images/ig.png').resize((30, 30)))
    linkdIn = ImageTk.PhotoImage(Image.open('images/linkdIn.png').resize((32, 32)))
    me = ImageTk.PhotoImage(Image.open('images/me.jpeg'))
    mp3 = ImageTk.PhotoImage(Image.open('images/mp3.png').resize((30, 30)))
    music = ImageTk.PhotoImage(Image.open('images/music.png').resize((29, 29)))
    new_doc = ImageTk.PhotoImage(Image.open('images/newdoc.png').resize((32, 32)))
    new_fold = ImageTk.PhotoImage(Image.open('images/newfold.png').resize((32, 32)))
    pic = ImageTk.PhotoImage(Image.open('images/pic.png').resize((32, 32)))
    pdf = ImageTk.PhotoImage(Image.open('images/pdf.png').resize((32, 32)))
    pictures = ImageTk.PhotoImage(Image.open('images/pictures.png').resize((32, 32)))
    search = ImageTk.PhotoImage(Image.open('images/search.png').resize((32, 32)))
    txt = ImageTk.PhotoImage(Image.open('images/txt.png').resize((32, 32)))
    unknown = ImageTk.PhotoImage(Image.open('images/unknown.png').resize((32, 32)))
    vid = ImageTk.PhotoImage(Image.open('images/vid.png').resize((32, 32)))
    videos = ImageTk.PhotoImage(Image.open('images/videos.png').resize((29, 29)))
except IOError as e:
    print(f"Error loading image: {e}")