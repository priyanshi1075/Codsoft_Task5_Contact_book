import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        self.file_name = "contacts.json"

        # Load existing contacts
        self.contacts = self.load_contacts()

        # ---------------- TITLE ----------------

        title = tk.Label(
            root,
            text="CONTACT BOOK",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=15)

        # ---------------- FORM FRAME ----------------

        form_frame = tk.LabelFrame(
            root,
            text="Contact Information",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )
        form_frame.pack(fill="x", padx=20)

        # Name
        tk.Label(
            form_frame,
            text="Name:"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        self.name_entry = tk.Entry(
            form_frame,
            width=30
        )
        self.name_entry.grid(row=0, column=1, padx=10)

        # Phone
        tk.Label(
            form_frame,
            text="Phone:"
        ).grid(row=0, column=2, padx=10, pady=8, sticky="w")

        self.phone_entry = tk.Entry(
            form_frame,
            width=30
        )
        self.phone_entry.grid(row=0, column=3, padx=10)

        # Email
        tk.Label(
            form_frame,
            text="Email:"
        ).grid(row=1, column=0, padx=10, pady=8, sticky="w")

        self.email_entry = tk.Entry(
            form_frame,
            width=30
        )
        self.email_entry.grid(row=1, column=1, padx=10)

        # Address
        tk.Label(
            form_frame,
            text="Address:"
        ).grid(row=1, column=2, padx=10, pady=8, sticky="w")

        self.address_entry = tk.Entry(
            form_frame,
            width=30
        )
        self.address_entry.grid(row=1, column=3, padx=10)

        # ---------------- BUTTONS ----------------

        button_frame = tk.Frame(root)
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="Add Contact",
            command=self.add_contact,
            width=15
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Update Contact",
            command=self.update_contact,
            width=15
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Delete Contact",
            command=self.delete_contact,
            width=15
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields,
            width=15
        ).grid(row=0, column=3, padx=5)

        # ---------------- SEARCH ----------------

        search_frame = tk.Frame(root)
        search_frame.pack(pady=10)

        tk.Label(
            search_frame,
            text="Search:"
        ).pack(side="left", padx=5)

        self.search_entry = tk.Entry(
            search_frame,
            width=35
        )
        self.search_entry.pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_contact
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Show All",
            command=self.display_contacts
        ).pack(side="left", padx=5)

        # ---------------- CONTACT TABLE ----------------

        table_frame = tk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = (
            "Name",
            "Phone",
            "Email",
            "Address"
        )

        self.contact_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        for column in columns:
            self.contact_table.heading(
                column,
                text=column
            )

        self.contact_table.column(
            "Name",
            width=160
        )

        self.contact_table.column(
            "Phone",
            width=140
        )

        self.contact_table.column(
            "Email",
            width=220
        )

        self.contact_table.column(
            "Address",
            width=250
        )

        self.contact_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.contact_table.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.contact_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.contact_table.bind(
            "<ButtonRelease-1>",
            self.select_contact
        )

        # Display existing contacts
        self.display_contacts()

    # ==========================================================
    # FILE HANDLING
    # ==========================================================

    def load_contacts(self):
        """Load contacts from JSON file."""

        if not os.path.exists(self.file_name):
            return []

        try:
            with open(
                self.file_name,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except (json.JSONDecodeError, OSError):
            return []

    def save_contacts(self):
        """Save contacts to JSON file."""

        try:
            with open(
                self.file_name,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.contacts,
                    file,
                    indent=4
                )

        except OSError:
            messagebox.showerror(
                "Error",
                "Unable to save contacts."
            )

    # ==========================================================
    # ADD CONTACT
    # ==========================================================

    def add_contact(self):
        """Add a new contact."""

        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning(
                "Missing Information",
                "Name and phone number are required."
            )
            return

        # Check duplicate phone number
        for contact in self.contacts:
            if contact["phone"] == phone:
                messagebox.showwarning(
                    "Duplicate Contact",
                    "A contact with this phone number already exists."
                )
                return

        contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        }

        self.contacts.append(contact)

        self.save_contacts()
        self.display_contacts()
        self.clear_fields()

        messagebox.showinfo(
            "Success",
            "Contact added successfully."
        )

    # ==========================================================
    # DISPLAY CONTACTS
    # ==========================================================

    def display_contacts(self):
        """Display all contacts."""

        for item in self.contact_table.get_children():
            self.contact_table.delete(item)

        for contact in self.contacts:
            self.contact_table.insert(
                "",
                "end",
                values=(
                    contact["name"],
                    contact["phone"],
                    contact["email"],
                    contact["address"]
                )
            )

    # ==========================================================
    # SEARCH CONTACT
    # ==========================================================

    def search_contact(self):
        """Search contacts by name or phone number."""

        query = self.search_entry.get().strip().lower()

        if not query:
            self.display_contacts()
            return

        for item in self.contact_table.get_children():
            self.contact_table.delete(item)

        found = False

        for contact in self.contacts:

            if (
                query in contact["name"].lower()
                or query in contact["phone"].lower()
            ):
                self.contact_table.insert(
                    "",
                    "end",
                    values=(
                        contact["name"],
                        contact["phone"],
                        contact["email"],
                        contact["address"]
                    )
                )

                found = True

        if not found:
            messagebox.showinfo(
                "Search Result",
                "No matching contact found."
            )

    # ==========================================================
    # SELECT CONTACT
    # ==========================================================

    def select_contact(self, event):
        """Load selected contact into form fields."""

        selected = self.contact_table.selection()

        if not selected:
            return

        values = self.contact_table.item(
            selected[0],
            "values"
        )

        self.clear_fields()

        self.name_entry.insert(0, values[0])
        self.phone_entry.insert(0, values[1])
        self.email_entry.insert(0, values[2])
        self.address_entry.insert(0, values[3])

    # ==========================================================
    # UPDATE CONTACT
    # ==========================================================

    def update_contact(self):
        """Update selected contact."""

        selected = self.contact_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a contact to update."
            )
            return

        old_values = self.contact_table.item(
            selected[0],
            "values"
        )

        old_phone = old_values[1]

        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning(
                "Invalid Data",
                "Name and phone number are required."
            )
            return

        for contact in self.contacts:

            if contact["phone"] == old_phone:
                contact["name"] = name
                contact["phone"] = phone
                contact["email"] = email
                contact["address"] = address
                break

        self.save_contacts()
        self.display_contacts()
        self.clear_fields()

        messagebox.showinfo(
            "Success",
            "Contact updated successfully."
        )

    # ==========================================================
    # DELETE CONTACT
    # ==========================================================

    def delete_contact(self):
        """Delete selected contact."""

        selected = self.contact_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a contact to delete."
            )
            return

        values = self.contact_table.item(
            selected[0],
            "values"
        )

        name = values[0]
        phone = values[1]

        confirmation = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {name}?"
        )

        if not confirmation:
            return

        self.contacts = [
            contact
            for contact in self.contacts
            if contact["phone"] != phone
        ]

        self.save_contacts()
        self.display_contacts()
        self.clear_fields()

        messagebox.showinfo(
            "Deleted",
            "Contact deleted successfully."
        )

    # ==========================================================
    # CLEAR FIELDS
    # ==========================================================

    def clear_fields(self):
        """Clear all input fields."""

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

        self.contact_table.selection_remove(
            self.contact_table.selection()
        )


# ==============================================================
# MAIN PROGRAM
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = ContactBook(root)

    root.mainloop()