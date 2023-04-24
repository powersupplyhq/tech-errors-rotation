# Tech Errors Rotation App

## Summary
This app is responsible for setting the #tech-errors rotation each week. The selected engineer is responsible for monitoring that channel as well as Relicx, the PopSQL dashboards, and any other error or logging services.

## How It Works
In the `.env` file, there are two variables: `ENGINEERS` and `IGNORE`. The former is a comma separated list of the engineers that are on normal rotation. The latter is a list of engineers to be temporarily ignored for rotation (e.g. on vacation, out sick, etc.). `ENGINEERS` must be set in order for the app to work properly.

Each day a cron runs the script at 12PM EST to decide who will be on rotation for that day. The script will output the selected engineer to the determined Slack channel as set in the `.env` via the `SLACK_WEBHOOK_URL`.

The `duty_history.json` file will record the days that each person has been on duty in order to enforce the selection rules.

## Selection Rules
1. An engineer cannot be on duty two days in a row
2. An engineer cannot be on duty more than two times in a work week (Mon-Fri)
3. If for some reason an engineer cannot be on duty the day they are selected, re-running the script will pick a new engineer
4. As previously mentioned, an engineer on the `IGNORE` list will not be selected
