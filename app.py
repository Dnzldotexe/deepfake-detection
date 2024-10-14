import streamlit as st


def main() -> None:
    st.info("We do not store any user uploaded content in this site. You can verify by clicking the GitHub icon.", icon="ℹ️")

    image = st.Page(
        "media/image.py",
        title="Detect Image",
        icon="🖼️",
        default=True
    )
    audio = st.Page(
        "media/audio.py",
        title="Detect Audio",
        icon="🔉",
    )
    video = st.Page(
        "media/video.py",
        title="Detect Video",
        icon="📽️",
    )

    pg = st.navigation(
        {
            "Media": [image, audio, video],
        }
    )

    pg.run()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Deepfake Detection",
        page_icon="🤖", 
    )

    main()