import time
import requests
import os
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from tkinter import *
from PIL import Image, ImageTk
import tkinter.font
from tkinter import messagebox

product_dict = {}
product_number = None
doc_dir = os.path.join(os.path.expanduser("~"), "Documents")
links = []
product_links = []

def show_first_product():
    img = Image.open(image_path(0))
    img = img.resize((190, 260), Image.ANTIALIAS)
    img_tk = ImageTk.PhotoImage(img)
    image_product.create_image(0, 0, image=img_tk, anchor=NW)
    image_product.image = img_tk
    label_product.config(text=product_dict.get(image_path(0)))
    global product_number
    product_number = 0


def image_path(number):
    return os.path.join(os.path.expanduser("~"), "Documents")+"/"+str(number)+".png"


def trendyol(driver, product):
    global links
    global product_links
    product_links.clear()
    links.clear()
    driver.get("https://www.trendyol.com/sr?q=" + product)
    WebDriverWait(driver, 4).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "prc-box-dscntd")))
    products = driver.find_elements(By.CLASS_NAME, "prc-box-dscntd")
    images = driver.find_elements(By.CSS_SELECTOR, 'img.p-card-img')
    containers = driver.find_elements(By.CLASS_NAME, 'p-card-chldrn-cntnr')
    for container in containers:
        links.append(container.find_element(By.TAG_NAME, 'a'))
    for image in images:
        if image.get_attribute('src') == "https://cdn.dsmcdn.com/web/master/legal-requirement-card-new-white.png":
            driver.get("https://www.google.com/search?q=site:trendyol.com%20intext:18%20Ya%C5%9F%C4%B1ndan%20B%C3%BCy%C3%BC%C4%9F%C3%BCm")
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                try:
                    if href.startswith("https://www.trendyol.com"):
                        link.click()
                        break
                except:
                    pass
            button = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.ID, "confirmed")))
            button.click()
            driver.get("https://www.trendyol.com/sr?q=" + product)
            WebDriverWait(driver, 4).until(expected_conditions.visibility_of_element_located(
                (By.CLASS_NAME, "prc-box-dscntd")
            ))
            products = driver.find_elements(By.CLASS_NAME, "prc-box-dscntd")
            images = driver.find_elements(By.CSS_SELECTOR, 'img.p-card-img')
            break
    for index, image in enumerate(images):
        if index == 10:
            break
        image_link = image.get_attribute('src')
        file_name = "product_" + str(index) + ".png"
        file_location = os.path.join(doc_dir, file_name)
        response = requests.get(image_link)
        if response.status_code == 200:
            with open(file_location, 'wb') as file:
                file.write(response.content)
    global product_dict
    for index, price in enumerate(products):
        if index == 10:
            break
        product_dict[os.path.join(doc_dir, "product_"+str(index)+".png")] = price.text

    show_first_product()
    for link in links:
        product_links.append(link.get_attribute('href'))

def amazon(driver, product):
    global product_links
    product_links.clear()
    links.clear()
    messagebox.showinfo("Technical Error",
                        'Our tool has errors in product price and link matching for Amazon products, so we do not recommend using the amazon option.')
    driver.get("https://www.amazon.com.tr")
    time.sleep(0.5)
    driver.get("https://www.amazon.com.tr/s?k=" + product)
    WebDriverWait(driver, 4).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "a-price-whole")))
    products = driver.find_elements(By.CLASS_NAME, "a-price-whole")
    images = driver.find_elements(By.CSS_SELECTOR, 'img.s-image')
    containers = driver.find_elements(By.CSS_SELECTOR, 'a.s-no-hover')
    for container in containers:
        product_links.append(container.get_attribute('href'))
    for index, image in enumerate(images):
        if index == 10:
            break
        image_link = image.get_attribute('src')
        file_name = "product_" + str(index) + ".png"
        file_location = os.path.join(doc_dir, file_name)
        response = requests.get(image_link)
        if response.status_code == 200:
            with open(file_location, 'wb') as file:
                file.write(response.content)
    global product_dict
    for index, price in enumerate(products):
        if index == 10:
            break
        product_dict[os.path.join(doc_dir, "product_"+str(index)+".png")] = price.text

    show_first_product()


def n11(driver, product):
    global product_links
    product_links.clear()
    links.clear()
    driver.get("https://www.n11.com/arama?q=" + product)
    WebDriverWait(driver, 4).until(expected_conditions.visibility_of_element_located((By.TAG_NAME, "ins")))
    products = driver.find_elements(By.TAG_NAME, "ins")
    images = driver.find_elements(By.CSS_SELECTOR, 'img.lazy')
    containers = driver.find_elements(By.CSS_SELECTOR, "a.pro")
    for container in containers:
        product_links.append(container.get_attribute('href'))
    for index, image in enumerate(images):
        if index == 10:
            break
        image_link = image.get_attribute('data-lazy')
        file_name = "product_" + str(index) + ".png"
        file_location = os.path.join(doc_dir, file_name)
        response = requests.get(image_link)
        if response.status_code == 200:
            with open(file_location, 'wb') as file:
                file.write(response.content)
            # Load and display the image
    global product_dict
    for index, price in enumerate(products):
        if index == 10:
            break
        product_dict[os.path.join(doc_dir, "product_" + str(index) + ".png")] = price.text

    show_first_product()


def search_product(driver, product):
    if x.get() == 1:
        trendyol(driver, product)
    elif x.get() == 2:
        amazon(driver, product)
    elif x.get() == 3:
        n11(driver, product)


def search_button():
    product = textBox1.get()
    if not product == "":
        driver = webdriver.Chrome()
        driver.minimize_window()
        search_product(driver, product)


def show_product():
    img = Image.open(image_path(product_number))
    img = img.resize((190, 260), Image.ANTIALIAS)
    img_tk = ImageTk.PhotoImage(img)
    image_product.create_image(0, 0, image=img_tk, anchor=NW)
    image_product.image = img_tk
    label_product.config(text=product_dict.get(image_path(product_number)))


def back_button():
    global product_number
    product_number -= 1
    if product_number == -1:
        product_number += 1
        messagebox.showerror("Hata", "You can't move back from the first product.")
    else:
        show_product()


def next_button():
    global product_number
    product_number += 1
    if product_number == 10:
        product_number -= 1
        messagebox.showerror("Hata", "You can't search more product")
    else:
        show_product()

def buy_button():
    global product_number
    try:
        webbrowser.open(product_links[product_number])
    except:
        pass

root = Tk()
root.geometry(f'{870}x{490}')
icon_path = "pricescraper.ico"
root.iconbitmap(icon_path)
# Ekran genişliği ve yüksekliğini al
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Pencereyi ortalamak için x ve y koordinatlarını hesapla
x = (screen_width // 2) - (870 // 2)
y = (screen_height // 2) - (490 // 2)

# Pencereyi yeni koordinatlarla yeniden konumlandır
root.geometry(f'{870}x{490}+{x}+{y}')
root.resizable(False, False)

x = IntVar()

image1 = Canvas(root, bg='white')
image1.place(x=0, y=0, width=903, height=183)
image1i = Image.open("automation.png")
image1img = ImageTk.PhotoImage(image1i.resize((903, 183)))
image1.create_image(0, 0, image=image1img, anchor=NW)

textBox1 = Entry(root, fg="#4ea8f1", font=tkinter.font.Font(family="Tw Cen MT", size=12), state="normal")
textBox1.place(x=230, y=230, width=220, height=22)

label2 = Label(root, text="Enter The Product Name:", anchor='w', fg="#4ea8f1",
               font=tkinter.font.Font(family="Gill Sans MT", size=12), cursor="arrow", state="normal")
label2.place(x=20, y=230, width=200, height=22)

radio_trendyol = Radiobutton(root, text="Trendyol", value=1, anchor='w', fg="#ffaa00",
                             font=tkinter.font.Font(family="Calibri", size=9),
                             cursor="arrow", state="normal", variable=x)
radio_trendyol.place(x=60, y=280, width=110, height=32)

radio_amazon = Radiobutton(root, text="Amazon", value=2, anchor='w', fg="#ffaa00",
                           font=tkinter.font.Font(family="Calibri", size=9), cursor="arrow", state="normal", variable=x)
radio_amazon.place(x=190, y=280, width=110, height=32)

radio_n11 = Radiobutton(root, text="N11", value=3, anchor='w', fg="#ffaa00",
                        font=tkinter.font.Font(family="Calibri", size=9), cursor="arrow", state="normal", variable=x)
radio_n11.place(x=330, y=280, width=90, height=32)

image2 = Canvas(root, bg='white')
image2.place(x=60, y=310, width=110, height=67)
image2i = Image.open(r"trendyol.png")
image2img = ImageTk.PhotoImage(image2i.resize((109, 67)))
image2.create_image(0, 0, image=image2img, anchor=NW)

image2_copy = Canvas(root, bg='white')
image2_copy.place(x=190, y=310, width=110, height=66)
image2_copyi = Image.open(r"amazon.png")
image2_copyimg = ImageTk.PhotoImage(image2_copyi.resize((109, 66)))
image2_copy.create_image(0, 0, image=image2_copyimg, anchor=NW)

image2_copy_copy = Canvas(root, bg='white')
image2_copy_copy.place(x=330, y=300, width=90, height=75)
image2_copy_copyi = Image.open(r"n11.png")
image2_copy_copyimg = ImageTk.PhotoImage(image2_copy_copyi.resize((159, 98)))
image2_copy_copy.create_image(0, 0, image=image2_copy_copyimg, anchor=NW)

image_product = Canvas(root, bg='white')
image_product.place(x=540, y=185, width=190, height=260)
image_producti = Image.open(r"pricescraper.png")
image_productimg = ImageTk.PhotoImage(image_producti.resize((236, 116)))
image_product.create_image(0, 0, image=image_productimg, anchor=NW)

button_next = Button(root, text="Next", font=tkinter.font.Font(family="Bell MT", size=12),
                     cursor="arrow", state="normal")
button_next.place(x=645, y=450, width=90, height=22)
button_next['command'] = next_button

button_back = Button(root, text="Back", font=tkinter.font.Font(family="Bell MT", size=12),
                     cursor="arrow", state="normal")
button_back.place(x=535, y=450, width=90, height=22)
button_back['command'] = back_button

button_search = Button(root, text="Search!", font=tkinter.font.Font(family="Bell MT", size=12),
                       cursor="arrow", state="normal")
button_search.place(x=190, y=420, width=140, height=52)
button_search['command'] = search_button

label3 = Label(root, text="|", anchor='w', fg="#ff0000",
               font=tkinter.font.Font(family="Calibri", size=72), cursor="arrow", state="normal")
label3.place(x=490, y=180, width=30, height=82)

label4 = Label(root, text="|", anchor='w', fg="#e20003",
               font=tkinter.font.Font(family="Calibri", size=72), cursor="arrow", state="normal")
label4.place(x=490, y=210, width=30, height=82)

label5 = Label(root, text="|", anchor='w', fg="#ca3333",
               font=tkinter.font.Font(family="Calibri", size=72), cursor="arrow", state="normal")
label5.place(x=490, y=240, width=30, height=82)

label6 = Label(root, text="|", anchor='w', fg="#ac0002",
               font=tkinter.font.Font(family="Calibri", size=72), cursor="arrow", state="normal")
label6.place(x=490, y=270, width=30, height=82)

label7 = Label(root, text="|", anchor='w', fg="#960002",
               font=tkinter.font.Font(family="Calibri", size=72), cursor="arrow", state="normal")
label7.place(x=490, y=300, width=30, height=82)

label8 = Label(root, text="|", anchor='w', fg="#000000",
               font=tkinter.font.Font(family="Calibri", size=72), cursor="arrow", state="normal")
label8.place(x=490, y=330, width=30, height=82)

label9 = Label(root, text="|", anchor='w', fg="#820002",
               font=tkinter.font.Font(family="Calibri", size=72), cursor="arrow", state="normal")
label9.place(x=490, y=330, width=30, height=82)

label10 = Label(root, text="|", anchor='w', fg="#630001",
                font=tkinter.font.Font(family="Calibri", size=72), cursor="arrow", state="normal")
label10.place(x=490, y=360, width=30, height=82)

label11 = Label(root, text="|", anchor='w', fg="#420001",
                font=tkinter.font.Font(family="Calibri", size=72), cursor="arrow", state="normal")
label11.place(x=490, y=390, width=30, height=82)

label12 = Label(root, text="|", anchor='w', fg="#260000",
                font=tkinter.font.Font(family="Calibri", size=72), cursor="arrow", state="normal")
label12.place(x=490, y=420, width=30, height=82)

label13 = Label(root, text="|", anchor='w', fg="#000000",
                font=tkinter.font.Font(family="Calibri", size=72), cursor="arrow", state="normal")
label13.place(x=490, y=450, width=30, height=82)

label_product = Label(root, text="0 TL", anchor='w', fg="#00aa00", bg="#000000",
                      font=tkinter.font.Font(family="Gill Sans MT", size=16), cursor="arrow", state="normal")
label_product.place(x=755, y=220, width=110, height=22)

button_buy = Button(root, text="Buy", font=tkinter.font.Font(family="Bell MT", size=12),
                    cursor="arrow", state="normal")
button_buy.place(x=755, y=255, width=110, height=22)
button_buy['command'] = buy_button

radio_trendyol.select()

root.mainloop()
