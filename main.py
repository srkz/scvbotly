import praw, yaml, time, traceback

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
    user_agent = config["user_agent"]
    mod_sub = config["mod_sub"]
    subs = config["filtered_subs"]

reddit = praw.Reddit(user_agent=user_agent)

streamComments = reddit.subreddit(mod_sub).stream.comments(pause_after=-1, skip_existing=True)

print('Starting comment stream')
while True:
    try:
        for comment in streamComments:
            if comment is None:
                break
            else:
                is_filtered = False
                author = comment.author.name
                
                userSubmissions = reddit.redditor(author).submissions.new(limit=50)
                for acct_submission in userSubmissions:
                    if acct_submission.subreddit.display_name in subs:
                        is_filtered = True
                        break
                userComments = reddit.redditor(author).comments.new(limit=50)
                for acct_comment in userComments:
                    if acct_comment.subreddit.display_name in subs:
                        is_filtered = True
                        break
                if is_filtered == True:
                    print('New comment from u/' + author + ': Removed due to filtered account activity.')
                    comment.mod.remove()
                    break
                else:
                    print('New comment from u/' + author + ': Clean account.')
                    break
    except Exception:
        print(traceback.format_exc())
        time.sleep(60)