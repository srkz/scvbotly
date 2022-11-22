import praw, yaml, time, traceback

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
    user_agent = config["user_agent"]
    mod_sub = config["mod_sub"]
    subs = config["filtered_subs"]

reddit = praw.Reddit(user_agent=user_agent)

streamComments = reddit.subreddit(mod_sub).stream.comments(pause_after=-1, skip_existing=True)

print('About to start while loop!')
while True:
    try:
        for comment in streamComments:
            if comment is None:
                break
            else:
                print('new comment coming in, setting is_filtered to false')
                is_filtered = False
                author = comment.author.name
                print('comment author name is u/' + author)
                
                userSubmissions = reddit.redditor(author).submissions.new(limit=None)
                print('checking user submissions against filtered subs' + subs)
                for acct_submission in userSubmissions:
                    print('submission in' + acct_submission.subreddit.display_name)
                    if acct_submission.subreddit.display_name in subs:
                        is_filtered = True
                        break
                    else:
                        break
                userComments = reddit.redditor(author).comments.new(limit=None)
                print('checking user comments against filtered subs')
                for acct_comment in userComments:
                    print('comment in' + acct_comment.subreddit.display_name)
                    if acct_comment.subreddit.display_name in subs:
                        is_filtered = True
                        break
                    else:
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