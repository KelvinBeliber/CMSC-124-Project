import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import lexical
import syntax

class LOLCodeInterpreterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCode Interpreter")
        
        # initialize main frames
        self.create_frames()
        
        # file and text Editor
        self.create_file_explorer()
        self.create_text_editor()
        
        # Lexeme list and symbol table
        self.create_Lexemes_table()
        self.create_symbol_table()
        
        # run button and console
        self.create_run_button()
        self.create_console()
    
    def create_frames(self):
        self.file_frame = tk.Frame(self.root)
        self.file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.editor_frame = tk.Frame(self.root)
        self.editor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.console_frame = tk.Frame(self.root)
        self.console_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_file_explorer(self):
        self.file_label = tk.Label(self.file_frame, text="File: None")
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        self.browse_button = tk.Button(self.file_frame, text="Browse", command=self.load_file)
        self.browse_button.pack(side=tk.RIGHT, padx=5)
    
    def create_text_editor(self):
        self.text_editor = tk.Text(self.editor_frame, wrap="none", height=20)
        self.text_editor.pack(fill=tk.BOTH, expand=True)
    
    def create_Lexemes_table(self):
        self.Lexemes_label = tk.Label(self.bottom_frame, text="Lexemes")
        self.Lexemes_label.pack(anchor="w")
        
        self.Lexemes_tree = ttk.Treeview(self.bottom_frame, columns=("Lexeme", "Type"), show="headings")
        self.Lexemes_tree.heading("Lexeme", text="Lexeme")
        self.Lexemes_tree.heading("Type", text="Type")
        self.Lexemes_tree.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)
        
        self.Lexemes_scrollbar = tk.Scrollbar(self.bottom_frame, command=self.Lexemes_tree.yview)
        self.Lexemes_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.Lexemes_tree.configure(yscrollcommand=self.Lexemes_scrollbar.set)
    
    def create_symbol_table(self):
        self.symbol_label = tk.Label(self.bottom_frame, text="Symbol Table")
        self.symbol_label.pack(anchor="w")
        
        self.symbol_tree = ttk.Treeview(self.bottom_frame, columns=("Variable", "Value"), show="headings")
        self.symbol_tree.heading("Variable", text="Variable")
        self.symbol_tree.heading("Value", text="Value")
        self.symbol_tree.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)
        
        self.symbol_scrollbar = tk.Scrollbar(self.bottom_frame, command=self.symbol_tree.yview)
        self.symbol_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.symbol_tree.configure(yscrollcommand=self.symbol_scrollbar.set)
    
    def create_run_button(self):
        self.run_button = tk.Button(self.console_frame, text="Run", command=self.run_code)
        self.run_button.pack(fill=tk.X, padx=5, pady=5)
    
    def create_console(self):
        self.console_label = tk.Label(self.console_frame, text="Console Output")
        self.console_label.pack(anchor="w")
        
        self.console_output = tk.Text(self.console_frame, wrap="none", height=10, state=tk.DISABLED)
        self.console_output.pack(fill=tk.BOTH, expand=True)
    
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
        
        # Lexemeize the code
        Lexemes = lexical.lex(code)
        self.update_Lexemes_table(Lexemes)
        
        # parse the code
        result = syntax.syntax(code)
        self.console_output.config(state=tk.NORMAL)
        self.console_output.delete("1.0", tk.END)
        self.console_output.insert("1.0", result)
        self.console_output.config(state=tk.DISABLED)
        
        # If the syntax is correct, display visible output and update symbol table
        if isinstance(result, str) and "syntax correct" in result:
            self.console_output.insert("1.0", f"Syntax Correct\n{syntax.visible_output}\n")
            self.console_output.insert(tk.END, "------------------------\n")
            
            # Update symbol table if syntax is correct
            if hasattr(syntax, 'symbol_table'):  # Check if the symbol table is available
                self.update_symbol_table(syntax.symbol_table)
        else:
            # Display syntax errors
            self.console_output.insert("1.0", f"Syntax Errors:\n{result}")
        
        self.console_output.config(state=tk.DISABLED)
    
    def update_Lexemes_table(self, Lexemes):
        for row in self.Lexemes_tree.get_children():
            self.Lexemes_tree.delete(row)
        for Lexeme in Lexemes:
            self.Lexemes_tree.insert("", "end", values=(Lexeme[0], Lexeme[1]))
    
    def update_symbol_table(self, symbol_table):
        for row in self.symbol_tree.get_children():
            self.symbol_tree.delete(row)
        for variable, value in symbol_table.items():
            self.symbol_tree.insert("", "end", values=(variable, value))

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LOLCodeInterpreterGUI(root)
    root.mainloop()
