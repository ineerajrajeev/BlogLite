from imports import *
# Table containing user data


class user_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    surname = db.Column(db.String(200), nullable=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    bio = db.Column(db.String(200), nullable=True)
    website = db.Column(db.String(200), nullable=True, unique=True)
    profile_pic = db.Column(db.Text, nullable=True)
    followers = db.Column(db.Integer, nullable=True)
    following = db.Column(db.Integer, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

    def __init__(self, name, surname, username, password, email, public_id, bio, website, profile_pic):
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password
        self.email = email
        self.bio = bio
        self.website = website
        self.profile_pic = profile_pic
        self.public_id = public_id
        self.followers = 0
        self.following = 0

    def serialize(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'username': self.username,
            'email': self.email,
            'public_id': self.public_id,
            'followers': self.followers,
            'following': self.following,
            'bio': self.bio,
            'website': self.website,
            'date_created': str(self.date_created)
        }

# Table containing followers and following users


class followers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower = db.Column(db.Integer, db.ForeignKey(
        'user_data.id'), nullable=False)
    following = db.Column(db.Integer, db.ForeignKey(
        'user_data.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id

    def __init__(self, follower, following):
        self.follower = follower
        self.following = following

    def serialize(self):
        return {
            'follower': self.follower,
            'following': self.following,
            'date_created': self.date_created
        }

# Table containing user posts


class blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    author = db.Column(db.Integer, db.ForeignKey(
        'user_data.id'), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    img = db.Column(db.Text, nullable=True)
    caption = db.Column(db.Text, nullable=True)
    state = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

    def __init__(self, blog_id, title, description, author, likes, img, caption, state):
        self.blog_id = blog_id
        self.title = title
        self.description = description
        self.author = author
        self.likes = likes
        self.img = img
        self.caption = caption
        self.state = state

    def serialize(self):
        return {
            'blog_id': self.blog_id,
            'title': self.title,
            'description': self.description,
            'date_created': str(self.date_created)[:16],
            'author': self.author,
            'likes': self.likes,
            'caption': self.caption,
            'state': self.state
        }


# Table containing user likes
class likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_liked = db.Column(db.DateTime, default=datetime.now)
    viewer = db.Column(db.Integer, db.ForeignKey(
        'user_data.id'), nullable=False)
    blog = db.Column(db.Integer, db.ForeignKey(
        'blogs.blog_id'), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

    def __init__(self, viewer, blog):
        self.viewer = viewer
        self.blog = blog

    def serialize(self):
        return {
            'date_liked': self.date_liked,
            'viewer': self.viewer,
            'blog': self.blog
        }

# Decorator for token verification


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if request.headers.get('x-access-token'):
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({'message': 'Token is missing!'}), 401)
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = user_data.query.filter_by(
                public_id=data['public_id']).first()
        except:
            return make_response(jsonify({'message': 'Token is invalid!'}), 401)
        return f(current_user, *args, **kwargs)
    return decorated

# Flask Restful API begins here

# Check if API is working with each template render
class apiCheck(Resource):

    # Check API
    def get(self):
        return make_response(jsonify({'status': 'Success'}), 200)

api.add_resource(apiCheck, '/apiCheck')

# Register new user
class Register(Resource):

    # Register a new user
    def post(self):
        data = request.json
        # match user by username or email
        user = user_data.query.filter_by(username=data['username']).first()
        try:
            if user:
                return make_response(jsonify({'message': 'User already exists', 'status': 'error'}), 409)
            else:
                hashed_password = generate_password_hash(
                    data['password'], method='sha256')
                new_user = user_data(name=data['name'], surname=data['surname'], username=data['username'], password=hashed_password, email=data['email'],
                                     public_id=str(uuid.uuid4()), bio=data['bio'], website=data['website'], profile_pic=None)
                db.session.add(new_user)
                db.session.commit()
                return make_response(jsonify({'message': 'Registered successfully!', 'status': 'success'}), 201)
        except:
            return make_response(jsonify({'message': 'Error!', 'status': 'error'}), 400)

api.add_resource(Register, '/api/register')

# Login and return JWT token
class Login(Resource):

    # Login a user and obtain JWT token
    def post(self):
        auth = request.json
        username = auth['username']
        password = auth['password']
        if not username or not password:
            return make_response(jsonify({'message': 'Please enter all fields!', 'status': 'error'}), 401)
        user = user_data.query.filter_by(username=username).first()
        if not user:
            return make_response(jsonify({'message': 'User does not exist!', 'status': 'error'}), 404)
        if check_password_hash(user.password, password):
            token = jwt.encode({'public_id': user.public_id, 'exp': datetime.utcnow(
            ) + timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
            return make_response(jsonify({'token': token, 'user_data': user.serialize(), 'status': 'success'}), 200)
        return make_response(jsonify({'message': 'Incorrect password!', 'status': 'error'}), 401)

api.add_resource(Login, '/api/login')

# Follow user
class follow(Resource):
    method_decorators = [token_required]

    # Follow user
    def post(self, current_user):
        data = request.json
        following = user_data.query.filter_by(
            username=data['username']).first()
        user_followers = followers.query.filter_by(
            follower=current_user.id, following=following.id).first()
        if following is None:
            return make_response(jsonify({'message': 'User not found!'}), 404)
        if following.id == current_user.id:
            return make_response(jsonify({'message': 'You cannot follow yourself!'}), 400)
        if user_followers is not None:
            return make_response(jsonify({'message': 'You are already following this user!'}), 400)
        new_follow = followers(current_user.id, following.id)
        following.followers += 1
        current_user.following += 1
        db.session.add(new_follow)
        db.session.commit()
        redis_client.delete(data['username'])
        redis_client.delete('analytics_'+data['username'])
        redis_client.delete('follow_'+data['username'])
        return make_response(jsonify({'message': 'Followed successfully!'}), 201)

api.add_resource(follow, '/api/follow')

# Unfollow user
class unfollow(Resource):
    method_decorators = [token_required]

    # Unfollow user
    def post(self, current_user):
        data = request.json
        following = user_data.query.filter_by(
            username=data['username']).first()
        user_followers = followers.query.filter_by(
            follower=current_user.id, following=following.id).first()
        if following is None:
            return make_response(jsonify({'message': 'User not found!'}), 404)
        if user_followers is None:
            return make_response(jsonify({'message': 'You are not following this user!'}), 400)
        db.session.delete(user_followers)
        following.followers -= 1
        current_user.following -= 1
        db.session.commit()
        redis_client.delete(data['username'])
        redis_client.delete('analytics_'+data['username'])
        redis_client.delete('follow_'+data['username'])
        return make_response(jsonify({'message': 'Unfollowed successfully!'}), 201)

api.add_resource(unfollow, '/api/unfollow')

# Get current user profile
class get_user(Resource):
    method_decorators = [token_required]

    # Get user data
    def get(self, current_user):
        user = user_data.query.filter_by(
            username=current_user.username).first()
        if user is None:
            return make_response(jsonify({'message': 'User not found!'}), 404)
        return make_response(jsonify({'user': user.serialize()}), 200)

api.add_resource(get_user, '/api/profile')

# Get user profile picture by username either from database or default image
class getProfile_pic(Resource):

    # Get user profile picture
    def get(self, username):
        user = user_data.query.filter_by(
            username=username).first()
        if user is None:
            return make_response(jsonify({'message': 'User not found!', 'status': 'error'}), 404)
        if user.profile_pic is None:
            return send_file('static/default.jpg', mimetype='image/jpeg')
        return Response(user.profile_pic, mimetype="image/jpeg")

api.add_resource(getProfile_pic, '/api/profile_pic/<string:username>')

# Search for user
class search_user(Resource):
    method_decorators = [token_required]

    # Search for user by username like string
    def post(self, current_user):
        data = request.json
        user = user_data.query.filter(
            user_data.username.like('%' + data['username'] + '%')).all()
        if user is None:
            return make_response(jsonify({'message': 'User not found!'}), 404)
        users = [u.serialize() for u in user]
        return make_response(jsonify({'user': users}), 200)

api.add_resource(search_user, '/api/search')

# Edit user data from settings
class update_user(Resource):
    method_decorators = [token_required]

    # Update user data
    def post(self, current_user):
        data = request.form.to_dict()
        user = user_data.query.filter_by(
            username=current_user.username).first()
        if user is None:
            return make_response(jsonify({'message': 'User not found!'}), 404)
        try:
            file = request.files['img']
            if file is not None and file.filename != '':
                user.profile_pic = file.read()
        except:
            pass
        user.bio = None if data['bio'] == "null" else data['bio']
        user.email = data['email']
        user.website = None if data['website'] == "null" else data['website']
        db.session.commit()
        redis_client.delete(current_user.username)
        return make_response(jsonify({'message': data['bio']}), 200)

api.add_resource(update_user, '/api/update_user')

# Get image for blog either from database or unsplash API
class get_blog_image(Resource):

    # Get blog image
    def get(self, blog_id):
        blog = blogs.query.filter_by(blog_id=blog_id).first()
        if blog is None:
            return make_response(jsonify({'message': 'Blog not found!'}), 404)
        if blog.img is None:
            unsplash_api_key = "p2s_7irxZGk0HZKPVv7tuUpQl_rCFxaHdxEcWrlqFiA"
            params = {'query': blog.title, 'client_id': unsplash_api_key}
            response = requests.get(
                'https://api.unsplash.com/search/photos', params=params)
            data = response.json()
            if len(data['results']) == 0:
                img_url = "https://images.unsplash.com/photo-1568667256549-094345857637?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzOTQ0ODV8MHwxfHNlYXJjaHw0fHxsaWJyYXJ5fGVufDB8fHx8MTY3Mjg1NDgzMw&ixlib=rb-4.0.3&q=80&w=1080"
            else: 
                random_no = random.randint(0, len(data['results'])-1)
                img_url = data['results'][random_no]['urls']['regular']
            local_filename, headers = urllib.request.urlretrieve(img_url)
            img = open(local_filename, 'rb').read()
            return Response(img, mimetype="image/jpeg")
        return Response(blog.img, mimetype="image/jpeg")

api.add_resource(get_blog_image, '/api/blog_image/<blog_id>')

# Update user password
class update_password(Resource):
    method_decorators = [token_required]

    # Update user password
    def post(self, current_user):
        data = request.args
        user = user_data.query.filter_by(
            username=current_user.username).first()
        if user is None:
            return make_response(jsonify({'message': 'User not found!'}), 404)
        if not check_password_hash(user.password, data['old_password']):
            return make_response(jsonify({'message': 'Wrong password!'}), 400)
        user.password = generate_password_hash(
            data['new_password'], method='sha256')
        db.session.commit()
        return make_response(jsonify({'message': 'Password updated successfully!'}), 200)

api.add_resource(update_password, '/update_password')

# API for creating new blog
class newBlog(Resource):
    method_decorators = [token_required]

    def post(self, current_user):
        data = request.form.to_dict()
        try:
            file = request.files['img']
            if file is not None and file.filename != '':
                img = file.read()                
        except:
            img = None
        blog_id = ''.join(random.choices(
            string.ascii_letters + string.digits, k=16))
        new_blog = blogs(
            blog_id=blog_id,
            title=data['title'],
            description=data['description'],
            author=current_user.id,
            likes=0,
            img=img,
            caption=data['caption'] if data['caption'] is not None else data['title'],
            state= True if data['state'] == 'true' else False,
        )
        db.session.add(new_blog)
        db.session.commit()
        redis_client.delete(current_user.username)
        redis_client.delete('analytics_'+current_user.username)
        return make_response(jsonify({'message': 'Blog created successfully!', 'status': 'success'}), 200)

api.add_resource(newBlog, '/api/new_blog')

# With every request, check if token is valid
class verify_token(Resource):

    method_decorators = [token_required]

    def get(self, current_user):
        return make_response(jsonify({'message': 'Token verified successfully!', 'status': 'success'}), 200)

api.add_resource(verify_token, '/api/verify_token')

# Fetch blogs for feed
class fetch_posts(Resource):
    method_decorators = [token_required]

    def get(self, current_user):
        followed_users = followers.query.filter_by(
            follower=current_user.id).all()
        blogs_list = []
        for blog in blogs.query.all():
            if blog.author == current_user.id or blog.author in [f.following for f in followed_users]:
                if blog.state:
                    author = user_data.query.filter_by(id=blog.author).first()
                    author_details = {
                        'username': author.username,
                        'name': author.name,
                        'surname': author.surname,
                    }
                    liked = likes.query.filter_by(viewer=current_user.id, blog=blog.blog_id).first()
                    blogs_list.append({'blog': blog.serialize(), 'author': author_details, 'liked': True if liked else False})
        blogs_list.sort(key=lambda x: x['blog']['date_created'], reverse=True)
        return make_response(jsonify({'message': blogs_list, 'status': 'success'}), 200)

api.add_resource(fetch_posts, '/api/fetch_posts')

# Fetch blogs for profile
class fetch_profile_posts(Resource):
    method_decorators = [token_required]

    def get(self, current_user):
        blogs_list = []
        for blog in blogs.query.filter_by(author=current_user.id).all():
            author_details = {
                'username': current_user.username,
                'name': current_user.name,
                'surname': current_user.surname,
            }
            blogs_list.append(
                {'blog': blog.serialize(), 'author': author_details})
        return make_response(jsonify({'message': blogs_list, 'status': 'success'}), 200)

api.add_resource(fetch_profile_posts, '/api/fetch_profile_posts')

# Fetch blogs for profile
class get_user_profile(Resource):
    method_decorators = [token_required]

    def get(self, current_user, username):
        res = redis_client.get(username)
        if not res:
            user = user_data.query.filter_by(username=username).first()
            if user is None:
                return make_response(jsonify({'message': 'User not found!', 'status': 'error'}), 404)
            blogs_list = blogs.query.filter_by(author=user.id).all()
            user_profile = {'user': user.serialize(), 'blogs': [
                blog.serialize() for blog in blogs_list]}
            redis_client.set(username, json.dumps(user_profile))
            redis_client.expire(username, timedelta(minutes=30))
        else:
            user_profile = json.loads(res)
        return make_response(jsonify({'message': user_profile, 'status': 'success'}), 200)

api.add_resource(get_user_profile, '/api/get_user/<username>')

# Delete blog
class delete_blog(Resource):
    method_decorators = [token_required]

    def post(self, current_user):
        data = request.json
        blog = blogs.query.filter_by(blog_id=data['blog_id']).first()
        if blog is None:
            return make_response(jsonify({'message': 'Blog not found!'}), 404)
        if blog.author != current_user.id:
            return make_response(jsonify({'message': 'You are not authorized to delete this blog!'}), 401)
        blog_likes = likes.query.filter_by(blog = data['blog_id']).all()
        for like in blog_likes:
            db.session.delete(like)
        db.session.delete(blog)
        db.session.commit()
        redis_client.delete(current_user.username)
        return make_response(jsonify({'message': 'Blog deleted', 'status': 'success'}), 200)

api.add_resource(delete_blog, '/api/delete')

# Hide blog
class hideBlog(Resource):
    method_decorators = [token_required]

    def post(self, current_user):
        data = request.json
        blog = blogs.query.filter_by(blog_id=data['blog_id']).first()
        message = 'Blog hidden' if blog.state else 'Blog unhidden'
        if blog is None:
            return make_response(jsonify({'message': 'Blog not found!'}), 404)
        if blog.author != current_user.id:
            return make_response(jsonify({'message': 'You are not authorized to hide this blog!'}), 401)
        blog.state = not blog.state
        db.session.commit()
        redis_client.delete(current_user.username)
        return make_response(jsonify({'message': message, 'status': 'success'}), 200)

api.add_resource(hideBlog, '/api/hide')

# Get followers for current user
class get_follow_data(Resource):
    method_decorators = [token_required]

    def get(self, current_user):
        res = redis_client.get('follow_'+current_user.username)
        if res is None:
            user = user_data.query.filter_by(username=current_user.username).first()
            if user is None:
                return make_response(jsonify({'message': 'User not found!','status': 'error'}), 404)
            follower_list = followers.query.filter_by(following=user.id).join(user_data, followers.follower == user_data.id).add_columns(user_data.username, user_data.name, user_data.surname).all()
            following_list = followers.query.filter_by(follower=user.id).join(user_data, followers.following == user_data.id).add_columns(user_data.username, user_data.name, user_data.surname).all()
            output = {'following': [{'username': i.username, 'name': i.name, 'surname': i.surname} for i in following_list],
                    'followers': [{'username': i.username, 'name': i.name, 'surname': i.surname} for i in follower_list],
                    'user': {'username': user.username, 'name': user.name, 'surname': user.surname},
                    'status': 'success'}
            redis_client.set('follow_'+current_user.username, json.dumps(output))
            redis_client.expire('follow_'+current_user.username, timedelta(minutes=30))
        else:
            output = json.loads(res)
        return make_response(jsonify(output), 200)

api.add_resource(get_follow_data, '/api/get_follow_data')

class fetch_blog(Resource):
    method_decorators = [token_required]

    def get(self, current_user, blog_id):
        blog = blogs.query.filter_by(blog_id=blog_id).first()
        if blog is None:
            return make_response(jsonify({'message': 'Blog not found!'}), 404)
        author = user_data.query.filter_by(id=blog.author).first()
        author_details = {
            'username': author.username,
            'name': author.name,
            'surname': author.surname,
        }
        blog_details = {'blog': blog.serialize(), 'author': author_details}
        return make_response(jsonify({'message': blog_details, 'status': 'success'}), 200)

api.add_resource(fetch_blog, '/api/fetch_blog/<blog_id>')

# Edit blog
class edit_blog(Resource):
    method_decorators = [token_required]

    def post(self, current_user):
        data = request.json
        blog = blogs.query.filter_by(blog_id=data['blog_id']).first()
        if blog is None:
            return make_response(jsonify({'message': 'Blog not found!'}), 404)
        if blog.author!= current_user.id:
            return make_response(jsonify({'message': 'You are not authorized to edit this blog!'}), 401)
        blog.title = data['title']
        blog.caption = data['caption']
        blog.description = data['description']
        db.session.commit()
        redis_client.delete(current_user.username)
        return make_response(jsonify({'message': "Blog updated", 'status': 'success'}), 200)

api.add_resource(edit_blog, '/api/edit_blog')

# Export all blogs to CSV format
class export_csv(Resource):

    def get(self):
        user = user_data.query.filter_by(username='shetkarrohan').first()
        if user is None:
            return make_response(jsonify({'message': 'User not found!','status': 'error'}), 404)
        csv_data = io.StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerow(['Blog ID', 'Title', 'Caption', 'Description', 'Author', 'Date', 'image_link'])
        blogs_list = blogs.query.filter_by(author=user.id).all()
        for blog in blogs_list:
            image_link = 'http://127.0.0.1:5000/api/blog_image/' + blog.blog_id
            csv_writer.writerow([blog.blog_id, blog.title, blog.caption, blog.description, " ".join([user.name, user.surname]), blog.date_created, image_link])
        csv_data.seek(0)
        filename = 'blogs_' + user.username + '_' + str(datetime.now()) + '.csv'
        return Response(csv_data, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename={}'.format(filename)})

api.add_resource(export_csv, '/export_csv')

# Like / Dislike blog
class like(Resource):
    method_decorators = [token_required]

    def post(self, current_user):
        data = request.json
        blog = blogs.query.filter_by(blog_id=data['blog_id']).first()
        if blog is None:
            return make_response(jsonify({'message': 'Blog not found!', 'status': 'error'}), 404)
        like_data = likes.query.filter_by(blog=data['blog_id'], viewer=current_user.id).first()
        user = user_data.query.filter_by(id=blog.author).first()
        redis_client.delete('analytics_'+user.username)
        if like_data is None:
            new_like = likes(blog=data['blog_id'], viewer=current_user.id)
            blog.likes += 1
            db.session.add(new_like)
            db.session.commit()
            return make_response(jsonify({'message': 'Liked', 'status': 'success'}), 200)
        else:
            blog.likes -= 1
            db.session.delete(like_data)
            db.session.commit()
            return make_response(jsonify({'message': 'Unliked', 'status': 'success'}), 200)

api.add_resource(like, '/api/like')

# Analytics
class analytics(Resource):
    method_decorators = [token_required]

    def get(self, current_user):
        res = redis_client.get('analytics_'+current_user.username)
        if res is None:
            user = user_data.query.filter_by(username=current_user.username).first()
            if user is None:
                return make_response(jsonify({'message': 'User not found!','status': 'error'}), 404)
            blogs_list = blogs.query.filter_by(author=user.id).all()
            blog_titles = [blog.title for blog in blogs_list]
            blog_likes = [blog.likes for blog in blogs_list]
            likes_data = {'titles':blog_titles, 'likes':blog_likes}
            # Count of posts made in each month
            month_posts_list = []
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            year_month = []
            month = datetime.now().month
            for i in range(month+1, month + 13):
                if i < 12:
                    month = i
                    year = int(datetime.now().year) - 1
                    year_month.append("{} {}".format(months[month - 1], year))
                    month_posts_list.append(blogs.query.filter_by(author=user.id).filter(extract('month', blogs.date_created) == month, extract('year', blogs.date_created) == year).count())
                else:
                    month = i % 12
                    year = datetime.now().year
                    year_month.append("{} {}".format(months[month - 1], year))
                    month_posts_list.append(blogs.query.filter_by(author=user.id).filter(extract('month', blogs.date_created) == month, extract('year', blogs.date_created) == year).count())
                output = {'likes_data': likes_data,
                      'posts_over_last_month': month_posts_list, 'months': year_month, 'status': 'success'}
            redis_client.set('analytics_'+current_user.username, json.dumps(output))
            redis_client.expire('analytics_'+current_user.username, timedelta(minutes=30))
        else:
            output = json.loads(res)
        return make_response(jsonify(output), 200)

api.add_resource(analytics, '/api/analytics')


@app.route('/api/export_html/<blog_id>')
def export_html(blog_id):
    blog = blogs.query.filter_by(blog_id=blog_id).first()
    if blog is None:
        return make_response(jsonify({'message': 'Blog not found!', 'status': 'error'}), 404)
    user = user_data.query.filter_by(id=blog.author).first()
    export = render_template('blog_export.html', blog=blog, user=user)
    filename = 'blog_' + blog_id + '_' + str(datetime.now()) + '.html'
    return Response(export, mimetype='text/html', headers={'Content-Disposition': 'attachment; filename={}'.format(filename)})

@celery.task
def reminder(bind=True):
    users = user_data.query.all()
    for user in users:
        like_data = likes.query.filter_by(viewer=user.id).filter(extract('day', likes.date_liked) == datetime.now().day).all()
        if len(like_data) == 0:
            no_likes_template =  render_template('no_likes.html', name=user.name)
            send_email(user.email, "You're missing your latest blogs !!!", no_likes_template)
        blog_data = blogs.query.filter_by(author=user.id).filter(extract('day', blogs.date_created) == datetime.utcnow().day).all()
        if len(blog_data) == 0:
            no_blog_template =  render_template('no_posts.html', name=user.name)
            send_email(user.email, "What's on your mind {}?".format(user.name), no_blog_template)
    return None


@celery.task(bind=True)
def monthly_report():
    users = user_data.query.all()
    for user in users:
        if user is None:
            return make_response(jsonify({'message': 'User not found!','status': 'error'}), 404)
        blogs_list = blogs.query.filter_by(author=user.id).filter(extract('month', blogs.date_created) == datetime.now().month).all()
        blog_titles = [blog.title for blog in blogs_list]
        blog_likes = [blog.likes for blog in blogs_list]
        likes_data = {'titles':blog_titles, 'likes':blog_likes}
        # Count of posts made in each month
        month_posts_list = []
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_limit = datetime.utcnow().month
        for month in range(1, month_limit+1):
            month_posts_list.append(blogs.query.filter_by(author=user.id).filter(extract('month', blogs.date_created) == month, extract('year', blogs.date_created) == datetime.now().year).count())
        output = {'likes_data': likes_data,
                'posts_over_last_month': month_posts_list, 'months': months[:month_limit],'status': 'success'}
        monthly_report_template =  render_template('monthly_report.html', data=output)
        send_email(user.email, "Monthly Report", monthly_report_template)
    return None

@app.route('/api/pdf_report')
@token_required
def pdf_report(current_user):
    user = user_data.query.filter_by(username=current_user.username).first()
    if user is None:
        return make_response(jsonify({'message': 'User not found!','status': 'error'}), 404)
    blogs_list = blogs.query.filter_by(author=user.id).filter(extract('month', blogs.date_created) == datetime.now().month).all()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year_log = {}
    month = datetime.now().month
    for i in range(month+1, month + 13):
        if i < 12:
            month = i
            year = int(datetime.now().year) - 1
            year_log["{} {}".format(months[month - 1], year)] = (blogs.query.filter_by(author=user.id).filter(extract('month', blogs.date_created) == month, extract('year', blogs.date_created) == year).count())
        else:
            month = i % 12
            year = datetime.now().year
            year_log["{} {}".format(months[month - 1], year)] = (blogs.query.filter_by(author=user.id).filter(
                extract('month', blogs.date_created) == month, extract('year', blogs.date_created) == year).count())
        output = {'months': year_log, 'status': 'success',
                'blogs':[i.serialize() for i in blogs_list], 'user':user.serialize(), 'date':datetime.now().strftime('%d %b %Y')}
    # weasyprint
    render = render_template('pdf_report.html', data=output)
    pdf = weasyprint.HTML(string=render).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=report.pdf'
    return response


@app.route('/api/html_report')
@token_required
def html_report(current_user):
    user = current_user
    blogs_list = blogs.query.filter_by(author=user.id).filter(extract('month', blogs.date_created) == datetime.now().month).all()
    blog_titles = [blog.title for blog in blogs_list]
    blog_likes = [blog.likes for blog in blogs_list]
    likes_data = {'titles':blog_titles, 'likes':blog_likes}
    month_posts_list = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_limit = datetime.utcnow().month
    for month in range(1, month_limit+1):
        month_posts_list.append(blogs.query.filter_by(author=user.id).filter(extract('month', blogs.date_created) == month, extract('year', blogs.date_created) == datetime.utcnow().year).count())
    output = {'likes_data': likes_data,
            'posts_over_last_month': month_posts_list, 'months': months[:month_limit],'status': 'success'}
    monthly_report_template =  render_template('monthly_report.html', data=output)
    response = make_response(monthly_report_template)
    response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Disposition'] = 'attachment; filename=report.html'
    return response

db.create_all()
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
