from PIL import Image, ImageDraw, ImageFilter

def draw_drop_shadow(base_image, offset=(10, 10), shadow_color=(0, 0, 0, 128), blur_radius=10):
    """Draws a drop shadow behind the given image."""
    shadow = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle((0, 0, base_image.width, base_image.height), fill=shadow_color)

    blurred_shadow = shadow.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    shadow_offset = Image.new('RGBA', (base_image.width + abs(offset[0]) * 2, base_image.height + abs(offset[1]) * 2), (0, 0, 0, 0))
    shadow_offset.paste(blurred_shadow, (abs(offset[0]), abs(offset[1])))

    #Can probably be dropped
    final_shadow = Image.new('RGBA', shadow_offset.size, (0, 0, 0, 0))
    final_shadow.paste(shadow_offset, (0, 0))

    return final_shadow

def generate_wallpaper(resolution, image_paths, bg_color):
    width_res, height_res = resolution
    num_images = len(image_paths)

    if not 1 <= num_images <= 10:
        raise ValueError("Number of images must be between 1 and 10.")
    # Math... Basically take the Wallpaper Width/Height, calculate what the appropriate size of the posters should be
    # Horizontal gaps between images are set to be 1/16 the size of the images
    # Gaps between the images and the edges of the wallpaper are set to be at least double the size of the inner gaps
    # At least one side has to give. The vertical or the horizontal edge gaps
    # The vertical_gap was chosen arbitrairly as the baseline for comparison

    if num_images > 0:
        inner_gap_horizontal_ver = width_res / (3 + (17 * num_images))
        vertical_gap_horizontal_ver = 2 * inner_gap_horizontal_ver
        vertical_gap_vertical_ver = height_res/(2 + (8*26/19))

        if vertical_gap_horizontal_ver < vertical_gap_vertical_ver:
            inner_gap = inner_gap_horizontal_ver
            image_width = inner_gap * 16
            vertical_gap = vertical_gap_horizontal_ver
            image_height = (29/19) * image_width

        else:
            vertical_gap = vertical_gap_vertical_ver
            inner_gap = vertical_gap / 2
            image_height = vertical_gap * 26 * 8 / 19
            image_width = image_height * 19 / 29

    wallpaper = Image.new('RGB', resolution, bg_color)
    shadow_offset = (int(inner_gap / 8), int(inner_gap / 8))
    shadow_color = (0, 0, 0, 128)
    blur_radius = int(inner_gap / 8)

    if num_images > 0:
        total_images_width = num_images * image_width
        total_inner_gaps_width = (num_images - 1) * inner_gap
        horizontal_available_space = width_res - total_images_width - total_inner_gaps_width
        horizontal_outer_gap = horizontal_available_space / 2
        vertical_available_space = height_res - image_height
        vertical_outer_gap = vertical_available_space / 2

        y_position = vertical_outer_gap
        x_position = horizontal_outer_gap

        for path in image_paths:
            try:
                img = Image.open(path).convert("RGBA")
                resized_img = img.resize((int(image_width), int(image_height)))

                # Draw drop shadow
                shadow = draw_drop_shadow(resized_img, offset=shadow_offset, shadow_color=shadow_color, blur_radius=blur_radius)
                wallpaper.paste(shadow, (int(x_position) + shadow_offset[0], int(y_position) + shadow_offset[1]), shadow)

                # Paste the actual image
                wallpaper.paste(resized_img, (int(x_position), int(y_position)), resized_img)

                x_position += image_width + inner_gap
            except FileNotFoundError:
                print(f"Error: Image not found at {path}")
                # Handle error as needed

    return wallpaper