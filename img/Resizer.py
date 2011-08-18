from java.awt import AlphaComposite, Graphics2D, RenderingHints
from java.awt.image import BufferedImage

def resize_image(original_image, width, height):
    resized_image = BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB)
    g = resized_image.createGraphics()
    g.drawImage(original_image, 0, 0, width, height, None)
    g.dispose();
    return resized_image
