from datetime import datetime
from collections import defaultdict

mvp_counter = defaultdict(int)

# Pre-made titles
MONTH_TITLES = {
    "January": "Winter’s January Highlights",
    "February": "Winter’s February Highlights",
    "March": "Winter’s March Highlights",
    "April": "Winter’s April Highlights",
    "May": "Winter’s May Highlights",
    "June": "Winter’s June Highlights",
    "July": "Winter’s July Highlights",
    "August": "Winter’s August Highlights",
    "September": "Winter’s September Highlights",
    "October": "Winter’s October Highlights",
    "November": "Winter’s November Highlights",
    "December": "Winter’s December Highlights"
}

# Map for abbreviated month input
MONTH_MAP = {
    "jan": "January",
    "january": "January",
    "feb": "February",
    "february": "February",
    "mar": "March",
    "march": "March",
    "apr": "April",
    "april": "April",
    "may": "May",
    "jun": "June",
    "june": "June",
    "jul": "July",
    "july": "July",
    "aug": "August",
    "august": "August",
    "sep": "September",
    "september": "September",
    "oct": "October",
    "october": "October",
    "nov": "November",
    "november": "November",
    "dec": "December",
    "december": "December"
}

# Optional intro templates
MONTH_INTRO = {
    "default": "Hello @Winter,\nIt was another busy month in OSRS, Here's the rundown of what our clan got up to this month! ❄️"
}

# Recap goodbye message
GOODBYE_MESSAGE = "\n\nTo ensure your amazing drops and achievements are included in our monthly recap, please post them in the #osrs-showcase channel.\nBest of luck with your drops and achievements in the upcoming month!! :WinterGif::Winter:"

def get_month():
    while True:
        raw = input("Which month is the recap for? ").strip().lower()

        month = MONTH_MAP.get(raw)

        if month:
            return month

        print("Invalid month. Try again (e.g. jan or January).")

def get_title_and_intro(month):
    title = MONTH_TITLES.get(month, f"{month} — Winter's Monthly Highlights")
    intro = MONTH_INTRO.get(month, MONTH_INTRO["default"])
    return title, intro


def flush_pets(output_lines, pets_buffer, pets_count):
    output_lines.append(f"Winter achieved a total of **{pets_count}** pets this month!")
    for pet in sorted(pets_buffer, key=str.lower):
        output_lines.append(pet)
    pets_buffer.clear()


def process_entry_line(line, current_section, output_lines, pets_buffer):
    title, users = line.split(":", 1)

    user_list = [u.strip() for u in users.split(",") if u.strip()]
    tagged_users = [f"@{u}" for u in user_list]

    if current_section == "Pets":
        for u in user_list:
            mvp_counter[u] += 1

    formatted_line = f"- {title.strip()}: {', '.join(tagged_users)}"

    if current_section == "Pets":
        pets_buffer.append(formatted_line)
        return len(user_list)
    else:
        output_lines.append(formatted_line)
        return 0


def build_mvp_section():
    if not mvp_counter:
        return []

    max_score = max(mvp_counter.values())
    mvps = [u for u, c in mvp_counter.items() if c == max_score]

    section = ["\n**MVP of the Month 🏆**"]
    for mvp in sorted(mvps, key=str.lower):
        section.append(f"- @{mvp} ({max_score} pets)")
    section.append("")
    return section


def write_output(output_file, output_lines):
    # Combine everything in one string first
    full_text = "\n".join(output_lines).strip() + GOODBYE_MESSAGE
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_text)

def build_output_filename(month):
    year = datetime.now().year
    return f"recap_{month}_{year}.txt"        


def format_recap(input_file, output_file, month):

    print(f"Generating recap for {month}...")
    title, intro = get_title_and_intro(month)

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    output_lines = [f"**{title}**\n", intro]

    pets_buffer = []
    pets_count = 0
    current_section = None

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        if line.endswith(":"):
            if current_section == "Pets":
                flush_pets(output_lines, pets_buffer, pets_count)
                pets_count = 0

            current_section = line[:-1]
            output_lines.append(f"\n**{line}**")
            continue

        if ":" in line:
            pets_count += process_entry_line(
                line, current_section, output_lines, pets_buffer
            )

    if current_section == "Pets":
        flush_pets(output_lines, pets_buffer, pets_count)

    # output_lines.extend(build_mvp_section())
    write_output(output_file, output_lines)
    print("Recap formatting complete.")

def main():
    month = get_month()
    output_file = build_output_filename(month)
    format_recap("recap_input.txt", output_file, month)


if __name__ == "__main__":
    main()
