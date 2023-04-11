from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from secure import SecurePassword
from db import DataBase
import pyperclip

class Window:
    db  = DataBase()
    
    def __init__(self):
        # Create a Main Frame
        TITLE = "Password Manager"
        root = Tk()
        root.title(TITLE)
        root.geometry("900x500")
        # root.state("zoomed")

        label_font = ("Cambria", 16)
        entry_font = ('Helvetica', 12)

        self.main_frame = Frame(root)
        self.main_frame.configure()
        self.main_frame.pack(fill=BOTH, expand=True)

        # Title
        self.heading = Label(self.main_frame, text="PASSWORD MANAGER")
        self.heading.configure(font="-family {Cambria} -size 28")
        self.heading.pack(fill=X)

        # Dividing Main Frame in to 2 equal halves

        # Left Frame for Entry boxes and Buttons
        self.left_frame = Frame(self.main_frame)
        self.left_frame.configure()
        self.left_frame.pack(fill=BOTH, expand=True, side=LEFT)

        # Right Frame for Tree View
        self.right_frame = Frame(self.main_frame)
        self.right_frame.configure()
        self.right_frame.pack(fill=BOTH, expand=True, side=LEFT)

        # Manager Frame for Entry Box and Labels
        self.manager_frame = Frame(self.left_frame)
        self.manager_frame.configure()
        self.manager_frame.pack(fill=BOTH, expand=True, pady=60)

        # Name Frame for Site name and entry
        self.name_frame = Frame(self.manager_frame)
        self.name_frame.configure()
        self.name_frame.pack(fill=BOTH, expand=True)

        self.name_label = Label(self.name_frame, text="SITENAME")
        self.name_label.configure(font=label_font, width=10)
        self.name_label.pack(fill=X, expand=True, side=LEFT, padx=20)

        self.name_entry = ttk.Entry(self.name_frame)
        self.name_entry.configure(font=entry_font, width=10)
        self.name_entry.pack(fill=X, expand=True, side=LEFT, padx=20)

        # Pass Frame for password name and entry
        self.pass_frame = Frame(self.manager_frame)
        self.pass_frame.configure()
        self.pass_frame.pack(fill=BOTH, expand=True)

        self.pass_label = Label(self.pass_frame, text="PASSWORD")
        self.pass_label.configure(font=label_font, width=10)
        self.pass_label.pack(fill=X, expand=True, side=LEFT, padx=20)

        self.pass_entry = ttk.Entry(self.pass_frame)
        self.pass_entry.configure(font=entry_font, width=10, show="*")
        self.pass_entry.pack(fill=X, expand=True, side=LEFT, padx=20)

        # Button Frame
        self.button_frame = Frame(self.manager_frame)
        self.button_frame.configure()
        self.button_frame.pack(fill=BOTH, expand=True)

        # Creating Buttons
        style = ttk.Style()
        style.configure('my.TButton', font=('Helvetica', 14))

        self.add_button = ttk.Button(self.button_frame, text="ADD", style='my.TButton')
        self.add_button.configure(cursor="hand2", width=10, command=self.check_password)
        self.add_button.pack(expand=True, side=LEFT)

        self.update_button = ttk.Button(self.button_frame, text="UPDATE", style='my.TButton')
        self.update_button.configure(cursor="hand2", width=10, command=self.update)
        self.update_button.pack(expand=True, side=LEFT)

        self.delete_button = ttk.Button(self.button_frame, text="DELETE", style='my.TButton')
        self.delete_button.configure(cursor="hand2", width=10, command=self.delete_record)
        self.delete_button.pack(expand=True, side=LEFT)

        self.search_button = ttk.Button(self.button_frame, text="SEARCH", style='my.TButton')
        self.search_button.configure(cursor="hand2", width=10, command=self.search)
        self.search_button.pack(expand=True, side=LEFT)

        # Creating Treeview
        columns = ('SrNo', 'Sitename', 'Password')

        self.tree = ttk.Treeview(self.right_frame, columns=columns, show='headings')
        self.tree.configure(selectmode="extended")

        style.theme_use("clam")
        style.configure('Treeview.Heading', font="-family {Cambria} -size 13")

        self.tree.heading('SrNo', text="SrNo", anchor=W)
        self.tree.heading('Sitename', text='Sitename', anchor=W)
        self.tree.heading('Password', text='Password', anchor=W)

        self.tree.column("#1", minwidth=50, stretch=NO, width=100)
        self.tree.column("#2", minwidth=50, stretch=YES, width=100)
        self.tree.column("#3", minwidth=50, stretch=YES, width=100)

        self.tree.pack(expand=True, fill=BOTH, side=LEFT, pady=80, padx=20)

        self.display_data()
        # scrollbar = ttk.Scrollbar(self.right_frame, orient=VERTICAL, command=tree.yview)
        # tree.configure(yscrollcommand=scrollbar.set)
        # scrollbar.pack(fill=Y, expand=True, side=RIGHT)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.on_click)

        root.mainloop()

    sel = []

    def on_tree_select(self, event=None):
        self.sel.clear()
        for i in self.tree.selection():
            if i not in self.sel:
                self.sel.append(i)

    def display_data(self):
        self.tree.delete(*self.tree.get_children())
        records = self.db.show_record()
        for record in records:
            self.tree.insert("", END, values=record)

    def add_record(self):
        name = self.name_entry.get()
        password = self.pass_entry.get()

        if name and password:
            get_srno = self.db.get_srno()
            srno = get_srno+1

            s = SecurePassword()
            s_pass = s.encrypt_message(password)
            
            try:
                self.db.insert_record(srno, name, s_pass)
                messagebox.showinfo("Success!!", "Record Inserted Successfully!!", parent=self.main_frame)
                self.clear()
                self.display_data()
            except:
                messagebox.showerror("Error", "Something went wrong", parent=self.main_frame)
        else:
            messagebox.showerror("Error", "Fields are empty", parent=self.main_frame)

    def delete_record(self):
        val = []
        if len(self.sel) != 0:
            sure = messagebox.askyesno("Sure", "Are you sure you want to delete ?", parent=self.main_frame)
            if sure:
                for i in self.sel:
                    for j in self.tree.item(i)["values"]:
                        val.append(j)

                for j in range(len(val)):
                    if j%3 == 0:
                        try:
                            self.db.delete_record(val[j])
                            self.db.serialize()
                            self.display_data()
                        except:
                            messagebox.showerror("Error", "Oops!!, Something went wrong", parent=self.main_frame)
                            return

                messagebox.showinfo("Success!!", "Record Deleted Successfully", parent=self.main_frame)
                
        else:
            messagebox.showwarning("Oops!!", "Select atleast one record to delete", parent=self.main_frame)

    def check_password(self):
        self.validation = tk.Toplevel()
        self.validation.title("Re-Type Password")
        self.validation.geometry("200x200")
        self.validation.resizable(False, False)
        self.validation.grab_set()

        self.validaton_frame = Frame(self.validation)
        self.validaton_frame.pack(fill=BOTH, expand=True, pady=40)

        self.label = Label(self.validaton_frame, text="RE-TYPE PASSWORD")
        self.label.configure(font="-family {Cambria} -size 14")
        self.label.pack(fill=X, expand=True)

        self.entry = ttk.Entry(self.validaton_frame)
        self.entry.configure(font="-family {Helvetica} -size 12", show="*")
        self.entry.pack(fill=X, expand=True, padx=20)

        self.button = ttk.Button(self.validaton_frame, text="SUBMIT", style='my.TButton')
        self.button.configure(cursor="hand2", width=10, command=self.submit)
        self.button.pack(expand=True)

        self.validation.mainloop()

    def submit(self):
        if self.entry.get() == self.pass_entry.get():
            self.add_record()
            self.validation.destroy()
        else:
            messagebox.showerror("Error", "Wrong password, Try again", parent=self.validaton_frame)

    def search(self):
        key = self.name_entry.get()
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)
        for search in val:
            if search == key:
                self.tree.selection_set(val[val.index(search) - 2])
                self.tree.focus(val[val.index(search) - 2])
                ask = messagebox.askyesno("Success!!", "Search found, Do you want to copy ?", parent=self.main_frame)
                if ask:
                    self.copy_password(val[val.index(search)-1])
                break
        else:
            messagebox.showwarning("Oops!", "Bill not found", parent=self.main_frame)

    def update(self):
        name = self.name_entry.get()
        password = self.pass_entry.get()

        if name and password:
            s = SecurePassword()
            s_pass = s.encrypt_message(password)

            val = []
            if len(self.sel) != 0:
                for i in self.sel:
                    for j in self.tree.item(i)["values"]:
                        val.append(j)

                for j in range(len(val)):
                    if j%3 == 0:
                        try:
                            self.db.update_record(val[j], name, s_pass)
                            self.clear()
                            self.display_data()
                        except:
                            messagebox.showerror("Error", "Oops!, Something went wrong", parent=self.main_frame)
                            return
                messagebox.showinfo("Success!!", "Record Updated Successfully", parent=self.main_frame)
        else:
            messagebox.showerror("Error", "Some fields are empty", parent=self.main_frame)

    def on_click(self, event=None):
        self.clear()
        val = []
        for i in self.sel:
            for j in self.tree.item(i)["values"]:
                val.append(j)

        for j in range(len(val)):
            if j%3 == 0:
                self.name_entry.insert('insert', val[j+1])

    def clear(self):
        self.name_entry.delete(0, END)
        self.pass_entry.delete(0, END)

    def copy_password(self, srno):
        fetch = self.db.specific_record(srno)
        s = SecurePassword()
        myPass = s.decrypt_message(fetch[0][2])
        pyperclip.copy(myPass)


def main():
    w = Window()
    
if __name__ == '__main__':
    main()