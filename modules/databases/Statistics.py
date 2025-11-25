import json
import os
import sys
from typing import Dict, Any, List

# Find project root (two levels up from this file: modules/examples/.. /..)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")

if SRC_ROOT not in sys.path:
    sys.path.insert(0, SRC_ROOT)

"""
DynamoDB export example with 30-day stats encoded minimally into the seed.

Flow:
- Build a full 30-day fitness/statistical user profile (per-day variation).
- Map the *aggregate* profile -> MSE signature (5 ints).
- Encode the *30-day time series* into a single integer series_seed.
- Slightly augment the signature with series_seed bits (still 5 ints).
- Initialize MorphicSemanticEngine from that augmented signature.
- Use TableData to turn engine state into table schema/rows.
- Export each step as a DynamoDB-style JSON item.
"""

from mse.core import MorphicSemanticEngine
from modules.databases.TableData import TableData


class Statistics:


    def __init__(self, **kwargs):
        super(Statistics, self).__init__(**kwargs)

    # -------------------------------
    # 30-day stats generation (example)
    #   Same metrics, varying over 30 days
    # -------------------------------

    def get_30day_stats(self) -> List[Dict[str, Any]]:
        """
        Build synthetic 30-day stats.
        In a real system this would come from your tracking DB or logs.
        """
        days: List[Dict[str, Any]] = []
        for day in range(30):
            # Simple pseudo-variation over days:
            treadmill = 200 + (day * 3) % 80      # 200–279
            steps = 9000 + (day * 250)           # grows slowly
            calories = 2100 + ((day % 5) * 80)   # cycles a bit
            protein = 120 + (day % 4) * 5        # 120–135
            sleep = 6.0 + (day % 3) * 0.4        # 6.0, 6.4, 6.8

            days.append({
                "day_index": day,  # 0–29
                "treadmill_minutes": treadmill,
                "avg_daily_steps": steps,
                "calories": calories,
                "protein_g": protein,
                "sleep_hours": sleep,
            })
        return days


    # -------------------------------
    # Aggregate profile -> MSE signature
    #   (health, cognition, stress, strength, lifestyle)
    # -------------------------------

    def aggregate_profile_from_30days(self, days: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate 30-day series into a single 'profile' view."""
        n = len(days)
        avg_treadmill = sum(d["treadmill_minutes"] for d in days) / n
        avg_steps = sum(d["avg_daily_steps"] for d in days) / n
        avg_calories = sum(d["calories"] for d in days) / n
        avg_protein = sum(d["protein_g"] for d in days) / n
        avg_sleep = sum(d["sleep_hours"] for d in days) / n

        # Fake subjective values for demo:
        return {
            "avg_treadmill": avg_treadmill,
            "avg_steps": avg_steps,
            "avg_calories": avg_calories,
            "avg_protein": avg_protein,
            "avg_sleep": avg_sleep,
            "subjective_stress": "high",    # e.g., from surveys
            "subjective_fatigue": 6,        # 1–10
            "subjective_mood": 7,           # 1–10
            "user_id": "u_30day_example",
        }


    def profile_to_signature(self, profile: Dict[str, Any]) -> tuple[int, int, int, int, int]:
        """
        Map aggregate 30-day profile -> (health, cognition, stress, strength, lifestyle).
        Result is 5 ints 0–100.
        """
        avg_treadmill = profile["avg_treadmill"]
        avg_steps = profile["avg_steps"]
        avg_calories = profile["avg_calories"]
        avg_protein = profile["avg_protein"]
        avg_sleep = profile["avg_sleep"]
        stress_str = profile["subjective_stress"]
        fatigue = profile["subjective_fatigue"]
        mood = profile["subjective_mood"]

        # Health
        activity_score = min(100, (avg_treadmill / 300) * 40 + (avg_steps / 12000) * 40)
        calorie_penalty = 0
        if avg_calories < 1500:
            calorie_penalty -= 10
        elif avg_calories > 2800:
            calorie_penalty -= 5
        h = int(max(0, min(100, activity_score + calorie_penalty)))

        # Cognition
        sleep_score = min(100, max(0, (avg_sleep / 8.0) * 70))
        mood_score = (mood / 10.0) * 30
        c = int(max(0, min(100, sleep_score + mood_score)))

        # Stress
        stress_map = {"low": 25, "medium": 50, "high": 75}
        stress_base = stress_map.get(stress_str, 50)
        fatigue_component = (fatigue / 10.0) * 30
        st = int(max(0, min(100, stress_base + fatigue_component)))

        # Strength
        strn_score = min(100, (avg_treadmill / 300) * 30 + (avg_protein / 150.0) * 70)
        strn = int(max(0, min(100, strn_score)))

        # Lifestyle
        lifestyle_score = min(100, (avg_sleep / 8.0) * 40 + (avg_steps / 12000) * 40)
        life = int(max(0, min(100, lifestyle_score)))

        return (h, c, st, strn, life)


    # -------------------------------
    # 30-day stats -> series_seed (minimal)
    # -------------------------------

    def quantize_day(self, day: Dict[str, Any]) -> Dict[str, int]:
        """
        Quantize one day's stats into 0–255 buckets.
        This is lossy on purpose but very compact.
        """
        q: Dict[str, int] = {}

        q["treadmill"] = int(max(0, min(255, day["treadmill_minutes"] / 600 * 255)))
        q["steps"]     = int(max(0, min(255, day["avg_daily_steps"] / 30000 * 255)))
        q["calories"]  = int(max(0, min(255, (day["calories"] - 1200) / 2800 * 255)))
        q["protein"]   = int(max(0, min(255, day["protein_g"] / 250 * 255)))
        q["sleep"]     = int(max(0, min(255, day["sleep_hours"] / 12 * 255)))
        return q


    def encode_30day_stats(self, days: List[Dict[str, Any]]) -> int:
        """
        Turn an entire 30-day series into ONE integer (series_seed).

        Strategy:
        - Quantize each day's 5 stats to 0–255.
        - Fold them through a rolling hash with a prime modulus.

        Result: a single integer that “summarizes” the whole 30-day pattern.
        """
        MOD = 2_147_483_647  # large prime (fits in 32-bit signed)
        BASE = 257

        series_seed = 0
        for day in days:
            q = self.quantize_day(day)
            # Fold each dimension deterministically into the rolling hash
            for key in ("treadmill", "steps", "calories", "protein", "sleep"):
                series_seed = (series_seed * BASE + q[key]) % MOD

        return series_seed


    def augment_signature_with_series(self, signature: tuple[int, int, int, int, int], series_seed: int) -> List[int]:
        """
        Mix bits of series_seed into the 5-element signature,
        keeping only 0–100, so MorphicSemanticEngine stays happy.

        This makes the 30-day pattern influence the internal seed,
        while we only store (signature, series_seed).
        """
        h, c, st, strn, life = signature
        sig_list = [h, c, st, strn, life]

        for i in range(5):
            # Take 7 bits at a time from the series_seed (0–127).
            chunk = (series_seed >> (i * 7)) & 0x7F
            sig_list[i] = int((sig_list[i] + chunk) % 101)  # keep 0–100

        return sig_list


