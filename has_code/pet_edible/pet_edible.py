"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config
from reflex_webcam import webcam, upload_screenshot
import reflex as rx

import time
from pathlib import Path
from urllib.request import urlopen
from PIL import Image

# Identifies a particular webcam component in the DOM
WEBCAM_REF = "webcam"

docs_url = "https://reflex.dev/docs/getting-started/introduction/"
filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    """The app state."""
    last_screenshot: Image.Image | None = None
    last_screenshot_timestamp: str = ""
    loading: bool = False
    webcam_open: bool = False
    if_img: bool = False

    def img_taken(self):
        self.if_img = not self.if_img

    def toggle_webcam(self):
        self.webcam_open = not self.webcam_open

    def handle_screenshot(self, img_data_uri: str):
        """Webcam screenshot upload handler.
        Args:
            img_data_uri: The data uri of the screenshot (from upload_screenshot).
        """
        if self.loading:
            return
        self.last_screenshot_timestamp = time.strftime("%H:%M:%S")
        with urlopen(img_data_uri) as img:
            self.last_screenshot = Image.open(img)
            self.last_screenshot.load()
            # convert to webp during serialization for smaller size
            self.last_screenshot.format = "WEBP"  # type: ignore
            self.webcam_open=False
            self.if_img=True

def last_screenshot_widget() -> rx.Component:
    """Widget for displaying the last screenshot and timestamp."""
    return rx.box(
        rx.cond(
            State.last_screenshot,
            rx.fragment(
                rx.image(src=State.last_screenshot),
                rx.text(State.last_screenshot_timestamp),
            ),

        ),
        height="270px",
    )


def webcam_upload_component(ref: str) -> rx.Component:
    """Component for displaying webcam preview and uploading screenshots.
    Args:
        ref: The ref of the webcam component.
    Returns:
        A reflex component.
    """
    return rx.vstack(
        webcam.webcam(
            id=ref,
            on_click=webcam.upload_screenshot(
                ref=ref,
                handler=State.handle_screenshot,  # type: ignore
            ),
            width="720px",
            height="1280px",
        ),
        last_screenshot_widget(),
        #width="320px",
        align="center",
    )



def index() -> rx.Component:
    return rx.fragment(
            rx.center(
                # this stack is home page
                rx.vstack(
                    rx.heading("Can my dog eat this?", size="9"),
                    rx.code(rx.text("Check what your dog can eat")),
                    rx.button(
                        "Take image",
                        on_click= State.toggle_webcam(),
                        size="4",
                    ),

                    # this stack is webcam page
                    # event handler for Take image button
                    rx.cond(
                        State.webcam_open,
                        rx.vstack(
                            # webcam display
                            webcam(
                                id="webcam",
                                border_radius = "10%",),
                            # this is the click button
                            rx.button(
                                width="60px", 
                                height="60px", 
                                border_radius="100%",
                                on_click=upload_screenshot(
                                    ref="webcam",
                                    handler=State.handle_screenshot,  # type: ignore
                                ),
                            ),
                            align= "center",
                            width = "100%",
                        ),
                        rx.cond(
                            State.if_img,
                            rx.vstack(
                                rx.hstack(
                                rx.box(
                                    rx.fragment(
                                        rx.button(
                                            "Save",
                                            size = "4",
                                        ),
                                        align = "left",
                                    ),
                                ),
                                
                                rx.box(
                                    rx.fragment(
                                        rx.button(
                                            "Retake",
                                            size = "4",
                                        ),
                                        align = "right",
                                    ),
                                ),
                                width = "100%",
                                justify="between",
                            ),
                            last_screenshot_widget(),
                            width = "100%",
                            ),
                        )
                        
                    ),
                    align="center",
                    spacing="7",
                    font_size="2em",
                ),
                height="100vh",
    )
    )


app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="large",
        accent_color="brown",
    ),
    )
app.add_page(index)
