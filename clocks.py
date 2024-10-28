import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pytz
import ctypes
from math import sin, cos, pi, radians
import time
from typing import Dict, Any

class LuxuryWorldClock:
    def __init__(self):
        self.timezones = {
            "Mumbai": {"zone": "Asia/Kolkata", "icon": "IN"},
            "London": {"zone": "Europe/London", "icon": "🇬🇧"},
            "New York": {"zone": "America/New_York", "icon": "🇺🇸"},
            "Tokyo": {"zone": "Asia/Tokyo", "icon": "🇯🇵"},
            "Dubai": {"zone": "Asia/Dubai", "icon": "🇦🇪"},
            "Singapore": {"zone": "Asia/Singapore", "icon": "🇸🇬"},
            "Paris": {"zone": "Europe/Paris", "icon": "🇫🇷"},
            "Sydney": {"zone": "Australia/Sydney", "icon": "🇦🇺"},
            "Hong Kong": {"zone": "Asia/Hong_Kong", "icon": "🇭🇰"},
            "Frankfurt": {"zone": "Europe/Berlin", "icon": "🇩🇪"},
            "Shanghai": {"zone": "Asia/Shanghai", "icon": "🇨🇳"}
        }
        
        self.colors = {
            'bg': '#0A0F1C',
            'card_bg': '#151C2C',
            'accent1': '#00A3FF',
            'accent2': '#FF3366',
            'text': '#FFFFFF',
            'subtext': '#8899AC',
            'scrollbar': '#1E2738'
        }
        
        self.setup_root()
        self.create_widgets()
        self.setup_bindings()
        
    def setup_root(self):
        self.root = tk.Tk()
        self.root.overrideredirect(1)
        self.root.geometry("800x700")
        self.root.configure(bg=self.colors['bg'])
        self.root.attributes('-alpha', 0.95)
        
        # Create main container with padding
        self.container = tk.Frame(self.root, bg=self.colors['bg'])
        self.container.pack(expand=True, fill='both', padx=20, pady=20)
        
    def create_title_bar(self):
        title_bar = tk.Frame(self.container, bg=self.colors['bg'], height=50)
        title_bar.pack(fill='x', pady=(0, 20))
        title_bar.pack_propagate(False)
        
        title = tk.Label(title_bar, 
                        text="WORLD CLOCK PRO",
                        font=('Helvetica', 24, 'bold'),
                        bg=self.colors['bg'],
                        fg=self.colors['accent1'])
        title.pack(side='left', padx=10)
        
        settings_btn = tk.Label(title_bar,
                              text="⚙️",
                              font=('Helvetica', 20),
                              bg=self.colors['bg'],
                              fg=self.colors['accent1'],
                              cursor='hand2')
        settings_btn.pack(side='right', padx=10)
        
        close_btn = tk.Label(title_bar,
                           text="×",
                           font=('Helvetica', 24, 'bold'),
                           bg=self.colors['bg'],
                           fg=self.colors['accent2'],
                           cursor='hand2')
        close_btn.pack(side='right')
        close_btn.bind('<Button-1>', lambda e: self.root.quit())
        
    def create_widgets(self):
        self.create_title_bar()
        
        # Create main content area with two columns
        content = tk.Frame(self.container, bg=self.colors['bg'])
        content.pack(expand=True, fill='both')
        
        # Left column for scrollable time cards
        left_col = tk.Frame(content, bg=self.colors['bg'])
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Create canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(left_col, bg=self.colors['bg'], 
                              highlightthickness=0)
        scrollbar = tk.Scrollbar(left_col, orient="vertical", 
                               command=self.canvas.yview)
        
        # Configure the canvas scrolling
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg'])
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        # Create a window in the canvas for the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, 
                                anchor="nw", width=self.canvas.winfo_reqwidth())
        
        # Configure canvas to work with scrollbar
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure scrollbar style
        self.canvas.configure(bg=self.colors['bg'])
        scrollbar.configure(bg=self.colors['scrollbar'], 
                          troughcolor=self.colors['bg'],
                          activebackground=self.colors['accent1'])
        
        # Add mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Right column for analog clock and weather
        right_col = tk.Frame(content, bg=self.colors['bg'], width=300)
        right_col.pack(side='right', fill='y', padx=(10, 0))
        right_col.pack_propagate(False)
        
        # Initialize time cards
        self.time_cards = {}
        for city, info in self.timezones.items():
            card = self.create_time_card(self.scrollable_frame, city, info['icon'])
            self.time_cards[city] = card
            
        # Create analog clock
        self.create_luxury_analog_clock(right_col)
        
        # Create weather widget
        self.create_weather_widget(right_col)
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def create_time_card(self, parent, city: str, icon: str) -> Dict[str, Any]:
        card = tk.Frame(parent, bg=self.colors['card_bg'],
                       height=100, width=400)
        card.pack(pady=10, ipady=15)
        card.pack_propagate(False)
        
        card.bind('<Enter>', lambda e: self.card_hover_enter(card))
        card.bind('<Leave>', lambda e: self.card_hover_leave(card))
        
        header = tk.Frame(card, bg=self.colors['card_bg'])
        header.pack(fill='x', padx=20, pady=(10, 5))
        
        icon_label = tk.Label(header, text=icon,
                            font=('Segoe UI Emoji', 20),
                            bg=self.colors['card_bg'])
        icon_label.pack(side='left')
        
        city_label = tk.Label(header, text=city,
                            font=('Helvetica', 18, 'bold'),
                            bg=self.colors['card_bg'],
                            fg=self.colors['text'])
        city_label.pack(side='left', padx=10)
        
        time_frame = tk.Frame(card, bg=self.colors['card_bg'])
        time_frame.pack(fill='x', padx=20)
        
        time_label = tk.Label(time_frame, text="",
                            font=('Helvetica', 32, 'bold'),
                            bg=self.colors['card_bg'],
                            fg=self.colors['accent1'])
        time_label.pack(side='left')
        
        date_label = tk.Label(card, text="",
                            font=('Helvetica', 12),
                            bg=self.colors['card_bg'],
                            fg=self.colors['subtext'])
        date_label.pack(anchor='w', padx=20)
        
        return {
            'frame': card,
            'time_label': time_label,
            'date_label': date_label
        }
        
    def create_luxury_analog_clock(self, parent):
        clock_frame = tk.Frame(parent, bg=self.colors['card_bg'],
                             width=300, height=300)
        clock_frame.pack(pady=20)
        clock_frame.pack_propagate(False)
        
        self.clock_canvas = tk.Canvas(clock_frame, width=280, height=280,
                                    bg=self.colors['card_bg'], highlightthickness=0)
        self.clock_canvas.pack(pady=10)
        
        # Create luxury clock face
        self.clock_canvas.create_oval(10, 10, 270, 270,
                                    outline=self.colors['accent1'],
                                    width=2)
        
        # Add hour markers
        for i in range(12):
            angle = i * 30 - 90
            rad = radians(angle)
            # Outer edge of marker
            x1 = 140 + cos(rad) * 120
            y1 = 140 + sin(rad) * 120
            # Inner edge of marker
            x2 = 140 + cos(rad) * 110
            y2 = 140 + sin(rad) * 110
            
            if i % 3 == 0:  # Emphasize quarter hours
                width = 3
                color = self.colors['accent1']
            else:
                width = 1
                color = self.colors['subtext']
                
            self.clock_canvas.create_line(x1, y1, x2, y2,
                                        fill=color, width=width)
    
    def create_weather_widget(self, parent):
        weather_frame = tk.Frame(parent, bg=self.colors['card_bg'],
                               width=300, height=150)
        weather_frame.pack(pady=20)
        weather_frame.pack_propagate(False)
        
        # Weather title
        tk.Label(weather_frame, text="Local Weather",
                font=('Helvetica', 16, 'bold'),
                bg=self.colors['card_bg'],
                fg=self.colors['text']).pack(pady=10)
        
        # Weather icon and temperature
        weather_display = tk.Frame(weather_frame, bg=self.colors['card_bg'])
        weather_display.pack(expand=True)
        
        tk.Label(weather_display, text="🌤️",
                font=('Segoe UI Emoji', 40),
                bg=self.colors['card_bg']).pack(side='left', padx=10)
        
        tk.Label(weather_display, text="24°C",
                font=('Helvetica', 32, 'bold'),
                bg=self.colors['card_bg'],
                fg=self.colors['accent1']).pack(side='left', padx=10)
        
    def card_hover_enter(self, card):
        card.configure(bg=self.colors['bg'])
        for widget in card.winfo_children():
            widget.configure(bg=self.colors['bg'])
            for subwidget in widget.winfo_children():
                subwidget.configure(bg=self.colors['bg'])
    
    def card_hover_leave(self, card):
        card.configure(bg=self.colors['card_bg'])
        for widget in card.winfo_children():
            widget.configure(bg=self.colors['card_bg'])
            for subwidget in widget.winfo_children():
                subwidget.configure(bg=self.colors['card_bg'])
    
    def update_analog_clock(self):
        self.clock_canvas.delete("hands")
        
        now = datetime.now()
        
        # Hour hand
        hour_angle = ((now.hour % 12 + now.minute / 60) * 30 - 90) * pi / 180
        self.draw_hand(hour_angle, 80, 4, self.colors['accent1'], "hands")
        
        # Minute hand
        minute_angle = (now.minute * 6 - 90) * pi / 180
        self.draw_hand(minute_angle, 100, 3, self.colors['text'], "hands")
        
        # Second hand
        second_angle = (now.second * 6 - 90) * pi / 180
        self.draw_hand(second_angle, 110, 1, self.colors['accent2'], "hands")
        
        # Center dot
        self.clock_canvas.create_oval(137, 137, 143, 143,
                                    fill=self.colors['accent1'],
                                    tags="hands")
    
    def draw_hand(self, angle, length, width, color, tag):
        x = 140 + cos(angle) * length
        y = 140 + sin(angle) * length
        self.clock_canvas.create_line(140, 140, x, y,
                                    fill=color, width=width,
                                    tags=tag)
    
    def setup_bindings(self):
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.on_motion)
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def on_motion(self, event):
        dx = event.x_root - self.x
        dy = event.y_root - self.y
        self.root.geometry(f"+{dx}+{dy}")
    
    def update_time(self):
        now = datetime.now()
        for city, info in self.timezones.items():
            timezone = pytz.timezone(info['zone'])
            city_time = now.astimezone(timezone)
            
            # Update time
            time_str = city_time.strftime("%I:%M:%S %p")
            self.time_cards[city]['time_label'].config(text=time_str)
            
            # Update date
            date_str = city_time.strftime("%A, %B %d")
            self.time_cards[city]['date_label'].config(text=date_str)
        
        self.update_analog_clock()
        self.root.after(1000, self.update_time)
    
    def run(self):
        self.update_time()
        self.root.mainloop()

if __name__ == "__main__":
    app = LuxuryWorldClock()
    app.run()