# Author: Linpeng Mao
# Date: 11/18/2025
# Description: Handles visualization of fitness data including calories, exercise, and nutrition trends.

import os
import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils.helpers import get_user_data_path, get_nutrition_data_path, get_exercise_data_path


def show_weekly_plot(username):
    # matplotlib 画摄入/消耗/目标
    """
    Display a weekly plot of calories intake, output, and goals.
    
    :param username: The current username
    :type username: str
    :return: None
    """
    plot_window = tk.Toplevel()
    plot_window.title(f"Weekly Summary - {username}")
    plot_window.geometry("800x600")
    
    user_data_path = get_user_data_path(username)
    
    if not os.path.isfile(user_data_path):
        ttk.Label(plot_window, text="No data available for visualization").pack(padx=20, pady=20)
        return
    
    try:
        df = pd.read_csv(user_data_path)
        
        df['date'] = pd.to_datetime(df['date'])
        
        # Get data for the last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        
        if df.empty:
            ttk.Label(plot_window, text="No data available for the past 7 days").pack(padx=20, pady=20)
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(df['date'], df['calories_in'], 'b-', label='Calories In', marker='o')
        ax.plot(df['date'], df['calories_out'], 'r-', label='Calories Out', marker='x')
        ax.plot(df['date'], df['goal'], 'g--', label='Goal', marker='^')
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        
        ax.set_xlabel('Date')
        ax.set_ylabel('Calories')
        ax.set_title('Weekly Calorie Summary')
        ax.legend()
        
        ax.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        close_button = ttk.Button(plot_window, text="Close", command=plot_window.destroy)
        close_button.pack(pady=10)
        
    except Exception as e:
        ttk.Label(plot_window, text=f"Error creating visualization: {e}").pack(padx=20, pady=20)


def show_nutrition_plot(username):
    # 画营养素趋势
    pass

def show_exercise_plot(username):
    """
    Display a plot of exercise trends and calorie burn.
    
    :param username: The current username
    :type username: str
    :return: None
    """
    plot_window = tk.Toplevel()
    plot_window.title(f"Exercise Trends - {username}")
    plot_window.geometry("800x600")
    
    exercise_data_path = get_exercise_data_path(username)
    
    if not os.path.isfile(exercise_data_path):
        ttk.Label(plot_window, text="No exercise data available for visualization").pack(padx=20, pady=20)
        return
    
    try:
        df = pd.read_csv(exercise_data_path)
        
        df['date'] = pd.to_datetime(df['date'])
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        
        if df.empty:
            ttk.Label(plot_window, text="No exercise data available for the past 30 days").pack(padx=20, pady=20)
            return
        
        fig = plt.figure(figsize=(10, 8))
        
        ax1 = fig.add_subplot(211)
        
        daily_calories = df.groupby('date')['calories'].sum().reset_index()
        
        ax1.bar(daily_calories['date'], daily_calories['calories'], color='orange', alpha=0.7)
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Calories Burned')
        ax1.set_title('Daily Exercise Calories')
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        ax2 = fig.add_subplot(212)
        
        activity_data = df.groupby('activity')['duration'].sum()
        
        top_activities = activity_data.nlargest(10)
        
        ax2.pie(top_activities, labels=top_activities.index, autopct='%1.1f%%', 
                shadow=True, startangle=90)
        ax2.axis('equal')
        ax2.set_title('Exercise Activity Distribution (Last 30 Days)')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        stats_frame = ttk.Frame(plot_window)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        total_calories = df['calories'].sum()
        total_duration = df['duration'].sum()
        favorite_activity = activity_data.idxmax() if not activity_data.empty else "None"
        
        stats_text = f"Total Calories Burned: {total_calories:.1f} | "
        stats_text += f"Total Exercise Time: {total_duration:.1f} minutes | "
        stats_text += f"Favorite Activity: {favorite_activity}"
        
        ttk.Label(stats_frame, text=stats_text).pack(pady=5)
        
        close_button = ttk.Button(plot_window, text="Close", command=plot_window.destroy)
        close_button.pack(pady=10)
        
    except Exception as e:
        ttk.Label(plot_window, text=f"Error creating visualization: {e}").pack(padx=20, pady=20)