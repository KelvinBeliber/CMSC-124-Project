import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import lexical
import syntax

class LOLCodeInterpreterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCode Interpreter")
        self.root.configure(bg="#1e1e1e")  # Dark gray background
        
        # Create main frames
        self.create_frames()
        
        # File and text editor
        self.create_file_explorer()
        self.create_text_editor()
        
        # Lexeme list and symbol table
        self.create_Lexemes_table()
        self.create_symbol_table()
        
        # Run button and console
        self.create_run_button()
        self.create_console()

    def create_frames(self):
        # Top-left for file explorer and editor
        self.file_frame = tk.Frame(self.root, bg="#2e2e2e", bd=1, relief=tk.SUNKEN)
        self.file_frame.place(relx=0, rely=0, relwidth=0.5, relheight=0.1)  # Smaller vertically
        
        self.editor_frame = tk.Frame(self.root, bg="#2e2e2e", bd=1, relief=tk.SUNKEN)
        self.editor_frame.place(relx=0, rely=0.1, relwidth=0.5, relheight=0.4)  # Below file_frame
        
        # Bottom-left for lexeme table
        self.lexemes_frame = tk.Frame(self.root, bg="#2e2e2e", bd=1, relief=tk.SUNKEN)
        self.lexemes_frame.place(relx=0, rely=0.5, relwidth=0.5, relheight=0.5)
        
        # Top-right for symbol table
        self.symbol_table_frame = tk.Frame(self.root, bg="#2e2e2e", bd=1, relief=tk.SUNKEN)
        self.symbol_table_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.5)
        
        # Bottom-right for console
        self.console_frame = tk.Frame(self.root, bg="#2e2e2e", bd=1, relief=tk.SUNKEN)
        self.console_frame.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)
    
    def create_file_explorer(self):
        self.file_label = tk.Label(self.file_frame, text="File: None", anchor="w", bg="#2e2e2e", fg="white")
        self.file_label.pack(fill=tk.X, padx=5, pady=5)
        
        self.browse_button = tk.Button(self.file_frame, text="Browse", command=self.load_file, bg="#3e3e3e", fg="white")
        self.browse_button.pack(fill=tk.X, padx=5, pady=5)
    
    def create_text_editor(self):
        self.text_editor = tk.Text(self.editor_frame, wrap="none", height=20, bg="#1e1e1e", fg="white", insertbackground="white")
        self.text_editor.pack(fill=tk.BOTH, expand=True)
    
    def create_Lexemes_table(self):
        self.Lexemes_label = tk.Label(self.lexemes_frame, text="Lexemes", bg="#2e2e2e", fg="white")
        self.Lexemes_label.pack(anchor="w")
        
        # Frame to hold Treeview and scrollbar
        treeview_frame = tk.Frame(self.lexemes_frame, bg="#2e2e2e")
        treeview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for lexemes
        self.Lexemes_tree = ttk.Treeview(treeview_frame, columns=("Lexeme", "Type"), show="headings")
        self.Lexemes_tree.heading("Lexeme", text="Lexeme")
        self.Lexemes_tree.heading("Type", text="Type")
        self.Lexemes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar on the right side
        self.Lexemes_scrollbar = tk.Scrollbar(treeview_frame, orient=tk.VERTICAL, command=self.Lexemes_tree.yview)
        self.Lexemes_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.Lexemes_tree.configure(yscrollcommand=self.Lexemes_scrollbar.set)

        # Apply dark theme to Treeview
        style = ttk.Style()
        style.configure("Treeview", background="#1e1e1e", foreground="white", fieldbackground="#1e1e1e")
        style.map("Treeview", background=[("selected", "#3e3e3e")])


    def create_symbol_table(self):
        self.symbol_table_label = tk.Label(self.symbol_table_frame, text="Symbol Table", bg="#2e2e2e", fg="white")
        self.symbol_table_label.pack(anchor="w")
        
        # Frame to hold Treeview and scrollbar
        treeview_frame = tk.Frame(self.symbol_table_frame, bg="#2e2e2e")
        treeview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for symbol table
        self.symbol_table_tree = ttk.Treeview(treeview_frame, columns=("Variable", "Value"), show="headings")
        self.symbol_table_tree.heading("Variable", text="Variable")
        self.symbol_table_tree.heading("Value", text="Value")
        self.symbol_table_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar on the right side
        self.symbol_table_scrollbar = tk.Scrollbar(treeview_frame, orient=tk.VERTICAL, command=self.symbol_table_tree.yview)
        self.symbol_table_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.symbol_table_tree.configure(yscrollcommand=self.symbol_table_scrollbar.set)

        # Apply dark theme to Treeview
        style = ttk.Style()
        style.configure("Treeview", background="#1e1e1e", foreground="white", fieldbackground="#1e1e1e")
        style.map("Treeview", background=[("selected", "#3e3e3e")])


    def create_run_button(self):
        self.run_button = tk.Button(self.console_frame, text="Run", command=self.run_code, bg="#3e3e3e", fg="white")
        self.run_button.pack(fill=tk.X, padx=5, pady=5)
    
    def create_console(self):
        self.console_label = tk.Label(self.console_frame, text="Console Output", bg="#2e2e2e", fg="white")
        self.console_label.pack(anchor="w")
        
        self.console_output = tk.Text(self.console_frame, wrap="none", height=10, bg="#1e1e1e", fg="white", insertbackground="white", state=tk.DISABLED)
        self.console_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("LOLCode Files", "*.lol")])
        if filepath:
            with open(filepath, "r") as file:
                content = file.read()
            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert("1.0", content)
            self.file_label.config(text=f"File: {filepath}")
    
    def run_code(self):
        code = self.text_editor.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("No Code", "Please write or load code to run.")
            return
        
        Lexemes = lexical.lex(code)
        self.update_Lexemes_table(Lexemes)
        
        # Get console output and symbol table from syntax module
        console_output, symbol_table = syntax.syntax(code)
        
        # Update the console
        self.console_output.config(state=tk.NORMAL)
        self.console_output.delete("1.0", tk.END)
        self.console_output.insert("1.0", console_output)
        self.console_output.config(state=tk.DISABLED)
        
        # Update the symbol table
        self.update_symbol_table(symbol_table)

    def update_Lexemes_table(self, Lexemes):
        for row in self.Lexemes_tree.get_children():
            self.Lexemes_tree.delete(row)
        for Lexeme in Lexemes:
            self.Lexemes_tree.insert("", "end", values=(Lexeme[0], Lexeme[1]))

    def update_symbol_table(self, symbol_table):
        # Clear existing content
        for row in self.symbol_table_tree.get_children():
            self.symbol_table_tree.delete(row)
        # Add new data
        print(symbol_table)
        for variable in symbol_table:
            value = symbol_table[variable]
            self.symbol_table_tree.insert("", "end", values=(variable, value))

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # Set a reasonable size
    app = LOLCodeInterpreterGUI(root)
    root.mainloop()
