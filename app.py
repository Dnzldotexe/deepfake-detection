import streamlit as st


def main() -> None:
    st.info("All user uploaded content is cached only for the current browser session. \
            Data will be deleted when the session is destroyed i.e. closing the tab or refreshing the page.", icon="ℹ️")

    image = st.Page(
        "media/image.py",
        title="Image",
        icon="🖼️",
        default=True
    )
    audio = st.Page(
        "media/audio.py",
        title="Audio",
        icon="🔉",
    )
    video = st.Page(
        "media/video.py",
        title="Video",
        icon="📽️",
    )

    pg = st.navigation(
        {
            "Medium": [image, audio, video],
        }
    )

    pg.run()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Deepfake Detection",
        page_icon="🤖",
        menu_items={
            "See Repository": "https://github.com/Dnzldotexe/deepfake-detection/"
        }
    )

    main()
