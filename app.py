# from flask import Flask, render_template, request, redirect, url_for
# import datetime
# import matplotlib.pyplot as plt
# import pandas as pd
# import os

# app = Flask(__name__)

# # Workout split data
# workout_plan = {
#     1: 'Legs (Quad Focus) + Abs',
#     2: 'Shoulders + Triceps',
#     3: 'Back + Biceps',
#     4: 'Legs (Hamstring/Glute Focus) + Abs',
#     5: 'Shoulders + Chest',
#     6: 'Back + Arms',
#     7: 'Rest or Active Recovery'
# }

# # Initial state for user data
# workout_progress = []
# bodyweight_data = []

# # Helper to get the current day in the cycle
# def get_current_day():
#     today = len(workout_progress) % 7 + 1
#     return today

# @app.route('/')
# def home():
#     current_day = get_current_day()
#     current_plan = workout_plan[current_day]
#     return render_template('index.html', day=current_day, plan=current_plan)

# @app.route('/done', methods=['POST'])
# def mark_done():
#     workout_progress.append(datetime.datetime.now())
#     return redirect(url_for('home'))

# @app.route('/track_weight', methods=['POST'])
# def track_weight():
#     weight = float(request.form['weight'])
#     bodyweight_data.append({'date': datetime.datetime.now(), 'weight': weight})
#     return redirect(url_for('home'))

# @app.route('/view_weight')
# def view_weight():
#     df = pd.DataFrame(bodyweight_data)
#     if not df.empty:
#         df['date'] = pd.to_datetime(df['date'])
#         df.set_index('date', inplace=True)
#         plt.figure()
#         df['weight'].plot()
#         plt.ylabel('Weight')
#         plt.savefig('static/weight_graph.png')
#     return render_template('view_weight.html')

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for
import datetime
import matplotlib.pyplot as plt
import os
import pandas as pd

app = Flask(__name__)

# Workout split data
workout_plan = {
    1: {
        "title": "Legs (Quad Focus) + Abs",
        "exercises": [
            ("Squats", "4 sets x 6-8 reps"),
            ("Leg Press", "4 sets x 8-12 reps"),
            ("Bulgarian Split Squats", "3 sets x 10-12 reps"),
            ("Leg Extensions", "4 sets x 10-15 reps"),
            ("Calf Raises", "4 sets x 12-15 reps"),
            ("Ab Circuit", "3 sets (Planks, Leg Raises, Russian Twists)")
        ]
    },
    2: {
        "title": "Shoulders + Triceps",
        "exercises": [
            ("Overhead Barbell Press", "4 sets x 6-8 reps"),
            ("Dumbbell Lateral Raises", "4 sets x 12-15 reps"),
            ("Cable Face Pulls", "3 sets x 12-15 reps"),
            ("Dumbbell Front Raises", "3 sets x 10-12 reps"),
            ("Barbell Shrugs", "4 sets x 8-12 reps"),
            ("Tricep Dips", "4 sets x 8-12 reps"),
            ("Skull Crushers", "3 sets x 10-12 reps")
        ]
    },
    3: {
        "title": "Back + Biceps",
        "exercises": [
            ("Deadlifts", "4 sets x 5-6 reps"),
            ("Pull-ups (or Lat Pulldown)", "4 sets x 8-10 reps"),
            ("Barbell Rows", "4 sets x 6-8 reps"),
            ("T-Bar Rows", "3 sets x 8-10 reps"),
            ("Dumbbell Curls", "4 sets x 8-10 reps"),
            ("Hammer Curls", "3 sets x 10-12 reps")
        ]
    },
    4: {
        "title": "Legs (Hamstring/Glute Focus) + Abs",
        "exercises": [
            ("Romanian Deadlifts", "4 sets x 6-8 reps"),
            ("Leg Curls", "4 sets x 8-12 reps"),
            ("Walking Lunges", "3 sets x 12-15 reps"),
            ("Hip Thrusts", "4 sets x 8-12 reps"),
            ("Standing Calf Raises", "4 sets x 12-15 reps"),
            ("Ab Circuit", "3 sets (Crunches, Bicycle Kicks, Toe Touches)")
        ]
    },
    5: {
        "title": "Shoulders + Chest",
        "exercises": [
            ("Dumbbell Shoulder Press", "4 sets x 6-8 reps"),
            ("Dumbbell Lateral Raises", "4 sets x 12-15 reps"),
            ("Cable Lateral Raises", "3 sets x 12-15 reps"),
            ("Incline Bench Press", "4 sets x 6-8 reps"),
            ("Flat Dumbbell Bench Press", "4 sets x 8-10 reps"),
            ("Chest Flyes", "3 sets x 12-15 reps")
        ]
    },
    6: {
        "title": "Back + Arms",
        "exercises": [
            ("Pull-ups (Weighted if possible)", "4 sets x 6-8 reps"),
            ("Seated Cable Rows", "4 sets x 8-10 reps"),
            ("Lat Pulldown", "3 sets x 8-12 reps"),
            ("Preacher Curls", "4 sets x 8-10 reps"),
            ("Concentration Curls", "3 sets x 12 reps"),
            ("Close-Grip Bench Press", "4 sets x 8-10 reps"),
            ("Tricep Pushdowns", "3 sets x 10-12 reps")
        ]
    },
    7: {
        "title": "Rest or Active Recovery",
        "exercises": []
    }
}

# Store weights for exercises
exercise_weights = {}

# Initial state for user data
workout_progress = []
bodyweight_data = []

# Helper to get the current day in the cycle
def get_current_day():
    today = len(workout_progress) % 7 + 1
    return today

@app.route('/')
def home():
    current_day = get_current_day()
    current_plan = workout_plan[current_day]
    return render_template('index.html', day=current_day, plan=current_plan)

@app.route('/done', methods=['POST'])
def mark_done():
    workout_progress.append(datetime.datetime.now())
    return redirect(url_for('home'))

@app.route('/track_bodyweight', methods=['POST'])
def track_bodyweight():
    weight = float(request.form['weight'])
    bodyweight_data.append({'date': datetime.datetime.now(), 'weight': weight})
    return redirect(url_for('home'))

@app.route('/view_weight')
def view_weight():
    df = pd.DataFrame(bodyweight_data)
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        plt.figure()
        df['weight'].plot()
        plt.title('Your journey so far...')
        plt.ylabel('Weight (kgs)')
        plt.savefig('static/weight_graph.png')
    return render_template('view_weight.html')

@app.route('/track_weight/<exercise>', methods=['POST'])
def track_weight(exercise):
    weight = request.form['weight']
    date = datetime.datetime.now().date()
    
    if exercise not in exercise_weights:
        exercise_weights[exercise] = []
    
    exercise_weights[exercise].append((date, float(weight)))
    return redirect(url_for('home'))

@app.route('/view_graph/<exercise>', methods=['GET'])
def view_graph(exercise):
    weights = exercise_weights.get(exercise, [])
    
    if weights:
        dates, values = zip(*weights)
        plt.figure(figsize=(10, 5))
        plt.plot(dates, values, marker='o')
        plt.title(f'Weights Lifted for {exercise}')
        plt.xlabel('Date')
        plt.ylabel('Weight (kgs)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'static/{exercise}_graph.png')
        plt.close()
    
    return redirect(url_for('show_graph', exercise=exercise))

@app.route('/show_graph/<exercise>', methods=['GET'])
def show_graph(exercise):
    return render_template('show_graph.html', exercise=exercise)

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
