import tkinter as tk
from PIL import ImageTk, Image 
import requests

############################## event handlers #######################################

#Event handler for the 'Close' button
def close_it():
  exit(0)

#Event handler for the 'Run' button
def run_it(*Args):
#clean out what is left from any previous request
  response_label['text'] = "HTTP response status: " 
  header_listbox.delete(0, tk.END)
  canvas.delete("all")

 #Gets the entry from the URL box and stores it in variable 'url_path'
  url_path = url_textbox.get()

 #Imports the requests packet
 #Runs the HTTP request, captures the response and stores it in a variable called response
 #Handles error in case of any
  import requests 
  try:
   response = requests.get(url_path, "r")
  except:
   response_text['text'] = "Error capturing response... "
 
 #If the response was successful, displays the response status code 
  response_text['text'] = response.status_code 
  
 #Displays the HTTP response headers
  response_headers = requests.get(url_path).headers
  for attribute, value in response_headers.items():
   header_listbox.insert(tk.END, '{} : {}'.format(attribute, value))

 #Checks to see if what we retrieved is actually an image. If not, handles the error
  if "image/" not in response_headers['Content-Type']:
   canvas.create_text(120, 30, text = "This url does not contain an image...try again")
   return()
   
  #opens image 
  try:
    open("my_image", 'wb').write(response.content)
  except:
    response_label['text'] = "Image download failed... "
    return

#Display the image   
  global img
  img = Image.open("my_image") 
  
  img = ImageTk.PhotoImage(img) 
  canvas.create_image(1, 1, image = img, anchor = tk.NW)
  canvas.config(scrollregion = canvas.bbox(tk.ALL))

################################# main #########################################

#Create the root window
window = tk.Tk()
window.title("Simple HTTP Image Browser")
window.bind('<Return>', run_it)

#Three frames:
url_frame = tk.Frame(master = window)
status_frame = tk.Frame(master = window)
header_frame = tk.Frame(master = window)
display_frame = tk.Frame(master = window)

url_frame.pack(side = tk.TOP, fill = tk.BOTH)
status_frame.pack(side = tk.TOP, fill = tk.BOTH)
header_frame.pack(side = tk.TOP, fill = tk.BOTH)
display_frame.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

#URL label, textbox and run/stop buttons for URL frame
url_label = tk.Label(master = url_frame, text = " Image URL: ", justify = tk.LEFT)
url_textbox = tk.Entry(master = url_frame, width = 100)
run_button = tk.Button(text = "Go", master = url_frame, command = run_it)
close_button = tk.Button(text = "Exit", master = url_frame, command = close_it)

url_label.pack(side = tk.LEFT)
url_textbox.pack(side = tk.LEFT, expand = True)
run_button.pack(side = tk.LEFT)
close_button.pack(side = tk.LEFT)

#Response label and text:
response_label = tk.Label(master = status_frame, text = " HTTP response status: ", justify = tk.LEFT)
response_text = tk.Label(master = status_frame, text = "goes here", justify = tk.LEFT)
response_label.pack(side = tk.LEFT)
response_text.pack(side = tk.LEFT)

#HTTP response header listbox
header_listbox = tk.Listbox(master = header_frame, width = 125, height = 10)
header_listbox.pack(side = tk.LEFT, fill = tk.Y)
header_listbox.insert(tk.END, "")
header_listbox.insert(tk.END, " HTTP response headers go here")

#Scrollbar for the header listbox
scrollbar = tk.Scrollbar(master = header_frame)
scrollbar.pack(side = tk.LEFT, fill = tk.Y)

#Associate the scrollbar with the header listbox
header_listbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = header_listbox.yview)

#Set canvas dimensions
canvas_width = 500
canvas_height = 500

#Canvas for image display
canvas = tk.Canvas(master = display_frame, width = canvas_width, height = canvas_height)

#Scrollbars for the canvas
hscrollbar = tk.Scrollbar(master = display_frame, orient = tk.HORIZONTAL)
hscrollbar.pack(side = tk.BOTTOM, fill = tk.X)
hscrollbar.config(command = canvas.xview) 

vscrollbar = tk.Scrollbar(master = display_frame, orient = tk.VERTICAL)
vscrollbar.pack(side = tk.RIGHT, fill = tk.Y)
vscrollbar.config(command = canvas.yview) 

#Associate the scrollbars with the canvas
canvas.config(width = canvas_width, height = canvas_height)
canvas.config(xscrollcommand = hscrollbar.set, yscrollcommand = vscrollbar.set)

#Pack canvas
canvas.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)

canvas.create_text(110, 25, text="Images will be displayed here...")

window.mainloop()