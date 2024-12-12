"""
UI components and styles for the Grade Evaluation System.
"""

import tkinter as tk
from tkinter import ttk

# Color scheme
COLORS = {
    'primary': '#1a73e8',
    'secondary': '#5f6368',
    'background': '#f8f9fa',
    'surface': '#ffffff',
    'error': '#d93025',
    'text': '#202124',
    'text_secondary': '#5f6368',
    'border': '#dadce0'
}

# Styles
STYLES = {
    'title': ('Helvetica', 24, 'bold'),
    'subtitle': ('Helvetica', 18, 'bold'),
    'body': ('Helvetica', 12),
    'body_bold': ('Helvetica', 12, 'bold'),
    'small': ('Helvetica', 10),
    'button': ('Helvetica', 12)
}

def setup_styles():
    """Setup custom styles for the application."""
    style = ttk.Style()
    
    # Configure frame styles
    style.configure('App.TFrame', background=COLORS['background'])
    style.configure('Card.TFrame', background=COLORS['surface'])
    
    # Configure label styles
    style.configure('App.TLabel', background=COLORS['background'], foreground=COLORS['text'])
    style.configure('Card.TLabel', background=COLORS['surface'], foreground=COLORS['text'])
    style.configure('Heading.TLabel', background=COLORS['surface'], foreground=COLORS['text'])
    
    # Configure button styles
    style.configure('Primary.TButton',
                   background=COLORS['primary'],
                   foreground='white',
                   padding=(20, 10))
    style.map('Primary.TButton',
              background=[('active', COLORS['primary'])])
    
    style.configure('Secondary.TButton',
                   background=COLORS['surface'],
                   foreground=COLORS['primary'],
                   padding=(20, 10))
    style.map('Secondary.TButton',
              background=[('active', COLORS['surface'])])

def create_custom_button(parent, text, command=None, style='Primary.TButton'):
    """Create a custom styled button."""
    button = ttk.Button(parent, text=text, command=command, style=style)
    return button

def create_entry(parent, width=30):
    """Create a styled entry widget."""
    entry = ttk.Entry(parent, width=width)
    return entry

def create_title_bar(parent, title):
    """Create a consistent title bar."""
    title_frame = ttk.Frame(parent, style='App.TFrame', padding=(20, 10))
    title_frame.pack(fill=tk.X, pady=(0, 20))
    
    title_label = ttk.Label(title_frame,
                           text=title,
                           font=STYLES['title'],
                           foreground=COLORS['primary'],
                           background=COLORS['background'])
    title_label.pack(anchor='w')
    
    separator = ttk.Separator(parent, orient='horizontal')
    separator.pack(fill=tk.X, padx=20)
    
    return title_frame

def create_card(parent, title=None, padding=20):
    """Create a modern card-style container."""
    card = ttk.Frame(parent, style='Card.TFrame', padding=padding)
    
    if title:
        title_label = ttk.Label(card,
                               text=title,
                               font=STYLES['subtitle'],
                               foreground=COLORS['text'],
                               background=COLORS['surface'])
        title_label.pack(anchor='w', pady=(0, 10))
    
    return card

def create_button(parent, text, command, is_primary=True):
    """Create a modern styled button."""
    style = 'Primary.TButton' if is_primary else 'Secondary.TButton'
    button = ttk.Button(parent,
                       text=text,
                       command=command,
                       style=style)
    return button

def create_treeview(parent, columns, show='headings'):
    """Create a modern styled treeview."""
    tree = ttk.Treeview(parent,
                       columns=columns,
                       show=show,
                       style='App.Treeview')
    
    # Style the headings
    for col in columns:
        tree.heading(col, text=col.title())
        tree.column(col, anchor='center')
    
    # Add scrollbars
    y_scroll = ttk.Scrollbar(parent,
                            orient='vertical',
                            command=tree.yview)
    x_scroll = ttk.Scrollbar(parent,
                            orient='horizontal',
                            command=tree.xview)
    
    tree.configure(yscrollcommand=y_scroll.set,
                  xscrollcommand=x_scroll.set)
    
    # Pack scrollbars
    tree.grid(row=0, column=0, sticky='nsew')
    y_scroll.grid(row=0, column=1, sticky='ns')
    x_scroll.grid(row=1, column=0, sticky='ew')
    
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(0, weight=1)
    
    return tree
