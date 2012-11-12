import os
import zipfile
import shutil
from sys import exit
from Tkinter import *
import tkFileDialog, tkMessageBox

class Application(Frame):
	
	def openDir(self):
		self.txtDir.set(tkFileDialog.askdirectory(parent=self,initialdir="/",title='Please select a directory'))

	def packageFiles(self):
	
		self.dir = self.txtDir.get()
		if not os.path.isdir(self.dir):
			self.failure("Could not open directory:" + self.dir)
			return False
		
		self.export = self.txtOutput.get()
		
		if self.export == "":
			self.failure("Please enter a name for the output folder.")
			return False
		path = os.path.join(os.getcwd(), self.export)
		if os.path.isfile(path + ".love") or os.path.isdir(path) or os.path.isfile(path + ".zip"):
			self.failure("File/Folder already exists!")
			return False
			
		option = self.rbOutputType.get()
		if option == 1:
			self.makeLoveFile()
			
		else:
			self.makeApp()
			
		self.success(self.export)
		self.clearInput()
		
		return True
	
	def makeLoveFile(self):
		z = zipfile.ZipFile(self.export + ".zip", "w", zipfile.ZIP_DEFLATED)

		rootlen = len(self.dir) + 1
		for root, dirs, files in os.walk(self.dir):
			for name in files:
				fn = os.path.join(root, name)
				z.write(fn, fn[rootlen:])
				
		z.close()

		os.rename(self.export + ".zip", self.export + ".love")
	
	def makeApp(self):
		#make a .love file
		self.makeLoveFile()
		
		#then pack files into a .exe
		os.system("copy /b love.exe+" + self.export + ".love " + self.export + ".exe")
		os.mkdir(self.export)

		shutil.copyfile(self.export + ".exe", self.export + "/" + self.export + ".exe")
		shutil.copyfile("SDL.dll", self.export + "/SDL.dll")
		shutil.copyfile("openal32.dll", self.export + "/openal32.dll")
		shutil.copyfile("DevIL.dll", self.export + "/DevIL.dll")

		os.remove(self.export + ".love")
		os.remove(self.export + ".exe")
		
		zipbool = self.chkZip.get()
		if zipbool == 1:
			z = zipfile.ZipFile(self.export + ".zip", "w", zipfile.ZIP_DEFLATED)
			rootlen = len(self.export) + 1
			for root, dirs, files in os.walk(self.export):
				for name in files:
					fn = os.path.join(root, name)
					z.write(fn, fn[rootlen:])
					os.remove(fn)

			z.close()
			os.removedirs(self.export)
		
		return True
	
	def toggleRadioButton(self, event):
		if event.widget == self.rbBuildLove:
			self.chkZipObj.deselect()
			self.chkZipObj.config(state=DISABLED)
		elif event.widget == self.rbBuildExe:
			self.chkZipObj.config(state=NORMAL)
		
	
	def success(self, export):
		tkMessageBox.showinfo(
            "Success!",
            "Successfully created:\n" + export
        )
		
	def failure(self, txt):
		tkMessageBox.showerror(
            "Oops!",
            "Error:\n" + txt
        )
	
	def showCredits(self):
		tkMessageBox.showinfo(
            "Credits",
            u"Created by and copyright of Samuel Jackson \u00A9 2011. \n All rights reserved."
        )
	
	def showAbout(self):
		tkMessageBox.showinfo(
            "About",
            "Love Zipper is an application designed to turn a directory of Love Lua files into application executable. It can also zip the output for you."
        )
	
	def clearInput(self):
		self.txtDir.set("")
		self.txtOutput.set("")
		
	
	def exit(self):
		exit()
		
	def createWidgets(self):
		menu = Menu(self)
		root.config(menu=menu)

		filemenu = Menu(menu)
		helpmenu = Menu(menu)
		
		menu.add_cascade(label="File", menu=filemenu)
		menu.add_cascade(label="Help", menu=helpmenu)
		
		filemenu.add_command(label="Pack", command=self.packageFiles)
		filemenu.add_command(label="Exit", command=self.exit)
		
		helpmenu.add_command(label="About", command=self.showAbout)
		helpmenu.add_command(label="Credits", command=self.showCredits)
		
		
		self.lblDir = Label(self, text="Select a directory:", anchor=W, justify=LEFT).grid(row=0, sticky=W)
		
		self.txtDir = StringVar()
		self.txtDirObj = Entry(self, textvariable=self.txtDir, width=32).grid(row=1, columnspan=2, sticky=W)
		
		self.btnOpenDir = Button(self, text="Browse...", command= self.openDir).grid(row=1, column=1, sticky=E)
		
		self.lblOuput = Label(self, text="Name of output folder:", anchor=W, justify=LEFT).grid(row=3, sticky=W)
		
		self.txtOutput = StringVar()
		self.txtOutputObj = Entry(self, textvariable=self.txtOutput, width=43).grid(row=4, columnspan=3, sticky=W)
		
		self.rbOutputType = IntVar()

		self.rbBuildLove = Radiobutton(self, text="Build .love File", variable=self.rbOutputType, value=1)
		self.rbBuildExe = Radiobutton(self, text="Build .exe distibution", variable=self.rbOutputType, value=2)
		
		self.rbBuildLove.select()
		
		self.rbBuildLove.grid(row=5, sticky=W)
		self.rbBuildExe.grid(row=5, column=1, sticky=W)
		
		self.rbBuildLove.bind("<Button-1>", self.toggleRadioButton)
		self.rbBuildExe.bind("<Button-1>", self.toggleRadioButton)
		
		self.chkZip = IntVar()
		self.chkZipObj = Checkbutton(self, text="Zip Ouput Folder?", variable=self.chkZip, state=DISABLED)
		self.chkZipObj.grid(row=7, sticky=W)
		
		self.btnPack = Button(self, text="Pack!", command=self.packageFiles).grid(row=8, sticky=W)

	def __init__(self, master=None):
		Frame.__init__(self, master)
		
		#init properties
		self.export = ""
		self.dir = ""
		
		self.pack()
		self.createWidgets()

root = Tk()
root.geometry("%dx%d%+d%+d" % (300, 190, 100, 100))
root.title("LoveZipper")
app = Application(master=root)
app.mainloop()
sys.exit()