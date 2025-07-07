import matplotlib.pyplot as plt

# Figure configuration
fig_width_in = 11.7    # A3 size approx in inches (portrait)
fig_height_in = 16.5
TITLE = "Term 3 2025 Planner"
FONT_FAMILY = "DejaVu Sans"

# Dates setup
from datetime import datetime, timedelta
START_DATE = datetime(2025, 7, 14)
END_DATE = datetime(2025, 9, 12)
NZ_HOLIDAYS = {
    datetime(2025, 10, 24): "Labour Day (Observed)",
    datetime(2025, 11, 14): "Canterbury Show Day"
}
HOLIDAYS_IN_TERM = {d: n for d, n in NZ_HOLIDAYS.items() if START_DATE <= d <= END_DATE}
num_days = (END_DATE - START_DATE).days + 1
all_dates = [START_DATE + timedelta(days=i) for i in range(num_days)]
weeks = sorted(set(d.isocalendar()[1] for d in all_dates))

# Data preparation
import pandas as pd
data = []
for d in all_dates:
    is_weekend = d.weekday() >= 5
    is_holiday = d in HOLIDAYS_IN_TERM
    data.append({
        "date": d,
        "day": d.strftime("%A"),
        "date_str": d.strftime("%d %b"),
        "is_weekend": is_weekend,
        "is_holiday": is_holiday
    })
df = pd.DataFrame(data)

# Original margins and line height
left_margin = 0.05
right_margin = 0.95
top_margin = 0.98
bottom_margin = 0.02
line_height = (top_margin - bottom_margin) / len(weeks) / 7

# Create figure
fig, ax = plt.subplots(figsize=(fig_width_in, fig_height_in), dpi=300)
ax.axis("off")

# Fill entire page
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# Add title
plt.suptitle(
    TITLE,
    fontsize=20,
    fontweight="bold",
    fontname=FONT_FAMILY,
    ha="center",
    y=0.99
)

# Draw content
y_cursor = top_margin

for week in sorted(set(d.date.isocalendar()[1] for _, d in df.iterrows())):
    week_dates = df[df.date.apply(lambda d: d.isocalendar()[1]) == week]
    for idx, row in week_dates.iterrows():
        y = y_cursor - (row.date.weekday() * line_height)
        
        if row.is_weekend:
            ax.fill_between(
                [left_margin, right_margin],
                [y - line_height / 2]*2,
                [y + line_height / 2]*2,
                color="#e0e0e0",
                zorder=0
            )
        ax.plot(
            [left_margin, right_margin],
            [y - line_height / 2]*2,
            color="#cccccc",
            linewidth=0.5,
            zorder=1
        )
        ax.text(
            left_margin + 0.01,
            y,
            f"{row.day}, {row.date_str}",
            fontsize=8,
            ha="left",
            va="center",
            color="black"
        )
        if row.is_holiday:
            ax.scatter(
                right_margin - 0.01,
                y,
                color="blue",
                s=10,
                zorder=2
            )
    y_cursor -= 7 * line_height

# Save output
pdf_filename = "Term3_2025_Planner_OriginalFullPageWithTitle.pdf"
png_filename = "Term3_2025_Planner_OriginalFullPageWithTitle.png"

plt.savefig(pdf_filename, format="pdf")
plt.savefig(png_filename, format="png")
plt.close(fig)
