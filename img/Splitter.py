from java.awt.image import BufferedImage

def split_image(image, length):
    piece_width = image.getWidth() / length
    piece_height = image.getHeight() / length

    images = []

    for i in range(length):
        for j in range(length):
            split = BufferedImage(piece_width, piece_height, image.getType())
            g = split.createGraphics()
            g.drawImage(image, 0, 0 ,\
                piece_width,\
                piece_height,\
                piece_width * j,\
                piece_height * i,\
                piece_width * j + piece_width,\
                piece_height * i + piece_height,\
                None);
            g.dispose();
            images.append(split)

    return images;
