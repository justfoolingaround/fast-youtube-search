from .channel import from_channel_renderer
from .playlist import from_playlist_renderer
from .show import from_show_renderer
from .video import from_video_renderer

from .utils import get_text


def iter_from_item_section_renderer(data: dict):

    attrs = {}

    def genexp(attrs=attrs):

        for renderer_shelf in data["contents"]:

            if "showingResultsForRenderer" in renderer_shelf:
                attrs.update(
                    {
                        "showing_results_for": get_text(
                            renderer_shelf["showingResultsForRenderer"][
                                "correctedQuery"
                            ],
                            runs_joiner="",
                        )
                    }
                )

            if "didYouMeanRenderer" in renderer_shelf:
                attrs.update(
                    {
                        "did_you_mean": get_text(
                            renderer_shelf["didYouMeanRenderer"]["correctedQuery"],
                            runs_joiner="",
                        ),
                    }
                )

            if "videoRenderer" in renderer_shelf:
                yield {
                    "type": "video",
                    "content": from_video_renderer(renderer_shelf["videoRenderer"]),
                }

            if "channelRenderer" in renderer_shelf:
                yield {
                    "type": "channel",
                    "content": from_channel_renderer(renderer_shelf["channelRenderer"]),
                }

            if "playlistRenderer" in renderer_shelf:
                yield {
                    "type": "playlist",
                    "content": from_playlist_renderer(
                        renderer_shelf["playlistRenderer"]
                    ),
                }

            if "showRenderer" in renderer_shelf:
                yield {
                    "type": "show",
                    "content": from_show_renderer(renderer_shelf["showRenderer"]),
                }

    for component in genexp():
        component.update(
            {
                "attrs": attrs,
            }
        )
        yield component
