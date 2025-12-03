import csv
import requests
from datetime import datetime

# -----------------------------
# Seat Tier Ranking Logic
# -----------------------------
def seat_to_tier(seat_str):
    """
    Converts a seat label like '10C' or '8A' into a tier score.
    Higher tier_score = BETTER seat.
    """

    if seat_str is None or seat_str.strip() == "":
        return 0

    seat = seat_str.upper().strip()

    # Aisle seats (C & D on AA single aisle aircraft)
    if seat.endswith("C"):
        return 10
    if seat.endswith("D"):
        return 9

    # Window seats (A or F)
    if seat.endswith("A") or seat.endswith("F"):
        return 8

    # Everything else is mid-tier
    return 5


# -----------------------------
# Mock Seat Map Fetcher (for now)
# -----------------------------
def fetch_available_seats(airline, flight_number, flight_date):
    """
    Eventually this will call AA's real seat map API.
    For now, we simulate by returning *fake* seat availability.
    """

    # mock rotating availability just so automation *works*
    day = int(flight_date.split("-")[-1])
    if day % 2 == 0:
        return ["7C", "12A", "13D"]   # better seats open
    else:
        return ["24B", "27E"]         # nothing great


# -----------------------------
# Main seat comparison logic
# -----------------------------
def check_flights():
    alerts = []

    with open("flights.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:

            # Skip rows that start with "#" (comment lines)
            if all(value.strip().startswith("#") for value in row.values()):
               continue
                
            active = row["Active"].strip().upper()
            if active != "Y":
                continue  # ignore inactive trips

            airline = row["Airline"]
            flight_number = row["FlightNumber"]
            flight_date = row["FlightDate"]
            origin = row["Origin"]
            destination = row["Destination"]
            current_seat = row["CurrentSeat"]
            current_tier = int(row["CurrentTier"])

            # get seat availability (mock for now)
            available = fetch_available_seats(airline, flight_number, flight_date)

            best_option = None
            best_tier = current_tier

            for seat in available:
                t = seat_to_tier(seat)
                if t > best_tier:
                    best_tier = t
                    best_option = seat

            if best_option:
                alerts.append(
                    f"🎉 Better seat found on {airline} {flight_number} "
                    f"({flight_date} {origin}->{destination}): {best_option} "
                    f"(Tier {best_tier}) replacing {current_seat} (Tier {current_tier})"
                )

    return alerts


# -----------------------------
# Script Entry Point
# -----------------------------
if __name__ == "__main__":
    results = check_flights()

    if not results:
        print("No better seats found.")
    else:
        print("Alerts:")
        for r in results:
            print(r)
