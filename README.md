AA Seat Stalker

Automated seat-monitoring system for American Airlines flights.

This tool checks your upcoming AA flights on a schedule, looks for better available seats based on your personal seating preferences, and sends you an email alert when an upgrade becomes available. It runs entirely in GitHub Actions, so your own computer does not need to stay on.

⸻

🚀 What This Project Does
	•	Reads your list of flights from a simple flights.csv file
	•	Checks each flight on a fixed schedule (every 15 minutes)
	•	Evaluates seats using your custom tier system:
	•	Tier 1 → MCE aisle, row 2+
	•	Tier 2 → MCE window, row 2+
	•	Tier 3 → Exit row aisle
	•	Tier 4 → Exit row window
	•	Tier 5 → Bulkhead aisle/window
	•	Tier 99 → Everything else
	•	Compares available seats to your current seat
	•	Sends you an email alert only if something better becomes available
	•	Runs 100% in the cloud via GitHub Actions

Right now, the seat-parsing logic is stubbed out. The automation framework is fully built; the only remaining step is connecting to AA’s actual seat map data.

⸻

🧩 How You Use It
	1.	Edit flights.csv to add or update flights you want to monitor
	2.	Commit the change to GitHub
	3.	GitHub Actions automatically runs the checker every 15 minutes
	4.	If a better seat opens up, you receive an email alert
	5.	You hop into the American Airlines app and grab the better seat

That’s it. No servers. No cron jobs. No laptop sitting open.
The cloud does the hunting; you just make decisions.

⸻

📄 The flights.csv Format

The file looks like this:

Active,Airline,FlightNumber,FlightDate,Origin,Destination,CurrentSeat,CurrentTier,Notes
Y,AA,1234,2025-12-20,PHL,DFW,8C,2,MCE window row 8
Y,AA,5678,2025-12-22,DFW,LAX,10D,3,Exit row aisle
N,AA,999,2025-12-24,LAX,PHL,9C,1,Perfect seat – no alerts

Column explanations:
	•	Active — Y to track the flight, N to ignore
	•	Airline — “AA”
	•	FlightNumber — numbers only (e.g. 1234)
	•	FlightDate — YYYY-MM-DD
	•	Origin / Destination — airport codes
	•	CurrentSeat — your assigned seat (e.g. 8C)
	•	CurrentTier — how good that seat is for you
	•	Notes — optional, for your reference

⸻

🔔 Email Alerts

The project uses simple SMTP (Gmail works great) to send upgrade alerts.
You configure the email settings in GitHub Secrets:
	•	SMTP_SERVER
	•	SMTP_PORT
	•	SMTP_USER
	•	SMTP_PASS
	•	ALERT_EMAIL_TO

⸻

🛠️ GitHub Actions

Located in:
.github/workflows/seat_stalker.yml

Runs automatically every 15 minutes and calls the main script:

python seat_stalker.py

You can also trigger it manually from the “Actions” tab at any time.

⸻

🔧 What’s Still Required (Seatmap Parsing)

The AA seatmap parser is stubbed out.
To complete the system, we will:
	1.	Capture a real AA seatmap network response
	2.	Identify the endpoint returning seat availability
	3.	Extract seat attributes:
	•	Row number
	•	Seat ID (e.g. “8C”)
	•	Cabin zone (MCE, Main, Exit, Bulkhead)
	•	Type (aisle, window, middle)
	4.	Feed the parsed seats into the existing seat-ranking system

Once this is added, the system becomes fully operational.

⸻

🏁 Status

Core automation: Complete
	•	Cloud runner
	•	Tier logic
	•	Multi-flight support
	•	Email notifications
	•	Continuous schedule
	•	CSV control panel

Next step: Add AA seatmap parsing logic.

⸻

If you want help connecting the seatmap, adjusting the tier logic, or customizing the CSV format, continue following the setup guide or reach out.

⸻

END OF README.md
