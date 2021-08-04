import os, requests, shutil
from instascrape import *

def get_test(hashtag):
    hash_obj = Hashtag(f"https://www.instagram.com/explore/tags/{hashtag}/")
    hash_obj.scrape()
    test_images = []
    total_post = hash_obj.amount_of_posts
    posts_list = hash_obj.get_recent_posts(total_post)
    for posts in posts_list:
        post = posts.to_dict()
        if not post['is_video']:
            test_images += [post['display_url']]
    os.system("mkdir -p test")
    for image_url, i in enumerate(test_images):
        res = requests.get(image_url, stream = True)
        if res.status_code == 200:
            res.raw.decode_content = True
            with open('test/test_image'+str(i)+'.jpg','wb') as f:
                shutil.copyfileobj(res.raw, f)


