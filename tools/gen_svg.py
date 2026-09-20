#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the profile README's SVG assets, one file per theme.

Run it from anywhere after editing the data below:

    python3 tools/gen_svg.py

Grades are the 42 intra grades; anything above 100 includes bonus work.
Each CPP module counts as one project.
"""
import os

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# --------------------------------------------------------------- the data ---
GRADES = {
    0: [120],                                    # libft
    1: [100, 112, 125],                          # ft_printf, get_next_line, born2beroot
    2: [120, 125, 104, 100],                     # fdf, minitalk, push_swap, Exam Rank 02
    3: [115, 100, 100],                          # minishell, philosophers, Exam Rank 03
    4: [115, 100] + [100] * 5 + [100],           # cub3d, netpractice, CPP00-04, Exam Rank 04
    5: [100, 125] + [100] * 4 + [100],   # ft_irc, inception, CPP05-08, Exam Rank 05
}
# Projects per rank, exams included: rank 2 through 6 each carry one exam.
TOTALS = {0: 1, 1: 3, 2: 4, 3: 3, 4: 8, 5: 8, 6: 3}
CURRENT_RANK = 5
IN_PROGRESS = "CPP09 \u00b7 ft_transcendence \u00b7 FT_Resume"
SIDE_PROJECT = "Coming soon..."
TAGLINE = "I build things that live close to the machine \u2014 shells, servers, renderers."
STACK_LINE = "C · C++ · Go · Python · PHP · Docker · Linux"

DONE = sum(len(v) for v in GRADES.values())
MEAN = round(sum(sum(v) for v in GRADES.values()) / DONE)
LEFT_IN_RANK = TOTALS[CURRENT_RANK] - len(GRADES[CURRENT_RANK])

THEMES = {
    "dark": dict(
        BG="#0D1117", BORDER="#30363D", FG="#E6EDF3", MUTED="#8B949E",
        FAINT="#6E7681", ACCENT="#58A6FF", SUCCESS="#3FB950", TODO="#30363D",
    ),
    "light": dict(
        BG="#FFFFFF", BORDER="#D0D7DE", FG="#1F2328", MUTED="#656D76",
        FAINT="#818B98", ACCENT="#0969DA", SUCCESS="#1A7F37", TODO="#D8DEE4",
    ),
}


# ----------------------------------------------------------------- banner ---
def banner(t):
    stats = [
        ("PROJECTS VALIDATED", str(DONE)),
        ("AVERAGE GRADE", str(MEAN)),
        ("CURRENT RANK", "%d / 6" % CURRENT_RANK),
    ]
    rows, y = [], 104
    for i, (label, value) in enumerate(stats):
        rows.append(
            '<text x="884" y="%d" font-family="%s" font-size="11" letter-spacing="2.2" '
            'fill="%s">%s</text>'
            '<text x="1144" y="%d" text-anchor="end" font-family="%s" font-size="27" '
            'font-weight="700" fill="%s">%s</text>'
            % (y, MONO, t["MUTED"], label, y + 4, SANS, t["FG"], value)
        )
        if i < len(stats) - 1:
            rows.append('<line x1="884" y1="%d" x2="1144" y2="%d" stroke="%s" stroke-width="1"/>'
                        % (y + 26, y + 26, t["BORDER"]))
        y += 56

    return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 280" width="1200" height="280" role="img"
     aria-labelledby="t d">
  <title id="t">Nikola &#8212; 42 Paris student, systems and backend developer</title>
  <desc id="d">%d projects validated, average grade %d out of 100, currently rank %d of 6.</desc>

  <rect x="0.5" y="0.5" width="1199" height="279" rx="10" fill="%s" stroke="%s"/>
  <line x1="840" y1="48" x2="840" y2="232" stroke="%s" stroke-width="1" opacity="0.55"/>

  <text x="56" y="68" font-family="%s" font-size="12.5" letter-spacing="3.4" fill="%s">42 PARIS &#8212; &#206;LE-DE-FRANCE</text>

  <text x="54" y="150" font-family="%s" font-size="70" font-weight="700" letter-spacing="2"
        fill="%s">NIKOLA<tspan fill="%s">.</tspan></text>

  <rect x="56" y="176" width="124" height="3" rx="1.5" fill="%s">
    <animate attributeName="width" from="0" to="124" dur="0.8s" begin="0.2s" fill="freeze"/>
  </rect>

  <text x="56" y="214" font-family="%s" font-size="17.5" fill="%s">%s</text>
  <text x="56" y="240" font-family="%s" font-size="13" fill="%s">%s</text>

  <g>
    %s
  </g>
</svg>
''' % (DONE, MEAN, CURRENT_RANK, t["BG"], t["BORDER"], t["BORDER"],
       MONO, t["MUTED"], SANS, t["FG"], t["ACCENT"], t["ACCENT"],
       SANS, t["MUTED"], TAGLINE, MONO, t["FAINT"], STACK_LINE,
       "\n    ".join(rows))


# ----------------------------------------------------------------- cursus ---
def cursus(t):
    pad, gap, n = 56, 12, len(TOTALS)
    seg = (1200 - pad * 2 - gap * (n - 1)) / float(n)
    top, h = 112, 16
    parts = []
    for i in range(n):
        total = TOTALS[i]
        done = len(GRADES.get(i, []))
        x = pad + i * (seg + gap)
        frac = done / float(total)
        color = t["SUCCESS"] if frac == 1 else (t["ACCENT"] if frac > 0 else t["TODO"])
        parts.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" rx="%s" fill="%s"/>'
                     % (x, top, seg, h, h / 2.0, t["TODO"]))
        if frac > 0:
            w = seg * frac
            parts.append(
                '<rect x="%.1f" y="%d" width="%.1f" height="%d" rx="%s" fill="%s">'
                '<animate attributeName="width" from="0" to="%.1f" dur="0.9s" begin="%.2fs" fill="freeze"/>'
                '</rect>' % (x, top, w, h, h / 2.0, color, w, 0.15 + i * 0.07)
            )
        parts.append(
            '<text x="%.1f" y="%d" font-family="%s" font-size="13" fill="%s">'
            '<tspan font-weight="700">R%d</tspan>'
            '<tspan dx="11" font-size="12" fill="%s">%d/%d</tspan></text>'
            % (x, top + 44, MONO, t["FG"] if frac > 0 else t["FAINT"], i, t["MUTED"], done, total)
        )

    return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" width="1200" height="300" role="img"
     aria-labelledby="ct cd">
  <title id="ct">42 cursus progress</title>
  <desc id="cd">Ranks 0 to 4 complete. Rank %d at %d of %d projects. Rank 6 not started.</desc>

  <rect x="0.5" y="0.5" width="1199" height="299" rx="10" fill="%s" stroke="%s"/>

  <text x="56" y="62" font-family="%s" font-size="12.5" letter-spacing="3.4" fill="%s">42 CURSUS</text>
  <text x="1144" y="62" text-anchor="end" font-family="%s" font-size="12.5" letter-spacing="1.4"
        fill="%s">%d VALIDATED &#183; MEAN %d/100</text>
  <line x1="56" y1="80" x2="1144" y2="80" stroke="%s" stroke-width="1"/>

  <g>
    %s
  </g>

  <line x1="56" y1="204" x2="1144" y2="204" stroke="%s" stroke-width="1"/>

  <text x="56" y="234" font-family="%s" font-size="11" letter-spacing="2.2" fill="%s">IN PROGRESS</text>
  <text x="56" y="262" font-family="%s" font-size="17" fill="%s">%s</text>

  <text x="1144" y="234" text-anchor="end" font-family="%s" font-size="11" letter-spacing="2.2"
        fill="%s">ALSO BUILDING</text>
  <text x="1144" y="262" text-anchor="end" font-family="%s" font-size="17" fill="%s">%s</text>
</svg>
''' % (CURRENT_RANK, len(GRADES[CURRENT_RANK]), TOTALS[CURRENT_RANK],
       t["BG"], t["BORDER"], MONO, t["MUTED"], MONO, t["FAINT"], DONE, MEAN, t["BORDER"],
       "\n    ".join(parts), t["BORDER"],
       MONO, t["MUTED"], SANS, t["FG"], IN_PROGRESS,
       MONO, t["MUTED"], SANS, t["FG"], SIDE_PROJECT)


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "assets")
    os.makedirs(out, exist_ok=True)
    for name, fn in (("banner", banner), ("cursus", cursus)):
        for theme, tokens in THEMES.items():
            path = os.path.join(out, "%s-%s.svg" % (name, theme))
            with open(path, "w") as f:
                f.write(fn(tokens))
            print("wrote", os.path.relpath(path, root))
    print("%d projects validated, mean %d, %d left in rank %d"
          % (DONE, MEAN, LEFT_IN_RANK, CURRENT_RANK))
