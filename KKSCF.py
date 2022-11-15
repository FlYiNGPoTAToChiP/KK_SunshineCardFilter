import os
import re as regex
import codecs
import shutil
import tkinter
from tkinter import Tk, filedialog, messagebox, ttk

path = os.getcwd()
png_list = []
png_count = 0
kks_card_list = []
kks_folder = "_KKS_card_"


def get_list(folder_path):
    new_list = []
    for (_, _, files) in os.walk(folder_path):
        for filename in files:
            if regex.match(r".*(\.png)$", filename):
                new_list.append(filename)
        return new_list


def check_png(card_path):
    with codecs.open(card_path, "rb") as card:
        data = card.read()
        card_type = 0
        if data.find(b"KoiKatuChara") != -1:
            card_type = 1
            if data.find(b"KoiKatuCharaSP") != -1:
                card_type = 2
            elif data.find(b"KoiKatuCharaSun") != -1:
                card_type = 3
        print(f"[{card_type}] {card_path}")
    return card_type


def c_get_list():
    global path, png_list, png_count, png_count_t
    b_sel['state'] = 'disabled'
    path = filedialog.askdirectory(title="Select target path (folder contain cards)", mustexist=True)

    if path:
        print(f"new path: {path}")
        os.chdir(path)
    else:
        print("no path")
        b_sel['state'] = 'normal'
        return

    png_list = get_list(path)
    png_count = len(png_list)
    png_count_t.set(f"png found: {png_count}")

    if png_count > 0:
        b_p['state'] = 'normal'
    else:
        b_p['state'] = 'disabled'

    b_sel['state'] = 'normal'


def process_png():
    global path, png_list, kks_folder, kks_card_list, window

    count = len(png_list)
    if count > 0:
        bar = ttk.Progressbar(window, maximum=count, length=250)
        bar.pack(pady=10)
        bar_val = 0
        print("0: unknown / 1: kk / 2: kksp / 3: kks")
        for png in png_list:
            if check_png(png) == 3:
                kks_card_list.append(png)
            bar_val = bar_val + 1
            bar['value'] = bar_val
            window.update()
        bar.destroy()
    else:
        messagebox.showinfo("Done", f"no PNG found")
        return

    count = len(kks_card_list)
    if count > 0:
        print(kks_card_list)

        target_folder = os.path.join(path, kks_folder)
        if not os.path.isdir(target_folder):
            os.mkdir(kks_folder)

        for card in kks_card_list:
            source = os.path.join(path, card)
            target = os.path.join(target_folder, card)
            shutil.move(source, target)

        messagebox.showinfo("Done", f"[{count}] cards move to [_KKS_card_] folder")
        kks_card_list = []
    else:
        messagebox.showinfo("Done", f"no KKS card found")


window = Tk()
# window.withdraw()
window.title("KKSCF")
w = 300
h = 300
ltx = int((window.winfo_screenwidth() - w) / 2)
lty = int((window.winfo_screenheight() - h) / 2)
window.geometry(f'{w}x{h}+{ltx}+{lty}')

tkinter.Label(window, text=" ", pady=5).pack()

b_sel = tkinter.Button(window, text="Select folder contain cards", padx=10, pady=10, relief="raised", bd=3, command=c_get_list)
b_sel.pack()

tkinter.Label(window, text=" ", pady=5).pack()

png_count_t = tkinter.StringVar()
png_count_t.set(f"png found: {png_count}")
tkinter.Label(window, textvariable=png_count_t, pady=10).pack()

tkinter.Label(window, text=" ", pady=5).pack()

b_p = tkinter.Button(window, text="Process", relief="raised", padx=10, pady=10, bd=3, command=process_png)
b_p.pack()
b_p['state'] = 'disabled'

tkinter.Label(window, text=" ", pady=5).pack()

window.mainloop()
exit(0)







