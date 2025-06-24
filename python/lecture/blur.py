from PIL import Image, ImageFilter

before = Image.open("Example.jpg")
after = before.filter(ImageFilter.GaussianBlur(radius=6))
after.save("out.jpg")
