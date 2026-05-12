from datetime import datetime

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
    "sept": "September",
    "september": "September",
    "oct": "October",
    "october": "October",
    "nov": "November",
    "november": "November",
    "dec": "December",
    "december": "December"
}

INTRO_MESSAGE = "Hello @Winter,\nIt was another busy month in OSRS, Here's the rundown of what our clan got up to this month! ❄️"

GOODBYE_MESSAGE = "\n\nTo ensure your amazing drops and achievements are included in our monthly recap, please post them in the #osrs-showcase channel.\nBest of luck with your drops and achievements in the upcoming month!! :WinterGif::Winter:"

def get_month():
    while True:
        raw = input("Which month is the recap for? ").strip().lower()

        month = MONTH_MAP.get(raw)

        if month:
            return month

        print("Invalid month. Try again (e.g. jan or January).")

def get_title_and_intro(month):
    title = f"Winter’s {month} Highlights"
    return title, INTRO_MESSAGE

def flush_pets(output_lines, pets_buffer, pets_count):
    output_lines.append(f"Winter achieved a total of **{pets_count}** pets this month!")
    for pet in sorted(pets_buffer, key=str.lower):
        output_lines.append(pet)
    pets_buffer.clear()

def process_entry_line(line, current_section, output_lines, pets_buffer):
    title, users = line.split(":", 1)

    user_list = [u.strip() for u in users.split(",") if u.strip()]
    tagged_users = [f"@{u}" for u in user_list]

    formatted_line = f"- {title.strip()}: {', '.join(tagged_users)}"

    if current_section == "Pets":
        pets_buffer.append(formatted_line)
        return len(user_list)
    else:
        output_lines.append(formatted_line)
        return 0

def write_output(output_file, output_lines):
    full_text = "\n".join(output_lines).strip() + GOODBYE_MESSAGE
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_text)

def build_output_filename(month):
    year = datetime.now().year
    return f"recap_{month.lower()}_{year}.txt"        

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

    write_output(output_file, output_lines)
    print("Recap formatting complete.")

def main():
    month = get_month()
    output_file = build_output_filename(month)
    format_recap("recap_input.txt", output_file, month)


if __name__ == "__main__":
    main()
