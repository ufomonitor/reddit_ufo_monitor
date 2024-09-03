import praw
import time
from datetime import datetime

# Reddit API credentials
client_id = ''
client_secret = ''
user_agent = 'doesn't really matter'

# Create a Reddit instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# Subreddit to monitor
subreddit_name = 'UFOs'
subreddit = reddit.subreddit(subreddit_name)

# Log file paths
log_file_path = r'c:\users\ufo_monitor.txt'
verbose_log_file_path = r'c:\users\ufo_monitor_adv.txt'

def get_comments_upvote_counts():
    upvote_counts = {}
    
    # Fetch the top 5 rising posts
    rising_posts = subreddit.rising(limit=5)
    
    # Fetch the top 2 hot posts
    hot_posts = subreddit.hot(limit=2)
    
    tracked_posts = list(rising_posts) + list(hot_posts)
    
    for submission in tracked_posts:
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            upvote_counts[comment.id] = {
                'score': comment.score,
                'body': comment.body[:100],  # limit to first 100 characters
                'author': comment.author.name if comment.author else "[deleted]",
                'permalink': f"https://reddit.com{comment.permalink}"
            }
    
    return upvote_counts, set(post.id for post in tracked_posts)

def log_upvote_differences(initial_upvotes, new_upvotes, tracked_post_ids):
    total_upvotes_difference = 0
    detailed_log = []
    
    for comment_id, initial_data in initial_upvotes.items():
        if comment_id in new_upvotes:
            initial_score = initial_data['score']
            new_data = new_upvotes[comment_id]
            new_score = new_data.get('score', 0)
            upvotes_difference = new_score - initial_score
            total_upvotes_difference += upvotes_difference
            
            # Log initial, new, and difference for each comment
            log_entry = f"Comment ID: {comment_id} | Initial: {initial_score}, New: {new_score}, Diff: {upvotes_difference}"
            detailed_log.append(log_entry)
            
            # If the difference is significant, log comment details
            if abs(upvotes_difference) > 5:
                comment_details = (
                    f"  Author: {initial_data['author']} | "
                    f"Comment: {initial_data['body']} | "
                    f"Link: {initial_data['permalink']}"
                )
                detailed_log.append(comment_details)
    
    return total_upvotes_difference, detailed_log

def monitor_upvote_changes():
    previous_tracked_post_ids = set()

    try:
        while True:
            # Get the current date and time
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Get the number of active users
            active_users = subreddit.active_user_count
            
            # Step 1: Get initial upvote counts and track post IDs
            initial_upvotes, tracked_post_ids = get_comments_upvote_counts()
            
            # Wait for 1 minute
            time.sleep(60)
            
            # Step 2: Get new upvote counts and track post IDs
            new_upvotes, _ = get_comments_upvote_counts()
            
            # Calculate the upvote differences and get detailed log
            total_upvotes_difference, detailed_log = log_upvote_differences(
                initial_upvotes, new_upvotes, tracked_post_ids
            )
            
            # Prepare the simple log entry
            log_entry = (
                f"{formatted_time} | Active users: {active_users} | "
                f"New comment upvotes: {total_upvotes_difference}\n"
            )
            
            # Write the main log entry to the main log file and print to console
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry)
                log_file.write("-------------------------------------\n")
            
            # Write the detailed log to the verbose log file
            with open(verbose_log_file_path, 'a', encoding='utf-8') as verbose_log_file:
                verbose_log_file.write(log_entry)
                verbose_log_file.write("\n".join(detailed_log) + "\n")
                verbose_log_file.write("-------------------------------------\n")
            
            # Print the main log entry and detailed log to console
            print(log_entry)
            print("\n".join(detailed_log))
            print("-------------------------------------")
            
            # Update the tracked post IDs for the next iteration
            previous_tracked_post_ids = tracked_post_ids
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    monitor_upvote_changes()
