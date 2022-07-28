from PIL import Image, ImageOps, ImageDraw  # type: ignore
import sys
import os


def main() -> Image.Image:
    if len(sys.argv) != 3:
        print(f"""
            Error @ number of arguments: Not enough arguments

            Expected number of arguments: 2
            Actual number of arguments: " + {len(sys.args)}
        """)
        sys.exit(1)

    try:
        BackgroundPath: str = sys.argv[1]
        Background: Image.Image = Image.open(BackgroundPath)
    except:
        print("""
            Error @ argument 1: Invalid file path

            First argument must be a valid path to an image type file
            This image will be used as the application image
        """)
        sys.exit(1)

    try:
        ForegroundPath: str = sys.argv[2]
        Foreground: Image.Image = Image.open(ForegroundPath)
    except:
        print("""
            Error @ argument 2: Invalid file path

            Second argument must be a valid path to an image type file
            This image will be used as the profile picture
        """)
        sys.exit(1)

    OutputImage: Image.Image = merge(Background, Foreground)
    BackgroundName: str = os.path.splitext(BackgroundPath)[0]
    ForegroundName: str = os.path.splitext(ForegroundPath)[0]

    # Keep changing name until valid by appending an incrementing number to the end
    i = 1
    name = os.path.expandvars(f"$HOME/Pictures/{BackgroundName}+{ForegroundName}{i}.png")
    while (os.path.exists(name)):
        name = name[:len(name)-4-len(str(i))] + str(i) + name[-4:]
        i += 1

    OutputImage.save(name)
    print("Output image saved to: " + name)


def merge(Background: Image.Image, Foreground: Image.Image) -> Image.Image:
    BackgroundSize: int = 256
    ForegroundSize: int = 128

    # Resize and convert Background image
    Background = Background.resize((BackgroundSize, BackgroundSize))
    Background = Background.convert("RGBA")
    print("Image of App: ", Background.format, Background.size, Background.mode)

    # Reshape Foreground image into a circular frame
    print("Image of Profile: ", Foreground.format, Foreground.size, Foreground.mode)
    size = (128, 128)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    Foreground = ImageOps.fit(Foreground, mask.size, centering=(0.5, 0.5))
    Foreground.putalpha(mask)
    #Foreground.save("output.png")
    #Foreground.convert('P', palette=Image.ADAPTIVE)

    # Merge Image of App and Image of Profile into one Image
    OutputImage: Image.Image = Image.new("RGBA", Background.size)
    OutputImage = Image.alpha_composite(Background, Background)
    OutputImage.paste(Background)
    OutputImage.paste(Foreground, (Background.width - Foreground.width, 0), Foreground)
    return OutputImage


if __name__ == "__main__":
    main()
    sys.exit(0)
