def define_env(env):
    """
    Define custom macros for MkDocs
    """

    @env.macro
    def h5p_lumi_embed(container_id, html_path, width="100%", height="600px", base_url=None):
        """
        Embed a Lumi H5P iframe with optional base URL support.
        """
        # Get base_url from MkDocs config if not provided
        if base_url is None:
            base_url = env.config.get('extra', {}).get('base_url', '')

        # Construct the full path
        full_path = f"{base_url}/{html_path.lstrip('/')}" if base_url else f"/{html_path.lstrip('/')}"

        # Return the iframe HTML
        return f'<iframe id="{container_id}" src="{full_path}" width="{width}" height="{height}" frameborder="0" allowfullscreen></iframe>'

    @env.macro
    def image_block(src, alt_text="", caption="", source_text="", source_url="", size="medium", width=None):
        """
        Generates a styled image figure with caption and source reference.

        Args:
            src (str): Image path or URL.
            alt_text (str): Alt text for the image.
            caption (str): Caption displayed below the image.
            source_text (str): Text to display for image source.
            source_url (str): Hyperlink for image source.
            size (str): One of 'small', 'medium', or 'large' (default: medium).
            width (str): Optional custom width (e.g. '80%' or '400px').
        """

        # Default widths
        size_map = {
            "small": "40%",
            "medium": "60%",
            "large": "80%"
        }

        # Determine final width
        img_width = width if width else size_map.get(size, "60%")

        html = f"""
<figure markdown="span">
    <img src="{src}" alt="{alt_text}" width="{img_width}">
    <figcaption>{caption}</figcaption>
    <p align='right' style="font-size:0.8em">
        <i>Image Source: <a href="{source_url}" target="_blank">{source_text}</a></i>
    </p>
</figure>
"""
        return html
