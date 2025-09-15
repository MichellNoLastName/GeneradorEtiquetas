import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os.path
import cv2
import os
import errno

global code 
global dinamicCodeLow, dinamicCodeUp
global pointX, pointY
global filename

def widgetsUp():
    staticCodeEntered.configure(state="enable")
    dinamicCode1Entered.configure(state="enable")
    dinamicCode2Entered.configure(state="enable")
    xPointEntered.configure(state="enable")
    yPointEntered.configure(state="enable")
    previewButton.configure(state="enable")
    generateButton.configure(state="enable")

def loadImageCV2(filename):
    name = filename.split("/")
    name = name[-1]
    image = cv2.imread(filename)
    height, width, _ = image.shape
    imageNameText.set(name)
    heightText.set(str(height) + " px")
    widthText.set(str(width) + " px")
    messagebox.showinfo(message="Now, must you insert data and coordinate values.\nAfter, click Preview to see preliminary results", title="Instructions")

def showImageCV2(pointX, pointY):
    global filename
    global code
    global dinamicCodeLow
    image = cv2.imread(filename)
    color = (0,0,0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    size = 0.65
    bond = 2
    point = (pointX, pointY)
    text = code + " " + str(dinamicCodeLow)
    cv2.putText(image, text,point, font, size, color, bond )
    cv2.imshow("Preview", image)

def showImageLoaded():
    global code
    global dinamicCodeLow
    global dinamicCodeUp
    global pointX, pointY
    code = staticCode.get()
    dinamicCodeLow = dinamicCode1.get()
    dinamicCodeUp = dinamicCode2.get()
    pointX = xPoint.get()
    pointY =  yPoint.get()

    if((code != '') and (dinamicCodeUp != '') and (dinamicCodeLow != '') and (pointX != '') and (pointY != '')):
        try:
            dinamicCodeUp = int(dinamicCodeUp)
            dinamicCodeLow = int(dinamicCodeLow)
            pointX = int(pointX)
            pointY = int(pointY)
            if((type(dinamicCodeLow) is int ) and (type(dinamicCodeUp) is int) and (type(pointX) is int) and (type(pointY) is int)):
                showImageCV2(pointX, pointY)
        except Exception as e:
            print(e.args)
            messagebox.showerror(message="Format input is not valid", title="Invalid Format")
    else:
        messagebox.showerror(message="ALL data is required", title="Blank textboxs")



def generateImages():
    global dinamicCodeLow, dinamicCodeUp
    global filename
    global code
    global pointX, pointY
   
    color = (0,0,0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    size = 0.65
    bond = 2
    point = (pointX, pointY)
    

    if(dinamicCodeUp > dinamicCodeLow):
        try:
            messagebox.showinfo(message="Now, choose directory where images will save")
            filedir = filedialog.askdirectory()
            print(filedir)
            os.mkdir(filedir+"\imagesGenerated")
            filedir = filedir + "\imagesGenerated"

            for x in range(dinamicCodeLow, dinamicCodeUp+1):
                image = cv2.imread(filename)
                text = code + " " + str(x)
                cv2.putText(image, text, point, font, size, color, bond)
                cv2.imwrite(f"{filedir}\\{code}{x}.png", image)
            messagebox.showinfo(message="Images generated", title="Notification")
        except OSError as e:
            if e.errno != errno.EEXIST:
                pass
            else:
                print(e.args)
    else:
        messagebox.showerror(message="Interval error", title="Error")
    

def loadImage():
    global filename
    extensions = [".png", ".jpg", ".bmp", ".jpeg"]
    filename = filedialog.askopenfilename()
    _, extension = os.path.splitext(filename)
    if(extension in extensions):
        widgetsUp()
        loadImageCV2(filename)
    else:
        messagebox.showerror(message="File type not valid", title="File Type")

        
    
root = tk.Tk()
root.title("HANTEC Designer Tool")
root.geometry("940x590")
root.resizable(False, False)
root.configure(bg="white")

icon = tk.PhotoImage(file="scanning.png")
root.iconphoto(True,icon)

mighty = ttk.LabelFrame(root,text=" Serial Number Generator ")
mighty.grid(column=0,row=0,padx=8,pady=4)

imageHantec = tk.PhotoImage(file="hantec.jpg")
label = ttk.Label(mighty,image=imageHantec).grid(column=3,row=0)

imageStatic = tk.PhotoImage(file="codigoEstatico.png")
imageDinamic = tk.PhotoImage(file="codigoDinamico.png")
labelStatic = ttk.Label(mighty,image=imageStatic).grid(column=1,row=4,padx=8,pady=6)
labelDinamic = ttk.Label(mighty,image=imageDinamic).grid(column=4,row=4,padx=8,pady=6)

staticLabel = ttk.Label(mighty,text="Code:")
staticLabel.configure(font=("Courier", 16, "bold","italic"))
staticLabel.grid(column=1,row=5)
staticCode = tk.StringVar()
staticCodeEntered = ttk.Entry(mighty, width=14, textvariable=staticCode, state="disable")
staticCodeEntered.configure(font=("Courier", 14, "bold"))
staticCodeEntered.grid(column=2,row=5,padx=2, pady=8)

dinamicLabel1 = ttk.Label(mighty, text="From:")
dinamicLabel1.configure(font=("Courier", 16, "bold","italic"))
dinamicLabel1.grid(column=3,row=5)
dinamicCode1 = tk.StringVar()
dinamicCode1Entered = ttk.Entry(mighty, width=14, textvariable=dinamicCode1, state="disable")
dinamicCode1Entered.configure(font=("Courier", 14, "bold"))
dinamicCode1Entered.grid(column=4,row=5, padx=2, pady=8)

dinamicLabel2 = ttk.Label(mighty, text="To:")
dinamicLabel2.configure(font=("Courier", 16, "bold","italic"))
dinamicLabel2.grid(column=5, row=5, padx=8, pady=2)
dinamicCode2 = tk.StringVar()
dinamicCode2Entered = ttk.Entry(mighty, width=14, textvariable=dinamicCode2, state="disable")
dinamicCode2Entered.configure(font=("Courier", 14, "bold"))
dinamicCode2Entered.grid(column=6, row=5)

xPointLabel = ttk.Label(mighty, text="Point X:")
xPointLabel.configure(font=("Courier", 16, "bold","italic"))
xPointLabel.grid(column=1, row=6)
xPoint = tk.StringVar()
xPointEntered = ttk.Entry(mighty, width=10, textvariable=xPoint, state="disable")
xPointEntered.configure(font=("Courier", 14, "bold"))
xPointEntered.grid(column=2, row=6)

yPointLabel = ttk.Label(mighty, text="Point Y:")
yPointLabel.configure(font=("Courier", 16, "bold","italic"))
yPointLabel.grid(column=3, row=6)
yPoint = tk.StringVar()
yPointEntered = ttk.Entry(mighty, width=10, textvariable=yPoint, state="disable")
yPointEntered.configure(font=("Courier", 14, "bold"))
yPointEntered.grid(column=4, row=6)

#Load image
loadImageLabel = ttk.Label(mighty, text="Load Image")
loadImageLabel.configure(font=("Courier", 16, "bold","italic"))
loadImageLabel.grid(column=2,row=7, padx=2, pady=8)
imgSearch = tk.PhotoImage(file="buscar.png")
loadImageButton = ttk.Button(mighty, image=imgSearch, command=loadImage)
loadImageButton.grid(column=2, row=8, padx=2, pady=8)

#preview image
previewLabel = ttk.Label(mighty, text="Preview")
previewLabel.configure(font=("Courier", 16, "bold","italic"))
previewLabel.grid(column=4, row=7, padx=2, pady=8)
imgPreview = tk.PhotoImage(file="preview.png")
previewButton = ttk.Button(mighty, image=imgPreview, command=showImageLoaded)
previewButton.grid(column=4, row=8, padx=2, pady=8)
previewButton.configure(state="disable")

#image features
imageNameLabel = ttk.Label(mighty, text="Image Name:")
imageNameLabel.configure(font=("Courier", 16, "bold","italic"))
imageNameLabel.grid(column=1, row=9)
imageNameText = tk.StringVar()
imageNameTextEntered = ttk.Entry(mighty, width=16, textvariable=imageNameText)
imageNameTextEntered.grid(column=2, row=9,padx=2, pady=4)
imageNameTextEntered.configure(font=("Courier", 14, "bold"),state="readonly")
widthLabel = ttk.Label(mighty, text="Width:")
widthLabel.configure(font=("Courier", 16, "bold","italic"))
widthLabel.grid(column=1, row=10)
widthText = tk.StringVar()
widthTextEntered = ttk.Entry(mighty, width=10, textvariable=widthText)
widthTextEntered.grid(column=2, row=10,padx=2, pady=4)
widthTextEntered.configure(font=("Courier", 14, "bold"),state="readonly")
heightLabel = ttk.Label(mighty, text="Height:")
heightLabel.configure(font=("Courier", 16, "bold","italic"))
heightLabel.grid(column=1, row=11)
heightText = tk.StringVar()
heightTextEntered = ttk.Entry(mighty, width=10, textvariable=heightText)
heightTextEntered.grid(column=2, row=11,padx=2, pady=4)
heightTextEntered.configure(font=("Courier", 14, "bold"),state="readonly")

#generate button
generateImagesLabel = ttk.Label(mighty, text="Generate Images")
generateImagesLabel.configure(font=("Courier", 16, "bold","italic"))
generateImagesLabel.grid(column=3, row=12, padx=2, pady=4)
imageGenerate = tk.PhotoImage(file="content-writing.png")
generateButton = ttk.Button(mighty, image=imageGenerate, command=generateImages)
generateButton.grid(column=3, row=13, padx=4, pady=8)
generateButton.configure(state="disable")

root.mainloop()

