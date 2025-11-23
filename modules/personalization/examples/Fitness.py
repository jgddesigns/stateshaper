


class Fitness:



    def __init__(self, **kwargs):
        super(Fitness, self).__init__(**kwargs)

        self.ratings = {"health": 0, "composition": 0, "stress": 0, "strength": 0, "lifestyle": 0}

       
        self.questions = {

            1: {
                "question": "How many days per week do you currently exercise?",
                "choices": {
                    "A": {
                        "text": "0–1 days",
                        "scores": {"health": 2, "composition": 1, "stress": 1, "strength": 1, "lifestyle": 2}
                    },
                    "B": {
                        "text": "2–3 days",
                        "scores": {"health": 5, "composition": 4, "stress": 5, "strength": 4, "lifestyle": 5}
                    },
                    "C": {
                        "text": "4–5 days",
                        "scores": {"health": 8, "composition": 7, "stress": 7, "strength": 7, "lifestyle": 8}
                    },
                    "D": {
                        "text": "6–7 days",
                        "scores": {"health": 10, "composition": 9, "stress": 8, "strength": 9, "lifestyle": 10}
                    }
                },
                "response": None
            },

            2: {
                "question": "What type of training do you prefer?",
                "choices": {
                    "A": {
                        "text": "Strength training",
                        "scores": {"health": 6, "composition": 8, "stress": 4, "strength": 10, "lifestyle": 5}
                    },
                    "B": {
                        "text": "Cardio",
                        "scores": {"health": 9, "composition": 5, "stress": 6, "strength": 4, "lifestyle": 7}
                    },
                    "C": {
                        "text": "HIIT",
                        "scores": {"health": 8, "composition": 7, "stress": 5, "strength": 8, "lifestyle": 6}
                    },
                    "D": {
                        "text": "Yoga / mobility",
                        "scores": {"health": 5, "composition": 3, "stress": 10, "strength": 3, "lifestyle": 8}
                    }
                },
                "response": None
            },

            3: {
                "question": "What motivates you the most to work out?",
                "choices": {
                    "A": {
                        "text": "Appearance",
                        "scores": {"health": 2, "composition": 10, "stress": 3, "strength": 4, "lifestyle": 3}
                    },
                    "B": {
                        "text": "Performance",
                        "scores": {"health": 4, "composition": 5, "stress": 4, "strength": 10, "lifestyle": 5}
                    },
                    "C": {
                        "text": "Stress relief",
                        "scores": {"health": 5, "composition": 3, "stress": 10, "strength": 3, "lifestyle": 6}
                    },
                    "D": {
                        "text": "Long-term health",
                        "scores": {"health": 10, "composition": 4, "stress": 6, "strength": 4, "lifestyle": 7}
                    }
                },
                "response": None
            },

            4: {
                "question": "How long are your typical workouts?",
                "choices": {
                    "A": {
                        "text": "Under 20 minutes",
                        "scores": {"health": 3, "composition": 2, "stress": 4, "strength": 2, "lifestyle": 4}
                    },
                    "B": {
                        "text": "20–40 minutes",
                        "scores": {"health": 6, "composition": 5, "stress": 6, "strength": 5, "lifestyle": 6}
                    },
                    "C": {
                        "text": "40–60 minutes",
                        "scores": {"health": 8, "composition": 7, "stress": 7, "strength": 7, "lifestyle": 7}
                    },
                    "D": {
                        "text": "Over 60 minutes",
                        "scores": {"health": 10, "composition": 9, "stress": 8, "strength": 10, "lifestyle": 8}
                    }
                },
                "response": None
            },

            5: {
                "question": "How do you rate your nutrition habits?",
                "choices": {
                    "A": {
                        "text": "Poor",
                        "scores": {"health": 1, "composition": 1, "stress": 3, "strength": 1, "lifestyle": 2}
                    },
                    "B": {
                        "text": "Average",
                        "scores": {"health": 5, "composition": 4, "stress": 5, "strength": 4, "lifestyle": 5}
                    },
                    "C": {
                        "text": "Good",
                        "scores": {"health": 8, "composition": 7, "stress": 6, "strength": 6, "lifestyle": 7}
                    },
                    "D": {
                        "text": "Excellent",
                        "scores": {"health": 10, "composition": 9, "stress": 7, "strength": 7, "lifestyle": 9}
                    }
                },
                "response": None
            },

            6: {
                "question": "What time of day do you prefer to work out?",
                "choices": {
                    "A": {
                        "text": "Morning",
                        "scores": {"health": 7, "composition": 6, "stress": 7, "strength": 6, "lifestyle": 10}
                    },
                    "B": {
                        "text": "Afternoon",
                        "scores": {"health": 6, "composition": 5, "stress": 6, "strength": 5, "lifestyle": 6}
                    },
                    "C": {
                        "text": "Evening",
                        "scores": {"health": 5, "composition": 5, "stress": 5, "strength": 5, "lifestyle": 5}
                    },
                    "D": {
                        "text": "Whenever I have time",
                        "scores": {"health": 4, "composition": 3, "stress": 6, "strength": 3, "lifestyle": 7}
                    }
                },
                "response": None
            },

            7: {
                "question": "What is your biggest challenge staying consistent?",
                "choices": {
                    "A": {
                        "text": "Lack of time",
                        "scores": {"health": 4, "composition": 3, "stress": 3, "strength": 3, "lifestyle": 1}
                    },
                    "B": {
                        "text": "Lack of energy",
                        "scores": {"health": 3, "composition": 3, "stress": 2, "strength": 2, "lifestyle": 2}
                    },
                    "C": {
                        "text": "Lack of motivation",
                        "scores": {"health": 2, "composition": 2, "stress": 1, "strength": 1, "lifestyle": 1}
                    },
                    "D": {
                        "text": "Injuries or pain",
                        "scores": {"health": 1, "composition": 1, "stress": 3, "strength": 0, "lifestyle": 0}
                    }
                },
                "response": None
            },

            8: {
                "question": "How quickly do you recover after workouts?",
                "choices": {
                    "A": {
                        "text": "Very slow",
                        "scores": {"health": 1, "composition": 1, "stress": 4, "strength": 1, "lifestyle": 1}
                    },
                    "B": {
                        "text": "Slow",
                        "scores": {"health": 4, "composition": 3, "stress": 5, "strength": 3, "lifestyle": 3}
                    },
                    "C": {
                        "text": "Normal",
                        "scores": {"health": 7, "composition": 5, "stress": 6, "strength": 6, "lifestyle": 6}
                    },
                    "D": {
                        "text": "Fast",
                        "scores": {"health": 10, "composition": 7, "stress": 7, "strength": 9, "lifestyle": 8}
                    }
                },
                "response": None
            },

            9: {
                "question": "What is your favorite type of cardio?",
                "choices": {
                    "A": {
                        "text": "Running",
                        "scores": {"health": 9, "composition": 6, "stress": 5, "strength": 6, "lifestyle": 6}
                    },
                    "B": {
                        "text": "Cycling",
                        "scores": {"health": 8, "composition": 5, "stress": 5, "strength": 5, "lifestyle": 7}
                    },
                    "C": {
                        "text": "Rowing",
                        "scores": {"health": 7, "composition": 5, "stress": 4, "strength": 8, "lifestyle": 5}
                    },
                    "D": {
                        "text": "Walking / hiking",
                        "scores": {"health": 6, "composition": 4, "stress": 7, "strength": 3, "lifestyle": 10}
                    }
                },
                "response": None
            },

            10: {
                "question": "How would you rate your overall workout intensity?",
                "choices": {
                    "A": {
                        "text": "Low",
                        "scores": {"health": 2, "composition": 2, "stress": 4, "strength": 2, "lifestyle": 4}
                    },
                    "B": {
                        "text": "Moderate",
                        "scores": {"health": 6, "composition": 5, "stress": 6, "strength": 5, "lifestyle": 6}
                    },
                    "C": {
                        "text": "High",
                        "scores": {"health": 9, "composition": 8, "stress": 7, "strength": 9, "lifestyle": 7}
                    },
                    "D": {
                        "text": "Varies",
                        "scores": {"health": 5, "composition": 4, "stress": 6, "strength": 4, "lifestyle": 7}
                    }
                },
                "response": None
            }

        }



        self.daily_goals = {

            # A — Movement & Activity
            1: {
                "goal": "Take at least 8,000 steps today",
                "scores": {"health": 9, "composition": 6, "stress": 7, "strength": 3, "lifestyle": 10}
            },
            2: {
                "goal": "Complete 20 minutes of intentional exercise",
                "scores": {"health": 8, "composition": 6, "stress": 6, "strength": 5, "lifestyle": 9}
            },
            3: {
                "goal": "Do a 10-minute stretching session",
                "scores": {"health": 7, "composition": 2, "stress": 9, "strength": 2, "lifestyle": 8}
            },
            4: {
                "goal": "Walk for 10 minutes after a meal",
                "scores": {"health": 8, "composition": 5, "stress": 6, "strength": 2, "lifestyle": 9}
            },
            5: {
                "goal": "Avoid sitting longer than 60 minutes at a time",
                "scores": {"health": 8, "composition": 4, "stress": 7, "strength": 3, "lifestyle": 10}
            },
            6: {
                "goal": "Add 1 extra walk today compared to usual",
                "scores": {"health": 7, "composition": 5, "stress": 6, "strength": 2, "lifestyle": 9}
            },
            7: {
                "goal": "Take the stairs whenever possible",
                "scores": {"health": 7, "composition": 4, "stress": 4, "strength": 5, "lifestyle": 8}
            },
            8: {
                "goal": "Spend 15 minutes outdoors walking or moving",
                "scores": {"health": 8, "composition": 4, "stress": 9, "strength": 3, "lifestyle": 9}
            },

            # B — Strength Training
            9: {
                "goal": "Do 30 bodyweight squats today",
                "scores": {"health": 6, "composition": 6, "stress": 4, "strength": 8, "lifestyle": 7}
            },
            10: {
                "goal": "Perform 20 push-ups",
                "scores": {"health": 5, "composition": 5, "stress": 4, "strength": 9, "lifestyle": 7}
            },
            11: {
                "goal": "Do a 5-minute core routine",
                "scores": {"health": 6, "composition": 6, "stress": 5, "strength": 8, "lifestyle": 7}
            },
            12: {
                "goal": "Train one muscle group lightly today",
                "scores": {"health": 5, "composition": 5, "stress": 4, "strength": 7, "lifestyle": 6}
            },
            13: {
                "goal": "Hold a 1-minute plank",
                "scores": {"health": 5, "composition": 4, "stress": 4, "strength": 8, "lifestyle": 6}
            },
            14: {
                "goal": "Perform 3 sets of any strength movement",
                "scores": {"health": 6, "composition": 5, "stress": 4, "strength": 7, "lifestyle": 7}
            },
            15: {
                "goal": "Do 20 lunges per leg",
                "scores": {"health": 6, "composition": 5, "stress": 4, "strength": 8, "lifestyle": 7}
            },
            16: {
                "goal": "Spend 5 minutes improving posture",
                "scores": {"health": 7, "composition": 3, "stress": 6, "strength": 6, "lifestyle": 8}
            },

            # C — Mobility & Flexibility
            17: {
                "goal": "Complete a 3-minute deep breathing session",
                "scores": {"health": 6, "composition": 1, "stress": 10, "strength": 1, "lifestyle": 8}
            },
            18: {
                "goal": "Do a full-body mobility warmup",
                "scores": {"health": 7, "composition": 2, "stress": 8, "strength": 3, "lifestyle": 8}
            },
            19: {
                "goal": "Stretch your hips and lower back for 5 minutes",
                "scores": {"health": 8, "composition": 2, "stress": 9, "strength": 2, "lifestyle": 8}
            },
            20: {
                "goal": "Perform ankle mobility drills for 3 minutes",
                "scores": {"health": 6, "composition": 2, "stress": 6, "strength": 2, "lifestyle": 7}
            },
            21: {
                "goal": "Do a 10-minute yoga flow",
                "scores": {"health": 7, "composition": 3, "stress": 10, "strength": 3, "lifestyle": 9}
            },
            22: {
                "goal": "Work on hamstring flexibility for 3 minutes",
                "scores": {"health": 6, "composition": 2, "stress": 8, "strength": 2, "lifestyle": 7}
            },
            23: {
                "goal": "Improve shoulder mobility for 3 minutes",
                "scores": {"health": 6, "composition": 2, "stress": 7, "strength": 3, "lifestyle": 7}
            },
            24: {
                "goal": "Hold a deep squat for 60 seconds total",
                "scores": {"health": 6, "composition": 3, "stress": 6, "strength": 4, "lifestyle": 7}
            },

            # D — Cardio & Endurance
            25: {
                "goal": "Do 10 minutes of cardio",
                "scores": {"health": 8, "composition": 6, "stress": 6, "strength": 4, "lifestyle": 8}
            },
            26: {
                "goal": "Complete 5 intervals of 30s fast / 30s slow",
                "scores": {"health": 8, "composition": 6, "stress": 5, "strength": 6, "lifestyle": 7}
            },
            27: {
                "goal": "Add 1 extra mile to your total walking",
                "scores": {"health": 9, "composition": 5, "stress": 6, "strength": 4, "lifestyle": 9}
            },
            28: {
                "goal": "Do 3 minutes of jumping jacks",
                "scores": {"health": 7, "composition": 4, "stress": 5, "strength": 4, "lifestyle": 7}
            },
            29: {
                "goal": "Take a brisk 20-minute walk",
                "scores": {"health": 9, "composition": 5, "stress": 7, "strength": 3, "lifestyle": 10}
            },
            30: {
                "goal": "Get your heart rate up at least once today",
                "scores": {"health": 7, "composition": 4, "stress": 5, "strength": 4, "lifestyle": 8}
            },

            # E — Nutrition Goals
            31: {
                "goal": "Drink 8 cups of water",
                "scores": {"health": 10, "composition": 4, "stress": 6, "strength": 4, "lifestyle": 9}
            },
            32: {
                "goal": "Eat 2 servings of vegetables",
                "scores": {"health": 9, "composition": 5, "stress": 6, "strength": 4, "lifestyle": 9}
            },
            33: {
                "goal": "Eat one high-protein meal",
                "scores": {"health": 8, "composition": 7, "stress": 5, "strength": 7, "lifestyle": 8}
            },
            34: {
                "goal": "Limit added sugar to one serving",
                "scores": {"health": 9, "composition": 7, "stress": 7, "strength": 4, "lifestyle": 8}
            },
            35: {
                "goal": "Track your food for the entire day",
                "scores": {"health": 7, "composition": 8, "stress": 5, "strength": 4, "lifestyle": 9}
            },
            36: {
                "goal": "Choose a healthy snack instead of a processed one",
                "scores": {"health": 8, "composition": 7, "stress": 6, "strength": 4, "lifestyle": 9}
            },
            37: {
                "goal": "Eat slowly for one meal today",
                "scores": {"health": 6, "composition": 4, "stress": 8, "strength": 3, "lifestyle": 8}
            },
            38: {
                "goal": "Avoid late-night eating today",
                "scores": {"health": 7, "composition": 6, "stress": 6, "strength": 4, "lifestyle": 8}
            },

            # F — Lifestyle & Recovery
            39: {
                "goal": "Go to sleep 30 minutes earlier tonight",
                "scores": {"health": 9, "composition": 5, "stress": 9, "strength": 4, "lifestyle": 10}
            },
            40: {
                "goal": "Spend 5 minutes journaling about your health",
                "scores": {"health": 6, "composition": 2, "stress": 9, "strength": 2, "lifestyle": 8}
            },
            41: {
                "goal": "Take one mental break with no screens",
                "scores": {"health": 6, "composition": 1, "stress": 9, "strength": 1, "lifestyle": 8}
            },
            42: {
                "goal": "Practice gratitude for 3 minutes",
                "scores": {"health": 5, "composition": 1, "stress": 10, "strength": 1, "lifestyle": 8}
            },
            43: {
                "goal": "Reduce stress with a breathing technique",
                "scores": {"health": 6, "composition": 1, "stress": 10, "strength": 1, "lifestyle": 8}
            },
            44: {
                "goal": "Do one thing that improves tomorrow",
                "scores": {"health": 6, "composition": 3, "stress": 7, "strength": 3, "lifestyle": 10}
            },
            45: {
                "goal": "Get sunlight within 1 hour after waking",
                "scores": {"health": 8, "composition": 3, "stress": 7, "strength": 3, "lifestyle": 9}
            },
            46: {
                "goal": "Stretch before bed for 5 minutes",
                "scores": {"health": 7, "composition": 2, "stress": 9, "strength": 2, "lifestyle": 8}
            },

            # G — Habit Building
            47: {
                "goal": "Complete any workout today, even a short one",
                "scores": {"health": 7, "composition": 5, "stress": 6, "strength": 6, "lifestyle": 10}
            },
            48: {
                "goal": "Perform at least 5 minutes of movement today",
                "scores": {"health": 6, "composition": 3, "stress": 5, "strength": 3, "lifestyle": 10}
            },
            49: {
                "goal": "Track today’s mood, energy, and workout",
                "scores": {"health": 6, "composition": 2, "stress": 8, "strength": 3, "lifestyle": 9}
            },
            50: {
                "goal": "Hit your daily goal streak",
                "scores": {"health": 10, "composition": 4, "stress": 7, "strength": 4, "lifestyle": 10}
            }
        }

        self.vocab = []

        self.rules = {
            # --- Exercise ---
            "completed_walk":                  {"health": +1, "composition": +0, "stress": -1, "strength": +0, "lifestyle": +1},
            "completed_run":                   {"health": +2, "composition": +1, "stress": -1, "strength": +1, "lifestyle": +1},
            "completed_strength_workout":      {"health": +1, "composition": +1, "stress": -1, "strength": +3, "lifestyle": +1},
            "completed_cardio_workout":        {"health": +2, "composition": +1, "stress": -2, "strength": +0, "lifestyle": +1},
            "completed_yoga_session":          {"health": +1, "composition": +0, "stress": -3, "strength": +0, "lifestyle": +1},
            "completed_stretching":            {"health": +1, "composition": +0, "stress": -2, "strength": +0, "lifestyle": +1},
            "completed_hiit":                  {"health": +2, "composition": +2, "stress": -1, "strength": +2, "lifestyle": +1},
            "completed_cycling":               {"health": +2, "composition": +1, "stress": -1, "strength": +1, "lifestyle": +1},
            "completed_sports_activity":       {"health": +2, "composition": +1, "stress": -1, "strength": +1, "lifestyle": +2},

            # --- Routine / Daily Movement ---
            "completed_step_goal":             {"health": +2, "composition": +1, "stress": -1, "strength": +0, "lifestyle": +2},
            "completed_hard_workout":          {"health": +3, "composition": +2, "stress": -1, "strength": +3, "lifestyle": +1},
            "completed_light_activity":        {"health": +1, "composition": +0, "stress": -1, "strength": +0, "lifestyle": +1},

            # --- Nutrition ---
            "ate_healthy_meal":                {"health": +2, "composition": +2, "stress": +0, "strength": +0, "lifestyle": +1},
            "ate_unhealthy_meal":              {"health": -1, "composition": -2, "stress": +0, "strength": +0, "lifestyle": -1},
            "tracked_meals":                   {"health": +0, "composition": +1, "stress": +0, "strength": +0, "lifestyle": +1},
            "drank_water_goal":                {"health": +2, "composition": +0, "stress": -1, "strength": +0, "lifestyle": +1},
            "overate":                         {"health": -1, "composition": -3, "stress": +1, "strength": +0, "lifestyle": -1},
            "late_night_eating":               {"health": -1, "composition": -1, "stress": +1, "strength": +0, "lifestyle": -1},
            "skipped_breakfast":               {"health": -1, "composition": -1, "stress": +0, "strength": +0, "lifestyle": -1},
            "meal_prep_done":                  {"health": +1, "composition": +2, "stress": -1, "strength": +0, "lifestyle": +2},

            # --- Recovery / Sleep ---
            "slept_early":                     {"health": +2, "composition": +0, "stress": -2, "strength": +0, "lifestyle": +1},
            "slept_late":                      {"health": -1, "composition": +0, "stress": +1, "strength": +0, "lifestyle": -1},
            "good_sleep_quality":              {"health": +3, "composition": +0, "stress": -3, "strength": +0, "lifestyle": +1},
            "poor_sleep_quality":              {"health": -2, "composition": +0, "stress": +3, "strength": +0, "lifestyle": -1},
            "took_rest_day":                   {"health": +1, "composition": +0, "stress": -1, "strength": +1, "lifestyle": +1},
            "ignored_rest_day":                {"health": -1, "composition": +0, "stress": +1, "strength": -2, "lifestyle": -1},
            "hydrated_before_sleep":           {"health": +1, "composition": +0, "stress": -1, "strength": +0, "lifestyle": +1},

            # --- Mental / Stress ---
            "meditated":                       {"health": +1, "composition": +0, "stress": -3, "strength": +0, "lifestyle": +1},
            "journaling_completed":            {"health": +0, "composition": +0, "stress": -2, "strength": +0, "lifestyle": +1},
            "stressful_day":                   {"health": -1, "composition": +0, "stress": +3, "strength": -1, "lifestyle": -1},
            "relaxation_exercise":             {"health": +1, "composition": +0, "stress": -2, "strength": +0, "lifestyle": +1},
            "breathing_exercises":             {"health": +0, "composition": +0, "stress": -2, "strength": +0, "lifestyle": +1},
            "took_mental_break":               {"health": +0, "composition": +0, "stress": -1, "strength": +0, "lifestyle": +1},
            "high_stress_event":               {"health": -2, "composition": +0, "stress": +4, "strength": -1, "lifestyle": -2},
            "low_stress_day":                  {"health": +1, "composition": +0, "stress": -1, "strength": +0, "lifestyle": +1},

            # --- Consistency / Habits ---
            "completed_daily_goal":            {"health": +1, "composition": +1, "stress": -1, "strength": +1, "lifestyle": +3},
            "missed_daily_goal":               {"health": -1, "composition": +0, "stress": +1, "strength": -1, "lifestyle": -2},
            "weekly_consistency_win":          {"health": +2, "composition": +2, "stress": -1, "strength": +1, "lifestyle": +4},
            "broke_streak":                    {"health": -1, "composition": -1, "stress": +1, "strength": -1, "lifestyle": -3},
            "streak_extended":                 {"health": +2, "composition": +1, "stress": -1, "strength": +1, "lifestyle": +4},
            "logged_activity_today":           {"health": +0, "composition": +0, "stress": -1, "strength": +0, "lifestyle": +2},
            "skipped_logging":                 {"health": +0, "composition": +0, "stress": +1, "strength": +0, "lifestyle": -1},

            # --- Negative / Regression ---
            "sedentary_day":                   {"health": -2, "composition": -1, "stress": +1, "strength": -2, "lifestyle": -2},
            "junk_food_day":                   {"health": -2, "composition": -3, "stress": +1, "strength": -1, "lifestyle": -2},
            "overslept":                       {"health": -1, "composition": +0, "stress": +1, "strength": +0, "lifestyle": -1},
            "underslept":                      {"health": -2, "composition": +0, "stress": +2, "strength": -1, "lifestyle": -1},
            "skipped_workout":                 {"health": -1, "composition": -1, "stress": +1, "strength": -2, "lifestyle": -2},
            "low_energy_day":                  {"health": -1, "composition": +0, "stress": +1, "strength": -1, "lifestyle": -1},
            "excessive_screen_time":           {"health": +0, "composition": +0, "stress": +2, "strength": +0, "lifestyle": -2},

            # --- Major Milestones ---
            "lost_weight_milestone":           {"health": +3, "composition": +5, "stress": -1, "strength": +1, "lifestyle": +3},
            "gained_weight_muscle_milestone":  {"health": +3, "composition": +3, "stress": -1, "strength": +5, "lifestyle": +3},
            "hit_personal_record":             {"health": +2, "composition": +1, "stress": -1, "strength": +4, "lifestyle": +2},
            "completed_program_week":          {"health": +2, "composition": +2, "stress": -2, "strength": +2, "lifestyle": +4},
            "completed_30_day_challenge":      {"health": +4, "composition": +4, "stress": -3, "strength": +4, "lifestyle": +5},
            "finished_training_block":         {"health": +3, "composition": +2, "stress": -1, "strength": +3, "lifestyle": +4}
        }




    def get_vocab(self, ratings=None):
        if not ratings:
            ratings = self.ratings
        sorted_ratings = dict(sorted(ratings.items(), key=lambda x: x[1], reverse=True)) 

        for goal in self.daily_goals.keys():
            sorted_items = dict(sorted(self.daily_goals[goal]["scores"].items(), key=lambda x: x[1], reverse=True)) 
            local = list(sorted_items.keys())[:3]
            compare = list(sorted_ratings)[:3]
            if set(local) == set(compare):
                print("\n\nmatch")
                print(dict(sorted_items).keys())
                print(dict(sorted_ratings).keys())
                self.vocab.append(self.daily_goals[goal]["goal"])
        if len(self.vocab) < 5:
            return False

        print("\n\nvocab")
        print(self.vocab)

        return self.vocab




