from datetime import date, timedelta


def calculate_completion_rate(logs):
    if not logs:
        return 0

    completed = sum(
        1 for log in logs
        if log["completed"]
    )

    return round((completed / len(logs)) * 100)


def calculate_current_streak(logs):
    completed_dates = {
        log["log_date"]
        for log in logs
        if log["completed"]
    }

    if not completed_dates:
        return 0

    today = date.today()

    if today in completed_dates:
        current_date = today

    elif today - timedelta(days=1) in completed_dates:
        current_date = today - timedelta(days=1)

    else:
        return 0

    streak = 0

    while current_date in completed_dates:
        streak += 1
        current_date -= timedelta(days=1)

    return streak


def calculate_best_streak(logs):
    completed_dates = sorted({
        log["log_date"]
        for log in logs
        if log["completed"]
    })

    if not completed_dates:
        return 0

    best_streak = 1
    current_streak = 1

    for i in range(1, len(completed_dates)):

        if completed_dates[i] == completed_dates[i - 1] + timedelta(days=1):
            current_streak += 1
        else:
            current_streak = 1

        best_streak = max(
            best_streak,
            current_streak
        )

    return best_streak


def calculate_total_time(logs):
    total_minutes = sum(
        log["time_spent"] or 0
        for log in logs
    )

    return round(total_minutes / 60, 1)


def calculate_weekly_progress(logs):
    today = date.today()

    weekly_data = []

    for i in range(6, -1, -1):

        current_date = today - timedelta(days=i)

        day_logs = [
            log for log in logs
            if log["log_date"] == current_date
        ]

        completed = sum(
            1 for log in day_logs
            if log["completed"]
        )

        total = len(day_logs)

        percentage = (
            round((completed / total) * 100)
            if total > 0
            else 0
        )

        weekly_data.append({
            "date": current_date.strftime("%d %b"),
            "completion": percentage
        })

    return weekly_data


def calculate_monthly_progress(logs):
    today = date.today()

    monthly_data = []

    for i in range(5, -1, -1):

        month_offset = today.month - i
        year = today.year

        while month_offset <= 0:
            month_offset += 12
            year -= 1

        month_logs = [
            log for log in logs
            if log["log_date"].year == year
            and log["log_date"].month == month_offset
        ]

        completed = sum(
            1 for log in month_logs
            if log["completed"]
        )

        total = len(month_logs)

        percentage = (
            round((completed / total) * 100)
            if total > 0
            else 0
        )

        month_name = date(
            year,
            month_offset,
            1
        ).strftime("%b %Y")

        monthly_data.append({
            "month": month_name,
            "completion": percentage
        })

    return monthly_data


def calculate_activity_progress(logs):
    activity_data = {}

    for log in logs:

        title = log["title"]

        if title not in activity_data:
            activity_data[title] = {
                "total": 0,
                "completed": 0
            }

        activity_data[title]["total"] += 1

        if log["completed"]:
            activity_data[title]["completed"] += 1

    result = []

    for title, data in activity_data.items():

        percentage = round(
            (data["completed"] / data["total"]) * 100
        )

        result.append({
            "title": title,
            "completion": percentage
        })

    return result


def calculate_time_investment(logs):
    activity_time = {}

    for log in logs:

        title = log["title"]
        minutes = log["time_spent"] or 0

        if title not in activity_time:
            activity_time[title] = 0

        activity_time[title] += minutes

    result = []

    for title, minutes in activity_time.items():

        result.append({
            "title": title,
            "hours": round(minutes / 60, 1)
        })

    return result


def generate_insight(
    completion_rate,
    current_streak,
    total_time
):
    if current_streak >= 7:
        return "Excellent consistency! You have maintained a strong streak. Keep building on this momentum."

    if completion_rate >= 80:
        return "Great progress! Your completion rate is strong. Stay consistent to keep improving."

    if completion_rate >= 50:
        return "You're making steady progress. Try to stay consistent and complete a little more each day."

    if total_time >= 10:
        return "You are investing meaningful time in your activities. Focus on completing more of what you start."

    if completion_rate > 0:
        return "You have started building your progress. Keep showing up regularly to improve your consistency."

    return "Your growth journey starts here. Add an activity and begin tracking your progress."


def calculate_analytics(logs):
    completion_rate = calculate_completion_rate(logs)
    current_streak = calculate_current_streak(logs)
    best_streak = calculate_best_streak(logs)
    total_time = calculate_total_time(logs)

    return {
        "completion_rate": completion_rate,
        "current_streak": current_streak,
        "best_streak": best_streak,
        "total_time": total_time,
        "weekly_progress": calculate_weekly_progress(logs),
        "monthly_progress": calculate_monthly_progress(logs),
        "activity_progress": calculate_activity_progress(logs),
        "time_investment": calculate_time_investment(logs),
        "insight": generate_insight(
            completion_rate,
            current_streak,
            total_time
        )
    }