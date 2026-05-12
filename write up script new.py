# RECAP WRITE UP SCRIPT
import datetime
from collections import defaultdict

mvp_counter = defaultdict(int)
month = datetime.datetime.now().strftime("%B")

# Pre-made titles
MONTH_TITLES = {
    "January": "January's Chilled Conquests: Winter's Monthly Highlights",
    "February": "February's Glacial Gains: Winter's Monthly Highlights",
    "March": "March's Icy Illumination: Winter's Monthly Highlights",
    "April": "April's Frostbitten Feats: Winter's Monthly Highlights",
    "May": "May's Snowbound Success: Winter's Monthly Highlights",
    "June": "June's Arctic Accolades: Winter's Monthly Highlights",
    "July": "July's Polar Prosperity: Winter's Monthly Highlights",
    "August": "August's Frozen Fables: Winter's Monthly Highlights",
    "September": "September's Winter Wonderland: Winter's Monthly Highlights",
    "October": "October's Blizzard Bounty: Winter's Monthly Highlights",
    "November": "November's Icy Success: Winter's Monthly Highlights",
    "December": "December's Frosty Fortunes: Winter's Monthly Highlights"
}

# Optional intro templates
MONTH_INTRO = {
    "default": "Hello @Winter,\nAnother busy month in OSRS, Here's the rundown of what our clan got up to this month! ❄️"
}

# Recap goodbye message
GOODBYE_MESSAGE = "\n\nTo ensure your amazing drops and achievements are included in our monthly recap, please post them in the #osrs-showcase channel.\nBest of luck with your drops and achievements in the upcoming month!! :WinterGif::Winter:"


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


def format_recap(input_file, output_file, month=month):
    # if month is None:
    #     month = datetime.datetime.now().strftime("%B")

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


if __name__ == "__main__":
    format_recap("recap_input.txt", "recap_output.txt")
