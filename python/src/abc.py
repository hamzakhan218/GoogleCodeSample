import re
from pathlib import Path
import csv

print("Asdasdas")
def test_number_of_videos(capfd):
    player = VideoPlayer()
    player.number_of_videos()
    out, err = capfd.readouterr()
    print(out,"ssfs")
    assert "5 videos in the library" in out

test_number_of_videos(capfd)
def test_show_all_videos(capfd):
    player = VideoPlayer()
    player.show_all_videos()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 6
    assert "Here's a list of all available videos:" in lines[0]
    assert "Amazing Cats (amazing_cats_video_id) [#cat #animal]" in lines[1]
    assert "Another Cat Video (another_cat_video_id) [#cat #animal]" in lines[2]
    assert "Funny Dogs (funny_dogs_video_id) [#dog #animal]" in lines[3]
    assert "Life at Google (life_at_google_video_id) [#google #career]" in lines[4]
    assert "Video about nothing (nothing_video_id) []" in lines[5]


def test_play_video(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 1
    assert "Playing video: Amazing Cats" in out


def test_play_video_nonexistent(capfd):
    player = VideoPlayer()
    player.play_video("does_not_exist")
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 1
    assert "Cannot play video: Video does not exist" in out


def test_play_video_stop_previous(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.play_video("funny_dogs_video_id")
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 3
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Stopping video: Amazing Cats" in lines[1]
    assert "Playing video: Funny Dogs" in lines[2]


def test_play_video_dont_stop_previous_if_nonexistent(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.play_video("some_other_video")
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 2
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Stopping video: Amazing Cats" not in out
    assert "Cannot play video: Video does not exist" in lines[1]


def test_stop_video(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.stop_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 2
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Stopping video: Amazing Cats" in lines[1]


def test_stop_video_twice(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.stop_video()
    player.stop_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 3
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Stopping video: Amazing Cats" in lines[1]
    assert "Cannot stop video: No video is currently playing" in lines[2]


def test_stop_video_none_playing(capfd):
    player = VideoPlayer()
    player.stop_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 1
    assert "Cannot stop video: No video is currently playing" in out


def test_play_random_video(capfd):
    player = VideoPlayer()
    player.play_random_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 1
    assert re.match(
        "Playing video: (Amazing Cats|Another Cat Video|Funny Dogs|Life at Google|Video about nothing)",
        out)


def test_play_random_stops_previous_video(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.play_random_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 3
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Stopping video: Amazing Cats" in lines[1]
    assert re.match(
        "Playing video: (Amazing Cats|Another Cat Video|Funny Dogs|Life at Google|Video about nothing)",
        lines[2])


def test_show_playing(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.show_playing()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 2
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Currently playing: Amazing Cats (amazing_cats_video_id) [#cat #animal]" in lines[1]


def test_show_nothing_playing(capfd):
    player = VideoPlayer()
    player.show_playing()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 1
    assert "No video is currently playing" in lines[0]


def test_pause_video(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.pause_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 2
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Pausing video: Amazing Cats" in lines[1]


def test_pause_video_show_playing(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.pause_video()
    player.show_playing()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 3
    assert "Currently playing: Amazing Cats (amazing_cats_video_id) " \
           "[#cat #animal] - PAUSED" in lines[2]


def test_pause_video_play_video(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.pause_video()
    player.play_video("amazing_cats_video_id")
    player.show_playing()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 5
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Pausing video: Amazing Cats" in lines[1]
    assert "Stopping video: Amazing Cats" in lines[2]
    assert "Playing video: Amazing Cats" in lines[3]
    assert "Currently playing: Amazing Cats (amazing_cats_video_id) " \
           "[#cat #animal]" in lines[4]
    assert "PAUSED" not in lines[4]


def test_pause_already_paused_video(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.pause_video()
    player.pause_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 3
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Pausing video: Amazing Cats" in lines[1]
    assert "Video already paused: Amazing Cats" in lines[2]


def test_pause_video_none_playing(capfd):
    player = VideoPlayer()
    player.pause_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 1
    assert "Cannot pause video: No video is currently playing" in lines[0]


def test_continue_video(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.pause_video()
    player.continue_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 3
    assert "Playing video: Amazing Cats" in lines[0]
    assert "Pausing video: Amazing Cats" in lines[1]
    assert "Continuing video: Amazing Cats" in lines[2]


def test_continue_video_not_paused(capfd):
    player = VideoPlayer()
    player.play_video("amazing_cats_video_id")
    player.continue_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 2
    assert "Cannot continue video: Video is not paused" in lines[1]


def test_continue_none_playing(capfd):
    player = VideoPlayer()
    player.continue_video()
    out, err = capfd.readouterr()
    lines = out.splitlines()
    assert len(lines) == 1
    assert "Cannot continue video: No video is currently playing" in lines[0]




class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._currentVideo=None

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        print(self._video_library.get_all_videos())
        # print("show_all_videos needs implementation")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        name=self._video_library.get_video(video_id)._title()
        if(self._currentVideo!=None):
            self.stop_video()
        if name!=None:
            print("Playing video: ",name)
            self._currentVideo=self._video_library.get_video(video_id)._title()
        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        if self._currentVideo!=None:
            print("Stopping video: ",self._currentVideo)
            self._currentVideo=None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""

        print("play_random_video needs implementation")

    def pause_video(self):
        """Pauses the current video."""

        print("pause_video needs implementation")

    def continue_video(self):
        """Resumes playing the current video."""

        print("continue_video needs implementation")

    def show_playing(self):
        """Displays video currently playing."""

        print("show_playing needs implementation")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("create_playlist needs implementation")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        print("add_to_playlist needs implementation")

    def show_all_playlists(self):
        """Display all playlists."""

        print("show_all_playlists needs implementation")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("show_playlist needs implementation")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        print("remove_from_playlist needs implementation")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("clears_playlist needs implementation")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("deletes_playlist needs implementation")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        print("search_videos needs implementation")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")



# Helper Wrapper around CSV reader to strip whitespace from around
# each item.
def _csv_reader_with_strip(reader):
    yield from ((item.strip() for item in line) for line in reader)


class VideoLibrary:
    """A class used to represent a Video Library."""

    def __init__(self):
        """The VideoLibrary class is initialized."""
        self._videos = {}
        with open(Path(__file__).parent / "videos.txt") as video_file:
            reader = _csv_reader_with_strip(
                csv.reader(video_file, delimiter="|"))
            for video_info in reader:
                title, url, tags = video_info
                self._videos[url] = Video(
                    title,
                    url,
                    [tag.strip() for tag in tags.split(",")] if tags else [],
                )

    def get_all_videos(self):
        """Returns all available video information from the video library."""
        return list(self._videos.values())

    def get_video(self, video_id):
        """Returns the video object (title, url, tags) from the video library.

        Args:
            video_id: The video url.

        Returns:
            The Video object for the requested video_id. None if the video
            does not exist.
        """
        return self._videos.get(video_id, None)


from typing import Sequence


class Video:
    """A class used to represent a Video."""

    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str]):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id

        # Turn the tags into a tuple here so it's unmodifiable,
        # in case the caller changes the 'video_tags' they passed to us
        self._tags = tuple(video_tags)

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title

    @property
    def video_id(self) -> str:
        """Returns the video id of a video."""
        return self._video_id

    @property
    def tags(self) -> Sequence[str]:
        """Returns the list of tags of a video."""
        return self._tags
