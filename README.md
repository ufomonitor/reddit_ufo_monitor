# UFO Subreddit Monitor

This Python script monitors the activity on the r/UFOs subreddit, tracking active users and the number of upvotes on comments in the top rising and hot posts. It logs significant changes in comment upvotes and provides detailed information on comments with notable upvote differences.

## Features

- **Track Active Users**: Logs the number of active users on r/UFOs at each monitoring interval.
- **Upvote Monitoring**: Tracks upvotes on comments for the top 5 rising posts and the top 2 hot posts.
- **Significant Comment Changes**: Logs details of comments that experience significant upvote changes (difference greater than ±5).
- **Logging**:
  - **Main Log**: Records active users, total new upvotes, and significant comment details in `ufo_monitor.txt`.
  - **Verbose Log**: Provides a detailed log of all upvote changes in `ufo_monitor_adv.txt`.
  - **Console Output**: Prints key information to the console for real-time monitoring.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/ufo-subreddit-monitor.git
   cd ufo-subreddit-monitor

2. **Install Dependencies: Ensure you have Python 3.x installed. Install the required Python package:**
   ```bash
   pip install praw
4. ***Set Up Reddit API Credentials:***
   Go to Reddit Apps and create a new script application. Note down the client_id, client_secret, and user_agent. Update the script with your Reddit API credentials.

## Usage
1. **Run the Script:**
   ```bash
   python ufo_monitor.py

Output Files:

ufo_monitor.txt: Main log file with active users, new comment upvotes, and significant comment details.
ufo_monitor_adv.txt: Detailed verbose log with upvote changes for all tracked comments.
