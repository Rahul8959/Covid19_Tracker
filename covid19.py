import requests
import bs4
import tkinter as tk

def get_htrml_data(url):
    data = requests.get(url)
    return data

def get_covid_data():
    url = 'https://www.worldometers.info/coronavirus/'
    html_data = get_htrml_data(url)
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    info_div = bs.find('div', class_="content-inner").findAll("div", id="maincounter-wrap")
    all_data = ""

    # print(info_div)
    for block in info_div:
        # print(block)
        text = block.find("h1", class_=None).get_text()

        count = block.find("span", class_=None).get_text()

        all_data = all_data + text + " " + count + "\n"

    return all_data

def reload():
    textfield.delete(0, 'end')
    new_data = get_covid_data()
    mainlabel['text']=new_data

def get_county_data():
    name = textfield.get()
    url = "https://www.worldometers.info/coronavirus/country/"+name

    html_data = get_htrml_data(url)
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    
    # Check if the content-inner div is found
    content_inner_div = bs.find('div', class_="content-inner")
    if content_inner_div:
        info_div = content_inner_div.findAll("div", id="maincounter-wrap")
    else:
        mainlabel['text'] = "Please enter a valid country name."
        return
    
    all_data =""
    
    for block in info_div:
        h1_tag = block.find("h1", class_=None)
        if h1_tag:
            text = h1_tag.get_text()
            count = block.find("span", class_=None).get_text()
            all_data = all_data + text + " " + count + "\n"

    mainlabel['text'] = all_data
    

root = tk.Tk()
root.geometry("700x600")
root.title("Covid-19 Tracker")
bgcolor="#f3f5c4"
root.configure(bg=bgcolor)

# Fonts
title_font = ("Arial", 30, "bold")
button_font = ("Arial", 15)
label_font = ("Arial", 16)

# Load the image
banner = tk.PhotoImage(file="image/covid_logo.png")
resized_banner = banner.subsample(5, 5) 

# Banner
bannerlabel = tk.Label(root, image=resized_banner, bg=bgcolor)
bannerlabel.pack(pady=(30, 30))

# Text Entry with placeholder text
textfield = tk.Entry(root, width=40, font=10, bd=2, justify="center", bg="white")
textfield.insert(0, 'Enter the City Name')  # Add placeholder text
textfield.bind("<FocusIn>", lambda event: textfield.delete('0', 'end'))  # Clear placeholder text on focus
textfield.pack(pady=(5, 10), ipady=8) 

# Buttons
gbtn = tk.Button(root, text='Get Data', font=button_font, command=get_county_data,
                 bg='#787872',
                 fg='#ffffff',
                 bd=0, 
                 relief=tk.FLAT,
                 height=1,
                 width=13,
                 cursor="hand2")
gbtn.pack(pady=5)

rbtn = tk.Button(root, text='Reload', font=button_font, command=reload,
                 bg='#787872',
                 fg='#ffffff',
                 bd=0,  
                 relief=tk.FLAT,
                 height=1,
                 width=10,
                 cursor="hand2") 
rbtn.pack(pady=5)

# Label to display data
mainlabel = tk.Label(root, text=get_covid_data(), font=label_font, bg=bgcolor)
mainlabel.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()