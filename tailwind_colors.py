import requests
from datetime import datetime
import re


def clean_shade_strings(s):
    shade_number = s.split(":")[0].strip()
    shade_hex = "".join(s.split("#")[1].split("'")[0])
    return shade_number, shade_hex


def main():
    f = open("tailwindcolors.sty", "w")

    f.write("% ---------------------------------------------------------------\n")
    f.write("% TEX TAILWIND COLORS\n")
    f.write("% ---------------------------------------------------------------\n")
    f.write("% tailwindcolors.sty\n")
    f.write(f"% {datetime.now().strftime('%B')} {datetime.now().year}\n\n")
    f.write("% The default color definitions of Tailwind CSS\n")
    f.write("% Automatically generated by tailwind_colors.py\n")
    f.write("% github.com/duncan-christie/tex-tailwind-colors\n")
    f.write("% ---------------------------------------------------------------\n\n")

    base_colors = [
        "slate",
        "gray",
        "zinc",
        "neutral",
        "stone",
        "red",
        "orange",
        "amber",
        "yellow",
        "lime",
        "green",
        "emerald",
        "teal",
        "cyan",
        "sky",
        "blue",
        "indigo",
        "violet",
        "purple",
        "fuchsia",
        "pink",
        "rose",
    ]
    url = "https://raw.githubusercontent.com/tailwindlabs/tailwindcss/master/src/public/colors.js"

    res = requests.get(url)
    content = res.text

    for base_color in base_colors:
        f.write(f"% {base_color.capitalize()}\n")

        # parse color strings
        raw_color_string = re.findall(
            re.escape(base_color) + r":(.*?)},", content, re.DOTALL
        )
        raw_shades = re.findall(r"\n.*?,", raw_color_string[0], re.DOTALL)
        shades = [clean_shade_strings(shade) for shade in raw_shades]

        for shade in shades:
            f.write(f"\definecolor{{{base_color}-{shade[0]}}}{{HTML}}{{{shade[1]}}}\n")

        f.write("\n")

    f.close()


if __name__ == "__main__":
    main()
