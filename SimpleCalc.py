import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)
        
        # Variables
        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.should_reset_display = False
        
        # Create GUI
        self.create_widgets()
        
        # Bind keyboard events
        self.bind_keys()
        
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a2e', padx=20, pady=20)
        main_frame.pack()
        
        # Display frame
        display_frame = tk.Frame(main_frame, bg='#0f0f1e', relief=tk.SUNKEN, bd=2)
        display_frame.pack(pady=(0, 20), fill=tk.BOTH, expand=True)
        
        # Operation display (small text showing current operation)
        self.operation_label = tk.Label(
            display_frame, 
            text="", 
            bg='#0f0f1e', 
            fg='#888888',
            font=('Courier New', 12),
            anchor='e',
            padx=10,
            pady=5
        )
        self.operation_label.pack(fill=tk.X)
        
        # Main display
        self.display = tk.Label(
            display_frame,
            text="0",
            bg='#0f0f1e',
            fg='#00ff88',
            font=('Courier New', 36, 'bold'),
            anchor='e',
            padx=10,
            pady=10
        )
        self.display.pack(fill=tk.X)
        
        # Keyboard shortcuts info frame
        info_frame = tk.Frame(main_frame, bg='#1a1a2e')
        info_frame.pack(pady=(0, 10))
        
        #  info_text = "Keyboard: Backspace=Erase | Delete/C=Clear | P=Power | S=√ | A=|x| | Enter==Calculate"
        info_label = tk.Label(
            info_frame,
            #text=info_text,
            bg='#1a1a2e',
            fg='#888888',
            font=('Segoe UI', 9)
        )
        info_label.pack()
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#1a1a2e')
        buttons_frame.pack()
        
        # Button layout (added ← for backspace/erase)
        buttons = [
            ['←', '|x|', 'x^y', '÷', 'C'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '√', '=']
        ]
        
        # Create buttons
        for row_idx, row in enumerate(buttons):
            for col_idx, text in enumerate(row):
                # Determine button properties
                if text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
                    bg_color = '#3a3a4e'
                    fg_color = 'white'
                    hover_color = '#4a4a5e'
                elif text in ['+', '-', '×', '÷']:
                    bg_color = '#ff6b6b'
                    fg_color = 'white'
                    hover_color = '#ff5252'
                elif text == 'C':
                    bg_color = '#feca57'
                    fg_color = '#1a1a2e'
                    hover_color = '#feb947'
                elif text == '←':  # Backspace/erase button
                    bg_color = '#ff9f43'
                    fg_color = '#1a1a2e'
                    hover_color = '#ff8f33'
                elif text == '=':
                    bg_color = '#00ff88'
                    fg_color = '#1a1a2e'
                    hover_color = '#00dd77'
                else:  # Special functions
                    bg_color = '#4ecdc4'
                    fg_color = 'white'
                    hover_color = '#3dbdb4'
                
                # Special handling for 0 and = buttons (they span 2 columns)
                colspan = 2 if text in ['0', '='] else 1
                
                # Adjust width for 5-column layout in first row
                if row_idx == 0:
                    btn_width = 5
                else:
                    btn_width = 5 if colspan == 1 else 11
                
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    bg=bg_color,
                    fg=fg_color,
                    font=('Segoe UI', 16, 'bold'),
                    width=btn_width,
                    height=2,
                    relief=tk.FLAT,
                    command=lambda t=text: self.button_click(t)
                )
                
                # Position button
                if text == '0':
                    btn.grid(row=row_idx, column=col_idx, columnspan=2, padx=5, pady=5)
                elif text == '=':
                    btn.grid(row=row_idx, column=col_idx, columnspan=2, padx=5, pady=5)
                elif text != '.':  # Skip the dot position when 0 spans 2 columns
                    if row_idx == 4 and col_idx > 0:
                        actual_col = col_idx + 1 if col_idx == 1 else col_idx
                        btn.grid(row=row_idx, column=actual_col, padx=5, pady=5)
                    else:
                        btn.grid(row=row_idx, column=col_idx, padx=5, pady=5)
                
                # Bind hover effects
                btn.bind('<Enter>', lambda e, b=btn, c=hover_color: b.config(bg=c))
                btn.bind('<Leave>', lambda e, b=btn, c=bg_color: b.config(bg=c))
    
    def bind_keys(self):
        """Bind all keyboard shortcuts"""
        # Numbers
        for i in range(10):
            self.root.bind(str(i), lambda e, n=str(i): self.append_number(n))
        
        # Decimal point
        self.root.bind('.', lambda e: self.append_decimal())
        self.root.bind(',', lambda e: self.append_decimal())  # Alternative decimal
        
        # Basic operations
        self.root.bind('+', lambda e: self.append_operator('+'))
        self.root.bind('-', lambda e: self.append_operator('-'))
        self.root.bind('*', lambda e: self.append_operator('*'))
        self.root.bind('/', lambda e: self.append_operator('/'))
        
        # Power (P or ^)
        self.root.bind('p', lambda e: self.power())
        self.root.bind('P', lambda e: self.power())
        self.root.bind('^', lambda e: self.power())
        
        # Square root (S or R)
        self.root.bind('s', lambda e: self.square_root())
        self.root.bind('S', lambda e: self.square_root())
        self.root.bind('r', lambda e: self.square_root())
        self.root.bind('R', lambda e: self.square_root())
        
        # Absolute value (A)
        self.root.bind('a', lambda e: self.absolute())
        self.root.bind('A', lambda e: self.absolute())
        
        # Calculate (Enter or =)
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('=', lambda e: self.calculate())
        
        # Clear (C, Delete, or Escape)
        self.root.bind('c', lambda e: self.clear_display())
        self.root.bind('C', lambda e: self.clear_display())
        self.root.bind('<Escape>', lambda e: self.clear_display())
        self.root.bind('<Delete>', lambda e: self.clear_display())
        
        # Backspace/Erase
        self.root.bind('<BackSpace>', lambda e: self.backspace())
    
    def update_display(self):
        self.display.config(text=self.current_input)
        if self.operation and self.previous_input:
            op_symbol = {
                '*': '×',
                '/': '÷',
                '+': '+',
                '-': '-',
                '^': '^'
            }.get(self.operation, self.operation)
            self.operation_label.config(text=f"{self.previous_input} {op_symbol}")
        else:
            self.operation_label.config(text="")
    
    #Button Click Operation
    def button_click(self, value):
        if value == 'C':
            self.clear_display()
        elif value == '←':
            self.backspace()
        elif value in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.append_number(value)
        elif value == '.':
            self.append_decimal()
        elif value in ['+', '-', '×', '÷']:
            op_map = {'×': '*', '÷': '/'}
            self.append_operator(op_map.get(value, value))
        elif value == 'x^y':
            self.power()
        elif value == '√':
            self.square_root()
        elif value == '|x|':
            self.absolute()
        elif value == '=':
            self.calculate()
    
    def clear_display(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operation = None
        self.should_reset_display = False
        self.update_display()
    
    def backspace(self):
        """Remove the last character from current input"""
        if self.should_reset_display:
            return
        
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
        
        self.update_display()
    
    def append_number(self, num):
        if self.should_reset_display:
            self.current_input = "0"
            self.should_reset_display = False
        
        if self.current_input == "0":
            self.current_input = num
        else:
            # Limit display length to prevent overflow
            if len(self.current_input) < 12:
                self.current_input += num
        self.update_display()
    
    def append_decimal(self):
        if self.should_reset_display:
            self.current_input = "0"
            self.should_reset_display = False
        
        if '.' not in self.current_input:
            self.current_input += '.'
            self.update_display()
    
    def append_operator(self, op):
        if self.operation and not self.should_reset_display:
            self.calculate()
        self.previous_input = self.current_input
        self.operation = op
        self.should_reset_display = True
        self.update_display()
    
    def calculate(self):
        if not self.operation or not self.previous_input:
            return
        
        try:
            prev = float(self.previous_input)
            current = float(self.current_input)
            
            if self.operation == '+':
                result = prev + current
            elif self.operation == '-':
                result = prev - current
            elif self.operation == '*':
                result = prev * current
            elif self.operation == '/':
                if current == 0:
                    messagebox.showerror("Error", "Cannot divide by zero!")
                    return
                result = prev / current
            elif self.operation == '^':
                result = math.pow(prev, current)
            
            # Format result
            if result == int(result):
                self.current_input = str(int(result))
            else:
                # Limit decimal places
                self.current_input = f"{result:.8g}"
            
            self.operation = None
            self.previous_input = ""
            self.should_reset_display = True
            self.update_display()
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def power(self):
        if self.current_input != "0":
            self.append_operator('^')
    
    def square_root(self):
        try:
            current = float(self.current_input)
            if current < 0:
                messagebox.showerror("Error", "Cannot calculate square root of negative number!")
                return
            result = math.sqrt(current)
            
            if result == int(result):
                self.current_input = str(int(result))
            else:
                self.current_input = f"{result:.8g}"
            
            self.should_reset_display = True
            self.update_display()
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def absolute(self):
        try:
            current = float(self.current_input)
            result = abs(current)
            
            if result == int(result):
                self.current_input = str(int(result))
            else:
                self.current_input = f"{result:.8g}"
            
            self.should_reset_display = True
            self.update_display()
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")


def main():
    root = tk.Tk()
    calculator = Calculator(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()