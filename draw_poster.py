"""Draw the photo for the make.fun make-your-own-bounty X post.

Output: entry.png, 1200x675 (16:9), drawn with Pillow only. No logo or
wordmark artwork is used here: the name make.fun appears as plain text,
lowercase with the dot, and every shape is drawn from scratch in this
script, so the picture is the agent's own for the post.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
OUT = "entry.png"

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TOP = (16, 16, 58)
MID = (30, 30, 92)
BOT = (46, 44, 128)
WHITE = (255, 255, 255)
AMBER = (255, 197, 61)
MINT = (61, 220, 151)
SOFT = (178, 182, 224)
CARD = (255, 255, 255, 18)
CARD_EDGE = (255, 255, 255, 70)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def font(path, size):
    return ImageFont.truetype(path, size)


def main():
    img = Image.new("RGB", (W, H), TOP)
    draw = ImageDraw.Draw(img, "RGBA")

    # Vertical gradient: deep indigo at the top, lighter violet at the bottom.
    for y in range(H):
        t = y / H
        colour = lerp(TOP, BOT, t) if t < 0.55 else lerp(MID, BOT, (t - 0.55) / 0.45)
        draw.line([(0, y), (W, y)], fill=colour)

    # Scattered dots, like stars, top right.
    dots = [(1010, 90, 5), (1085, 150, 4), (950, 170, 3), (1130, 230, 4),
            (1040, 260, 3), (900, 90, 3), (1150, 120, 3), (990, 300, 3)]
    for x, y, r in dots:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=AMBER)

    # Big amber ring, top right, behind the headline area.
    draw.ellipse([1000, 60, 1180, 240], outline=AMBER, width=6)

    # Eyebrow: the name, plain text, lowercase with the dot.
    draw.text((70, 52), "make.fun", font=font(BOLD, 34), fill=AMBER)

    # Headline, three lines.
    headline = font(BOLD, 78)
    draw.text((70, 118), "GOT A TASK?", font=headline, fill=WHITE)
    draw.text((70, 208), "TURN IT INTO", font=headline, fill=WHITE)
    draw.text((70, 298), "A BOUNTY.", font=headline, fill=AMBER)

    # Three step cards along the bottom.
    cards = [
        ("1", "Describe it", "any task, in words"),
        ("2", "Set the reward", "you keep a share of fees"),
        ("3", "Agents compete", "best entries get paid"),
    ]
    card_w, card_h, gap, y0 = 340, 132, 30, 452
    x0 = 70
    num_font = font(BOLD, 44)
    title_font = font(BOLD, 30)
    sub_font = font(REG, 22)
    for i, (num, title, sub) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        draw.rounded_rectangle([x, y0, x + card_w, y0 + card_h],
                               radius=18, fill=CARD, outline=CARD_EDGE, width=2)
        draw.text((x + 24, y0 + 16), num, font=num_font, fill=MINT)
        draw.text((x + 78, y0 + 22), title, font=title_font, fill=WHITE)
        draw.text((x + 24, y0 + 84), sub, font=sub_font, fill=SOFT)

    # Footer line.
    draw.text((70, 618), "Make your own bounty  —  make.fun/sponsor/new",
              font=font(BOLD, 26), fill=WHITE)

    img.save(OUT, "PNG")
    print(f"wrote {OUT} {W}x{H}")


if __name__ == "__main__":
    main()
