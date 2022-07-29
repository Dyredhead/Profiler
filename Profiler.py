from PIL import Image, ImageOps, ImageDraw  # type: ignore
import sys
import os


def main() -> Image.Image:
    if (len(sys.argv) > 4):
        print(f"""
            Error @ number of arguments: Not enough arguments

            Expected number of arguments: 2 or 3
            Actual number of arguments: " + {len(sys.args)}
        """)
        sys.exit(1)

    try:
        BackgroundPath: str = sys.argv[1]
        Background: Image.Image = Image.open(BackgroundPath)
    except:
        print("""
            Error @ argument 1: Invalid input file path

            First argument must be a valid path to an image type file
            This image will be used as the application image
        """)
        sys.exit(1)

    try:
        ForegroundPath: str = sys.argv[2]
        Foreground: Image.Image = Image.open(ForegroundPath)
    except:
        print("""
            Error @ argument 2: Invalid input file path

            Second argument must be a valid path to an image type file
            This image will be used as the profile picture
        """)
        sys.exit(1)

    OutputPath = ""
    if (len(sys.argv) == 4):
        OutputPath = sys.argv[3]

    OutputImage: Image.Image = merge(Background, Foreground)
    BackgroundName: str = BackgroundPath.split("/")[-1].split(".")[0]
    ForegroundName: str = ForegroundPath.split("/")[-1].split(".")[0]

    # Keep changing name until valid by appending an incrementing number to the end
    i = 1
    if (OutputPath == ""):
        OutputPath = os.path.expandvars(f"$HOME/Pictures/{BackgroundName}+{ForegroundName}{i}.png")
        while (os.path.exists(OutputPath)):
            OutputPath = OutputPath[:len(OutputPath)-4-len(str(i))] + str(i) + OutputPath[-4:]
            i += 1
    elif OutputPath[-1] == "/":
        OutputPath = os.path.expandvars(f"{OutputPath}{BackgroundName}+{ForegroundName}{i}.png")
        while (os.path.exists(OutputPath)):
            OutputPath = OutputPath[:len(OutputPath)-4-len(str(i))] + str(i) + OutputPath[-4:]
            i += 1
    try: 
        OutputImage.save(OutputPath)
    except:
        print("""
            Error @ argument 3: Invalid output file path

            Third argument must be a valid path to either a directory or a file
            This image will be the output image
        """)

    print("Output image saved to: " + OutputPath)


def merge(Background: Image.Image, Foreground: Image.Image) -> Image.Image:
    BackgroundSize: int = 256
    ForegroundSize: int = 128

    # Resize and convert Background image
    Background = Background.resize((BackgroundSize, BackgroundSize))
    Background = Background.convert("RGBA")
    print("Image of App: ", Background.format, Background.size, Background.mode)

    # Resize and reshape Foreground image into a circular frame
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
