import csv
from datetime import datetime


# ---------------------------------------------------------------------
# Mock seat availability
# ---------------------------------------------------------------------
def fetch_available_seats(airline: str, flight_number: str, flight_date: str):
    """
    MOCK function so the workflow has something to run.

    Returns a list of dicts:
        { "seat": "11D", "tier": 6 }

    `tier` should match your CSV seat-tier primer:
        14 = First Class Aisle
        ...
         1 = Regular Middle
    """

    # Rotate "good" vs "bad" availability based on day of month
    try:
        day = int(flight_date.split("-")[-1])
    except Exception:
        # If the date is weird, just pretend nothing good is available
        return [
            {"seat": "24E", "tier": 1},
            {"seat": "26B", "tier": 1},
        ]

    if day % 2 == 0:
        # Even days: pretend some nicer seats are available
        return [
            {"seat": "11D", "tier": 6},   # MCE window exit
            {"seat": "8C", "tier": 9},    # MCE aisle (non-bulkhead, non-exit)
            {"seat": "3A", "tier": 13},   # First class window
        ]
    else:
        # Odd days: nothing really better
        return [
            {"seat": "24E", "tier": 1},   # regular middle
            {"seat": "26B", "tier": 1},
        ]


# ---------------------------------------------------------------------
# Main seat comparison logic
# ---------------------------------------------------------------------
def check_flights():
    alerts = []

    # Open the CSV and skip any lines that start with "#" BEFORE DictReader
    with open("flights.csv", newline="") as csvfile:
        data_lines = (
            line for line in csvfile
            if not line.lstrip().startswith("#") and line.strip() != ""
        )

        reader = csv.DictReader(data_lines)

        for row in reader:
            if not row:
                continue

            # Handle missing "Active" safely
            active = (row.get("Active") or "").strip().upper()
            if active != "Y":
                # ignore inactive trips
                continue

            airline = (row.get("Airline") or "").strip()
            flight_number = (row.get("FlightNumber") or "").strip()
            flight_date = (row.get("FlightDate") or "").strip()
            origin = (row.get("Origin") or "").strip()
            destination = (row.get("Destination") or "").strip()
            current_seat = (row.get("CurrentSeat") or "").strip()

            # CurrentTier must be an int – use 0 as absolute worst if blank
            try:
                current_tier = int(row.get("CurrentTier", "0"))
            except ValueError:
                current_tier = 0

            # Get (mock) seat availability
            available = fetch_available_seats(airline, flight_number, flight_date)

            best_option = None
            best_tier = current_tier

            for option in available:
                seat = option.get("seat", "").strip()
                try:
                    seat_tier = int(option.get("tier", 0))
                except ValueError:
                    seat_tier = 0

                if seat_tier > best_tier:
                    best_tier = seat_tier
                    best_option = seat

            # Build human-readable messages
            if best_option:
                # This line includes 🎉 so the GitHub Action will trigger email/SMS
                msg = (
                    f"🎉 {airline} {flight_number} on {flight_date} "
                    f"{origin}->{destination}: "
                    f"better seat {best_option} (tier {best_tier}) "
                    f"vs current {current_seat} (tier {current_tier})."
                )
            else:
                # No emoji here — workflow will NOT send mail for these
                msg = (
                    f"{airline} {flight_number} on {flight_date} "
                    f"{origin}->{destination}: "
                    f"no better seat than {current_seat} (tier {current_tier})."
                )

            alerts.append(msg)

    return "\n".join(alerts)


def main():
    results = check_flights()
    if not results:
        print("No flights to check.")
    else:
        print(results)


if __name__ == "__main__":
    main()
