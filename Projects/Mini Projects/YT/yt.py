"""This script fetches video details from a YouTube playlist URL using yt-dlp.
    It extracts video links and durations, and saves the details to a CSV file.
    It also calculates the total duration of the playlist.
"""

import datetime

import pandas as pd
import yt_dlp


def fetch_playlist_info(url):
    """Fetch video details from the playlist URL using yt-dlp."""
    ydl_opts = {
        'extract_flat': True,
        'force_generic_extractor': True,
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            if 'entries' in result:
                return result['entries']
            else:
                print("Failed to fetch playlist information.")
                return []
    except yt_dlp.DownloadError as e:
        print(f"An error occurred: {e}")
        return []

def convert_to_timedelta(duration_seconds):
    """Convert duration in seconds to timedelta."""
    return datetime.timedelta(seconds=duration_seconds)

def calculate_total_duration(durations):
    """Calculate the total duration from a list of timedelta objects."""
    return sum(durations, datetime.timedelta())

if __name__ == '__main__':
    playlist_url = input("Enter the YouTube playlist URL: ")

    # Fetch playlist information
    entries = fetch_playlist_info(playlist_url)

    if not entries:
        print("No video details were found.")
    else:
        # Extract video links and durations
        video_links = [entry['url'] for entry in entries if 'url' in entry]
        video_durations = [convert_to_timedelta(entry['duration']) for entry in entries if 'duration' in entry]

        if not video_links or not video_durations:
            print("No video links or durations were found.")
        else:
            # Create DataFrame to store video details
            playlist_df = pd.DataFrame({
                'Video Link': video_links,
                'Duration': [str(d) for d in video_durations]  # Convert timedelta to string
            })

            # Save DataFrame to a CSV file
            playlist_df.to_csv('youtube_playlist_videos.csv', index=False)

            # Calculate total duration of the playlist
            total_duration = calculate_total_duration(video_durations)

            print(f"Total time to watch the playlist: {total_duration}")
            print("Playlist details saved to 'youtube_playlist_videos.csv'.")
