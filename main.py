import praw, yaml, time, traceback

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
    client_id = config["client_id"]
    client_secret = config["client_secret"]
    username = config["username"]
    password = config["password"]
    user_agent = config["user_agent"]
    mod_sub = config["mod_sub"]
    subs = config["filtered_subs"]

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)

while True:
    try:
        for comment in reddit.subreddit(mod_sub).stream.comments(skip_existing=True):
            print('new comment!')
            is_filtered = False
            author = comment.author.name
            print('author:',author)
            for acct_submission in reddit.redditor(author).submissions.new(limit=None):
                if acc_submission.subreddit.display_name in subs:
                    is_filtered = True
                    print('filtered post in users history!')
                    break
            for acct_comment in reddit.redditor(author).comments.new(limit=None):
                if acct_comment.subreddit.display_name in subs:
                    is_filtered = True
                    print('filtered comment in users history!')
                    break
            print('is filtered?',is_filtered)
            if is_filtered == True:
                print('removed comment')
                comment.mod.remove()
            else:
                print('No filtered activity found.')
    except Exception:
        print(traceback.format_exc())
        time.sleep(60)
