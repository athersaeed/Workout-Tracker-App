from tkinter import *
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import sqlite3
import random


root = Tk()
root.title("Workout Tracker")
bg_clr = '#f0f0f0'
def_font = ('Helvetica', 16)
root.configure(background=bg_clr)

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def center_window(root, width=800, height=600):
    swidth = root.winfo_screenwidth()
    sheight = root.winfo_screenheight()
    x = int((swidth/2) - (width/2))
    y = int((sheight/2) - (height/2))
    root.geometry(f"{width}x{height}+{x}+{y}")

center_window(root)

user_name = ""

def init_db():
    conn = sqlite3.connect('workout_tracker.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS weight_journey (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            week_number INTEGER,
            weight REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            name TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS exercise_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_id INTEGER,
            day_number INTEGER,
            weight REAL,
            reps INTEGER,
            FOREIGN KEY (exercise_id) REFERENCES exercises(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS cardio_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            cardio_type TEXT,
            date TEXT,
            distance REAL,
            time REAL,
            calculated_speed REAL
        )
    ''')
    #creates 2 different lists for competitors and cardio types, for each competitor, random data is 
    #for comparison graph. each cardio type data is created using random values within a parameter
    #and then inserted into the database
    c.execute("SELECT COUNT(*) FROM cardio_data WHERE user_name LIKE 'Competitor%'")
    if c.fetchone()[0] == 0:
        competitors = ['Competitor1', 'Competitor2', 'Competitor3', 'Competitor4', 'Competitor5']
        cardio_types = ['Swimming', 'Running', 'Cycling']
        for comp in competitors:
            for ctype in cardio_types:
                for j in range(5):
                    if ctype == 'Cycling':
                        dist = random.uniform(100, 120)
                        time = random.uniform(2, 4)
                    elif ctype == 'Running':
                        dist = random.uniform(100,120)
                        time = random.uniform(10,12)
                    elif ctype == 'Swimming':
                        dist = random.uniform(50, 60)
                        time = random.uniform(25, 35)
                    speed = dist / time
                    c.execute(
                        "INSERT INTO cardio_data (user_name, cardio_type, date, distance, time, calculated_speed) VALUES (?, ?, DATE('now'), ?, ?, ?)",
                        (comp, ctype, dist, time, speed)
                    )
        conn.commit()
    c.close()
    conn.close()

init_db()

def name_page():
    clear_screen()
    page = Frame(root, background=bg_clr)
    page.pack(fill="both", expand=True)

    label = ttk.Label(page, text="Welcome to Workout Tracker", font=def_font)
    label.pack(pady=10)

    name_label = ttk.Label(page, text="Please enter your name:")
    name_label.pack()
    name_entry = ttk.Entry(page, width=30)
    name_entry.pack()

    def continue_to_exercise():
        global user_name
        usrnm = name_entry.get().strip()
        if not usrnm:
            messagebox.showerror("Input Error", "Please enter your name.")
            return
        user_name = usrnm
        exercise_page()

    continue_button = ttk.Button(page, text="Continue", command=continue_to_exercise)
    continue_button.pack(pady=5)

name_page()

def exercise_page():
    clear_screen()
    ex_page = Frame(root, background=bg_clr)
    ex_page.pack(fill="both", expand=True)

    label2 = ttk.Label(ex_page, text=f"Hi {user_name}, what would you like to do today?", font=def_font)
    label2.pack(pady=20)

    button_to_weight = ttk.Button(ex_page, text="Weight Journey", command=weight_journey)
    button_to_weight.pack(pady=5)

    button_to_weight_lifting = ttk.Button(ex_page, text="Weight Lifting", command=weight_lifting)
    button_to_weight_lifting.pack(pady=5)

    button_to_cardio = ttk.Button(ex_page, text="Cardio", command=Cardio)
    button_to_cardio.pack(pady=5)

    exit_button = ttk.Button(ex_page, text="Exit", command=root.quit)
    exit_button.pack(pady=10)

    delete_data_button = ttk.Button(ex_page, text="Delete All My Data", command=delete_data)
    delete_data_button.pack(pady=10)

def delete_data():
    global user_name
    confirm = messagebox.askyesno("Delete Data", "Are you sure you want to delete all your data?")
    if confirm:
        conn = sqlite3.connect('workout_tracker.db')
        c = conn.cursor()
        try:
            c.execute("DELETE FROM cardio_data WHERE user_name=?", (user_name,))
            c.execute("DELETE FROM weight_journey WHERE user_name=?", (user_name,))
            c.execute("SELECT id FROM exercises WHERE user_name=?", (user_name,))
            exercise_ids = c.fetchall()
            for (ex_id,) in exercise_ids:
                c.execute("DELETE FROM exercise_data WHERE exercise_id=?", (ex_id,))
            c.execute("DELETE FROM exercises WHERE user_name=?", (user_name,))
            conn.commit()
            messagebox.showinfo("Data Deleted", "Your data has been deleted.")
            user_name = ""
            name_page()
        except sqlite3.Error:
            messagebox.showerror("Database Error", f"Error: {sqlite3.Error}")
        finally:
            c.close()
            conn.close()

def weight_journey():
    clear_screen()
    weight_page = Frame(root, background=bg_clr)
    weight_page.pack(fill="both", expand=True)

    conn = sqlite3.connect('workout_tracker.db')
    c = conn.cursor()
    c.execute("SELECT MAX(week_number) FROM weight_journey WHERE user_name=?", (user_name,))
    res = c.fetchone()
    last_week = res[0] if res[0] else 0
    c.close()
    conn.close()

    weekly_entries = []

    def add_week_entries():
        nonlocal last_week
        last_week += 1
        frame = Frame(weight_page, background=bg_clr)
        frame.pack(pady=5)
        label = ttk.Label(frame, text=f"Week {last_week} Weight:")
        label.pack(side=LEFT, padx=5)
        entry = ttk.Entry(frame)
        entry.pack(side=LEFT)
        weekly_entries.append((last_week, entry))

    add_week_entries()

    add_week_button = ttk.Button(weight_page, text="Add Week", command=add_week_entries)
    add_week_button.pack(pady=10)

    def save_weight_entries():
        conn = sqlite3.connect('workout_tracker.db')
        c = conn.cursor()
        try:
            for week_num, entry in weekly_entries:
                weight_str = entry.get()
                try:
                    weight = float(weight_str)
                    c.execute("INSERT INTO weight_journey (user_name, week_number, weight) VALUES (?, ?, ?)",
                            (user_name, week_num, weight))
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter valid weights.")
                    return
            conn.commit()
            messagebox.showinfo("Success", "Weight data saved.")
        except sqlite3.Error:
            messagebox.showerror("Database Error", f"Error: {sqlite3.Error}")
        finally:
            c.close()
            conn.close()

    def check_weight_progress():
        conn = sqlite3.connect('workout_tracker.db')
        c = conn.cursor()
        try:
            c.execute("SELECT week_number, weight FROM weight_journey WHERE user_name=? ORDER BY week_number", (user_name,))
            data = c.fetchall()
            if not data:
                messagebox.showerror("No Data", "No weight data found.")
                return
            weeks = [row[0] for row in data]
            weights = [row[1] for row in data]

            plt.figure(figsize=(8, 6))
            plt.plot(weeks, weights, marker='o', linestyle='-', color='b')
            plt.title("Weight Journey")
            plt.xlabel("Weeks")
            plt.ylabel("Weight")
            plt.grid(True)
            plt.show()
        except sqlite3.Error:
            messagebox.showerror("Database Error", f"Error: {sqlite3.Error}")
        finally:
            c.close()
            conn.close()

    save_button = ttk.Button(weight_page, text="Save Weight Entries", command=save_weight_entries)
    save_button.pack(pady=10)

    weight_progress_button = ttk.Button(weight_page, text="Check your Progress", command=check_weight_progress)
    weight_progress_button.pack(pady=10)

    back_button = ttk.Button(weight_page, text="Back to Main Menu", command=exercise_page)
    back_button.pack(pady=10)

def weight_lifting():
    clear_screen()
    lifting_page = Frame(root, background=bg_clr)
    lifting_page.pack(fill="both", expand=True)

    exercise_entries = {}

    def add_exercise():
        ex_name = exercise_name_entry.get().strip()
        if ex_name:
            conn = sqlite3.connect('workout_tracker.db')
            c = conn.cursor()
            try:
                c.execute("SELECT id FROM exercises WHERE user_name=? AND name=?", (user_name, ex_name))
                res = c.fetchone()
                if res:
                    ex_id = res[0]
                else:
                    c.execute("INSERT INTO exercises (user_name, name) VALUES (?, ?)", (user_name, ex_name))
                    ex_id = c.lastrowid
                    conn.commit()
            except sqlite3.Error:
                messagebox.showerror("Database Error", f"Error: {sqlite3.Error}")
                c.close()
                conn.close()
                return

            c.execute("SELECT MAX(day_number) FROM exercise_data WHERE exercise_id=?", (ex_id,))
            res = c.fetchone()
            last_day = res[0] if res[0] else 0
            c.close()
            conn.close()

            exercise_frame = Frame(lifting_page, background='#e6e6e6', relief=RIDGE, borderwidth=2)
            exercise_frame.pack(pady=10, fill=X, padx=10)

            label = ttk.Label(exercise_frame, text=f"{ex_name} - Weights and Reps", font=def_font)
            label.pack(pady=5)

            daily_entries = []

            def add_daily_entry():
                nonlocal last_day
                last_day += 1
                day_frame = Frame(exercise_frame, background=bg_clr)
                day_frame.pack(pady=5, fill=X)

                day_label = ttk.Label(day_frame, text=f"Day {last_day}:")
                day_label.pack(side=LEFT, padx=5)

                weight_entry = ttk.Entry(day_frame, width=15)
                weight_entry.pack(side=LEFT, padx=5)
                weight_entry.insert(0, "Weight")

                reps_entry = ttk.Entry(day_frame, width=15)
                reps_entry.pack(side=LEFT, padx=5)
                reps_entry.insert(0, "Reps")

                daily_entries.append((last_day, weight_entry, reps_entry))

            add_day_button = ttk.Button(exercise_frame, text="Add Day", command=add_daily_entry)
            add_day_button.pack(pady=5)

            add_daily_entry()

            def save_exercise_data():
                conn = sqlite3.connect('workout_tracker.db')
                c = conn.cursor()
                try:
                    for day_num, weight_entry, reps_entry in daily_entries:
                        weight_str = weight_entry.get()
                        reps_str = reps_entry.get()
                        try:
                            weight = float(weight_str)
                            reps = int(reps_str)
                            c.execute(
                                "INSERT INTO exercise_data (exercise_id, day_number, weight, reps) VALUES (?, ?, ?, ?)",
                                (ex_id, day_num, weight, reps)
                            )
                        except ValueError:
                            messagebox.showerror("Invalid Input", "Enter valid numbers.")
                            return
                    conn.commit()
                    messagebox.showinfo("Success", "Exercise data saved.")
                except sqlite3.Error:
                    messagebox.showerror("Database Error", f"Error: {sqlite3.Error}")
                finally:
                    c.close()
                    conn.close()

            def show_progress():
                conn = sqlite3.connect('workout_tracker.db')
                c = conn.cursor()
                try:
                    c.execute("SELECT day_number, weight, reps FROM exercise_data WHERE exercise_id=? ORDER BY day_number", (ex_id,))
                    data = c.fetchall()
                    if not data:
                        messagebox.showerror("No Data", "No exercise data found.")
                        return
                    days = [row[0] for row in data]
                    weights = [row[1] for row in data]
                    reps = [row[2] for row in data]

                    fig, ax1 = plt.subplots(figsize=(8, 6))

                    ax1.set_xlabel("Days")
                    ax1.set_ylabel("Weight", color='tab:blue')
                    ax1.plot(days, weights, marker='o', color='tab:blue')
                    ax1.tick_params(axis='y', labelcolor='tab:blue')

                    ax2 = ax1.twinx()
                    ax2.set_ylabel("Reps", color='tab:green')
                    ax2.plot(days, reps, marker='x', color='tab:green')
                    ax2.tick_params(axis='y', labelcolor='tab:green')

                    plt.title(f"Progress for {ex_name}")
                    fig.tight_layout()
                    plt.grid(True)
                    plt.show()
                except sqlite3.Error:
                    messagebox.showerror("Database Error", f"Error: {sqlite3.error}")
                finally:
                    c.close()
                    conn.close()

            save_button = ttk.Button(exercise_frame, text="Save Exercise Data", command=save_exercise_data)
            save_button.pack(pady=5)

            progress_button = ttk.Button(exercise_frame, text="Show Progress", command=show_progress)
            progress_button.pack(pady=5)

            exercise_entries[ex_name] = daily_entries
            exercise_name_entry.delete(0, END)
        else:
            messagebox.showerror("Input Error", "Enter an exercise name.")

    label = ttk.Label(lifting_page, text="Enter a new exercise name:", font=def_font)
    label.pack(pady=10)
    exercise_name_entry = ttk.Entry(lifting_page, width=30)
    exercise_name_entry.pack()

    add_exercise_button = ttk.Button(lifting_page, text="Add Exercise", command=add_exercise)
    add_exercise_button.pack(pady=10)

    back_button = ttk.Button(lifting_page, text="Back to Main Menu", command=exercise_page)
    back_button.pack(pady=10)

def Cardio():
    clear_screen()
    cardio_page = Frame(root, background=bg_clr)
    cardio_page.pack(fill="both", expand=True)

    label3 = ttk.Label(cardio_page, text="Select the type of Cardio:", font=def_font)
    label3.pack(pady=20)

    cardio_type = StringVar(value="Swimming")

    cardio_options = [("Swimming", "Swimming"), ("Running", "Running"), ("Cycling", "Cycling")]

    for text, value in cardio_options:
        ttk.Radiobutton(cardio_page, text=text, variable=cardio_type, value=value).pack(anchor=W, padx=20)

    def select_cardio():
        selected = cardio_type.get()
        if selected == "Swimming":
            swim()
        elif selected == "Running":
            run()
        elif selected == "Cycling":
            cycle()

    continue_button = ttk.Button(cardio_page, text="Continue", command=select_cardio)
    continue_button.pack(pady=10)

    back_button = ttk.Button(cardio_page, text="Back to Main Menu", command=exercise_page)
    back_button.pack(pady=10)

def swim():
    clear_screen()
    swim_page = Frame(root, background=bg_clr)
    swim_page.pack(fill="both", expand=True)

    label = ttk.Label(swim_page, text="Swimming Performance", font=def_font)
    label.pack(pady=10)

    meters_label = ttk.Label(swim_page, text="Meters swam:")
    meters_label.pack()
    meters_entry = ttk.Entry(swim_page)
    meters_entry.pack()

    time_label = ttk.Label(swim_page, text="Time in seconds:")
    time_label.pack()
    time_entry = ttk.Entry(swim_page)
    time_entry.pack()

    def compare_swim():
        try:
            meters = float(meters_entry.get())
            time = float(time_entry.get())
            if meters <= 0 or time <= 0:
                raise ValueError
            user_speed = round(meters / time, 3)

            conn = sqlite3.connect('workout_tracker.db')
            c = conn.cursor()
            try:
                c.execute(
                    "INSERT INTO cardio_data (user_name, cardio_type, date, distance, time, calculated_speed) VALUES (?, ?, DATE('now'), ?, ?, ?)",
                    (user_name, 'Swimming', meters, time, user_speed)
                )
                conn.commit()
            except sqlite3.Error:
                messagebox.showerror("Database Error", f"Error: {sqlite3.Error}")
                return

            try:
                c.execute("""
                    SELECT user_name, MAX(calculated_speed) as max_speed
                    FROM cardio_data
                    WHERE cardio_type = ? AND user_name != ?
                    GROUP BY user_name
                    ORDER BY max_speed DESC
                    LIMIT 5
                """, ('Swimming', user_name))
                top_users = c.fetchall()
            except sqlite3.Error:
                messagebox.showerror("Database Error", f"Error: {sqlite3.Error}")
                return
            finally:
                c.close()
                conn.close()

            competitors = [user_name]
            swim_data = [user_speed]
            for uname, speed in top_users:
                competitors.append(uname)
                swim_data.append(speed)

            plt.figure(figsize=(8, 6))
            colors = ['orange'] + ['blue'] * (len(swim_data) - 1)
            bars = plt.bar(competitors, swim_data, color=colors)
            plt.xlabel('Competitors')
            plt.ylabel('Speed (m/s)')
            plt.title('Swimming Speed Comparison')
            plt.grid(True, axis='y')

            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

            plt.show()
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter positive numbers.")

    compare_swim_button = ttk.Button(swim_page, text="Compare", command=compare_swim)
    compare_swim_button.pack(pady=10)

    back_button = ttk.Button(swim_page, text="Back to Cardio Options", command=Cardio)
    back_button.pack()

def run():
    clear_screen()
    run_page = Frame(root, background=bg_clr)
    run_page.pack(fill="both", expand=True)

    label = ttk.Label(run_page, text="Running Performance", font=def_font)
    label.pack(pady=10)

    meters_label = ttk.Label(run_page, text="Meters ran:")
    meters_label.pack()
    meters_entry = ttk.Entry(run_page)
    meters_entry.pack()

    time_label = ttk.Label(run_page, text="Time in seconds:")
    time_label.pack()
    time_entry = ttk.Entry(run_page)
    time_entry.pack()

    def compare_run():
        try:
            meters = float(meters_entry.get())
            time = float(time_entry.get())
            if meters <= 0 or time <= 0:
                raise ValueError
            user_speed = round(meters / time, 3)

            conn = sqlite3.connect('workout_tracker.db')
            c = conn.cursor()
            try:
                c.execute(
                    "INSERT INTO cardio_data (user_name, cardio_type, date, distance, time, calculated_speed) VALUES (?, ?, DATE('now'), ?, ?, ?)",
                    (user_name, 'Running', meters, time, user_speed)
                )
                conn.commit()
            except sqlite3.Error:
                messagebox.showerror("Database Error", f"Error: {sqlite3.Error}")
                return

            try:
                c.execute("""
                    SELECT user_name, MAX(calculated_speed) as max_speed
                    FROM cardio_data
                    WHERE cardio_type = ? AND user_name != ?
                    GROUP BY user_name
                    ORDER BY max_speed DESC
                    LIMIT 5
                """, ('Running', user_name))
                top_users = c.fetchall()
            except sqlite3.Error:
                messagebox.showerror("Database Error", f"Error: {sqlite3.Error}")
                return
            finally:
                c.close()
                conn.close()

            competitors = [user_name]
            run_data = [user_speed]
            for uname, speed in top_users:
                competitors.append(uname)
                run_data.append(speed)

            plt.figure(figsize=(8, 6))
            colors = ['orange'] + ['green'] * (len(run_data) - 1)
            bars = plt.bar(competitors, run_data, color=colors)
            plt.xlabel('Competitors')
            plt.ylabel('Speed (m/s)')
            plt.title('Running Speed Comparison')
            plt.grid(True, axis='y')

            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

            plt.show()
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter positive numbers.")

    compare_run_button = ttk.Button(run_page, text="Compare", command=compare_run)
    compare_run_button.pack(pady=10)

    back_button = ttk.Button(run_page, text="Back to Cardio Options", command=Cardio)
    back_button.pack()

def cycle():
    clear_screen()
    cycle_page = Frame(root, background=bg_clr)
    cycle_page.pack(fill="both", expand=True)

    label = ttk.Label(cycle_page, text="Cycling Performance", font=def_font)
    label.pack(pady=10)

    km_label = ttk.Label(cycle_page, text="Kilometers cycled:")
    km_label.pack()
    km_entry = ttk.Entry(cycle_page)
    km_entry.pack()

    time_label = ttk.Label(cycle_page, text="Time in hours:")
    time_label.pack()
    time_entry = ttk.Entry(cycle_page)
    time_entry.pack()

    def compare_cycle():
        try:
            km = float(km_entry.get())
            time = float(time_entry.get())
            if km <= 0 or time <= 0:
                raise ValueError
            user_speed = round(km / time, 3)

            conn = sqlite3.connect('workout_tracker.db')
            c = conn.cursor()
            try:
                c.execute(
                    "INSERT INTO cardio_data (user_name, cardio_type, date, distance, time, calculated_speed) VALUES (?, ?, DATE('now'), ?, ?, ?)",
                    (user_name, 'Cycling', km, time, user_speed)
                )
                conn.commit()
            except sqlite3.Error:
                messagebox.showerror("Database Error", f"Error: {sqlite3.Error}")
                return

            try:
                c.execute("""
                    SELECT user_name, MAX(calculated_speed) as max_speed
                    FROM cardio_data
                    WHERE cardio_type = ? AND user_name != ?
                    GROUP BY user_name
                    ORDER BY max_speed DESC
                    LIMIT 5
                """, ('Cycling', user_name))
                top_users = c.fetchall()
            except sqlite3.Error:
                messagebox.showerror("Database Error", f"Error: {sqlite3.Error}")
                return
            finally:
                c.close()
                conn.close()

            competitors = [user_name]
            cycle_data = [user_speed]
            for uname, speed in top_users:
                competitors.append(uname)
                cycle_data.append(speed)

            plt.figure(figsize=(8, 6))
            colors = ['orange'] + ['purple'] * (len(cycle_data) - 1)
            bars = plt.bar(competitors, cycle_data, color=colors)
            plt.xlabel('Competitors')
            plt.ylabel('Speed (km/h)')
            plt.title('Cycling Speed Comparison')
            plt.grid(True, axis='y')

            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

            plt.show()
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter positive numbers.")

    compare_cycle_button = ttk.Button(cycle_page, text="Compare", command=compare_cycle)
    compare_cycle_button.pack(pady=10)

    back_button = ttk.Button(cycle_page, text="Back to Cardio Options", command=Cardio)
    back_button.pack()

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

root.mainloop()
