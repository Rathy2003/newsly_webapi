import datetime
import os
import uuid
from pathlib import Path
from flask import render_template, send_from_directory, url_for, Blueprint
from flask_restx import Api, Resource, fields,reqparse
import bcrypt
from werkzeug.exceptions import BadRequest
from sqlalchemy import func
from werkzeug.datastructures import FileStorage
from extentions.extensions import db, app
from fcm_v1 import send_fcm_v1
from models.models import Category, News, User
from flask_jwt_extended import JWTManager,create_access_token, get_jwt_identity, verify_jwt_in_request
from utils.response import success_response

UPLOAD_FOLDER = Path("uploads" if os.getenv("PRODUCTION") != "True" else "/uploads")
ROOT_DIR = Path(__file__).resolve().parent
app.config['RESTX_MASK_SWAGGER'] = False
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "7c9c6fd4e253ddd194481ee016a4a9b3"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=7)

jwt = JWTManager(app)

with app.app_context():
    db.create_all()
    # create directory if not exist
    UPLOAD_FOLDER.mkdir(exist_ok=True)
api_bp = Blueprint('api_v1', __name__,url_prefix="/api/v1")

api = Api(
    api_bp,
    version='1.0',
    title='Newsly API Documentation',
    doc=False,
)
@app.route('/docs')
def docs():
    return render_template(
        'index.html',
        specs_url="/api/v1/swagger.json"
    )    

app.register_blueprint(api_bp)

category_ns = api.namespace('category')
news_ns = api.namespace('news')
user_ns = api.namespace('user')

# Start Category
category_api_model = api.model('Category', {
    'id': fields.Integer(readOnly=True, description='Category ID'),
    'name': fields.String(required=True, description='Category name'),
    'createdAt': fields.DateTime(readOnly=True, description='Category createdAt'),
    'updatedAt': fields.DateTime(readOnly=True, description='Category updatedAt'),
})

update_category_api_model = api.model('Category', {
    'message': fields.String(readOnly=True, description='Category updated successfully'),
    'data': fields.Nested(category_api_model)
})

create_category_parser = api.parser()
create_category_parser.add_argument('name', type=str, help='Category name')

update_category_parser = api.parser()
update_category_parser.add_argument('name', type=str, help='Category name', required=True,location='form')

@app.route("/files/<path:filename>")
def serve_file(filename):
    return send_from_directory(directory= Path("../uploads" if os.getenv("PRODUCTION") != 'True' else '/uploads') / 'news',path=filename)

@app.route("/files/profiles/<path:filename>")
def serve_profile(filename):
    return send_from_directory(directory= Path("../uploads" if os.getenv("PRODUCTION") != 'True' else '/uploads') / 'users',path=filename)

@category_ns.route('/')
class CategoryList(Resource):
    @category_ns.doc('category_list')
    @category_ns.marshal_list_with(category_api_model)
    def get(self):
        '''List all categories'''
        categories = Category.query.all()
        return categories
    @category_ns.doc('category_create')
    @category_ns.expect(create_category_parser)
    # @category_ns.marshal_with(category_api_model,code=201)
    def post(self):
        """Create a new category"""
        args = create_category_parser.parse_args()
        name = args.get('name')
        is_exist = Category.query.filter(func.lower(Category.name) == func.lower(name)).first()
        if is_exist:
            raise BadRequest("This name already exists. Please choose another name.")
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()

        from fcm_v1 import send_fcm_v1
        tokens = [u.fcm_token for u in User.query.filter(User.fcm_token.isnot(None)).all()]
        for token in tokens:
            send_fcm_v1(token, "📰 New Article!", f"{category.name}")
        return {"message": "Category has been created.", "id": category.id}, 201

@category_ns.route('/<int:category_id>')
@category_ns.param('category_id', 'Category ID')
class CategoryOptions(Resource):
    @category_ns.doc('update_category',
                     consumes=['application/x-www-form-urlencoded'],
                    )
    @category_ns.expect(update_category_parser)
    @category_ns.marshal_with(update_category_api_model)
    def put(self,category_id):
        """Update a category"""
        args = update_category_parser.parse_args()
        name = args.get('name')
        category = Category.query.get(category_id)
        category.name = name
        db.session.commit()
        return {"message": "Category has been updated.", "data": category}, 200
    @category_ns.doc('delete_category')
    def delete(self,category_id):
        """Delete a category"""
        category = Category.query.get(category_id)
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category has been deleted."}, 200
# End Category

# Start News
news_api_model = api.model('News', {
    'id': fields.Integer(readOnly=True, description='News ID'),
    'title': fields.String(required=True, description='News title'),
    'description': fields.String(required=True, description='Description'),
    'content': fields.String(required=True, description='News content'),
    'category_id': fields.Integer(required=True,description='Category ID'),
    'full_image_path': fields.String(required=True, description='Full image path'),
    'category_name': fields.String(required=True, description='Category name'),
    'posted_at': fields.String(readOnly=True, description='News PostedAt'),
})
news_api_model['content'].__schema__['x-richtext'] = True

def get_new_parser():
    news_parser = reqparse.RequestParser()
    with app.app_context():
        categories = [c.name for c in Category.query.all()]
    news_parser.add_argument('title', type=str, help='Title', required=True, location='form')
    news_parser.add_argument('description', type=str, help='Description', required=True, location='form')
    news_parser.add_argument('category', type=str, choices=categories, help='Category', required=True, location='form')
    news_parser.add_argument('thumbnail', type=FileStorage, help='Thumbnail', required=True, location='files')
    news_parser.add_argument('content',type=str, help='Content', required=True,location="form")
    return news_parser

@news_ns.route('/')
class NewsList(Resource):
    news_parser = get_new_parser()
    @news_ns.doc('news_list')
    @news_ns.marshal_list_with(news_api_model)
    def get(self):
        """List all news"""
        news = News.query.all()
        news_list = []
        for x in news:
            news_item = {
                'id': x.id,
                'title': x.title,
                'description': x.description,
                'content': x.content,
                'category_id': x.category_id,
                'category_name': x.category.name,
                'full_image_path': url_for("serve_file", filename=x.thumbnail, _external=True),
                'posted_at': x.createdAt,
            }
            news_list.append(news_item)
        return news_list
    
    @news_ns.doc('news_create',consumes=['application/x-www-form-urlencoded'],)
    @news_ns.expect(news_parser)
    def post(self):
        args = self.news_parser.parse_args()
        title = args.get('title')
        description = args.get('description')
        category = args.get('category')
        content = args.get('content')
        thumbnail = args.get('thumbnail')

        file_ext = thumbnail.filename.split('.')[-1]
        safe_filename = f"{uuid.uuid4().hex}.{file_ext}"
        file_path = UPLOAD_FOLDER / 'news' /safe_filename
        category_id = Category.query.filter(func.lower(Category.name) == func.lower(category)).first().id
        news = News(
            title=title,
            description=description,
            content=content,
            category_id=category_id,
            thumbnail=safe_filename,
        )
        db.session.add(news)
        db.session.commit()
        thumbnail.save(file_path)

        users_list = User.query.all()
        for user in users_list:
            token = user.fcm_token
            if token:
                send_fcm_v1(
                    token=token,
                    title="ព័តិ៍មានថ្មីៗ",
                    body=f"{title}"
                )

        data = news.to_dict()
        return success_response(data,"News has been created successfully.",status_code=201)


def get_update_news_parser():
    news_parser = reqparse.RequestParser()
    with app.app_context():
        categories = [c.name for c in Category.query.all()]
    news_parser.add_argument('title', type=str, help='Title', required=False, location='form')
    news_parser.add_argument('description', type=str, help='Description', required=False, location='form')
    news_parser.add_argument('category', type=str, choices=categories, help='Category', required=False, location='form')
    news_parser.add_argument('thumbnail', type=FileStorage, help='Thumbnail', required=False, location='files')
    news_parser.add_argument('content',type=str, help='Content', required=False,location="form")
    return news_parser

@news_ns.route('/<int:id>')
@news_ns.param('id', 'The news ID')
class NewsUpdateAndDelete(Resource):
    news_parser = get_update_news_parser()
    @news_ns.doc('Update News', consumes=['application/x-www-form-urlencoded'])


    @news_ns.expect(news_parser)
    def put(self,id):
        args = self.news_parser.parse_args()
        title = args.get('title')
        description = args.get('description')
        category = args.get('category')
        content = args.get('content')
        thumbnail = args.get('thumbnail')

        news = News.query.get(id)
        if not news:
            return {"message": f"News with ID = {id} not found."}, 404

        if title:
            news.title = title
        if description:
            news.description = description
        if content:
            news.content = content
        if category:
            category_id = Category.query.filter(func.lower(Category.name) == func.lower(category)).first().id
            news.category_id = category_id

        if thumbnail:
            file_ext = thumbnail.filename.split('.')[-1]
            safe_filename = f"{uuid.uuid4().hex}.{file_ext}"
            file_path = UPLOAD_FOLDER / 'news' / safe_filename

            old_filepath = os.path.join(UPLOAD_FOLDER, 'news', news.thumbnail)
            if os.path.isfile(old_filepath):
                os.remove(old_filepath)
            thumbnail.save(file_path)
            news.thumbnail = safe_filename
        db.session.commit()
        data = news.to_dict()
        return success_response(data,"News has been updated successfully.",status_code=200)

    def delete(self,id):
        news = News.query.get(id)
        if not news:
            return {"message": "News not found."}, 404
        news_thumbnail_path = os.path.join(UPLOAD_FOLDER,"news",news.thumbnail)
        if os.path.isfile(news_thumbnail_path):
            os.remove(news_thumbnail_path)
        db.session.delete(news)
        db.session.commit()
        return {"message": "News has been deleted.","id":id}, 200

@news_ns.route('/breaking')
class BreakingNews(Resource):
    @news_ns.doc('breaking news')
    @news_ns.marshal_list_with(news_api_model)
    def get(self):
        """List Breaking News"""
        news = News.query.order_by(News.createdAt.desc()).limit(6)
        news_list = []
        for x in news:
            news_item = {
                'id': x.id,
                'title': x.title,
                'description': x.description,
                'content': x.content,
                'category_id': x.category_id,
                'category_name': x.category.name,
                'full_image_path': url_for("serve_file", filename=x.thumbnail, _external=True),
                'posted_at': x.createdAt,
            }
            news_list.append(news_item)
        return news_list

@news_ns.route('/category/<int:category_id>')
class NewsFilterByCategory(Resource):
    @news_ns.doc('news_list_by_category')
    @news_ns.marshal_list_with(news_api_model)
    def get(self,category_id):
        """List News By Category Id"""
        news = News.query.filter_by(category_id=category_id).all()
        news_list = []
        for x in news:
            # news_item = {
            #     'id': x.id,
            #     'title': x.title,
            #     'description': x.description,
            #     'content': x.content,
            #     'category_id': x.category_id,
            #     'category_name': x.category.name,
            #     'full_image_path': url_for("serve_file", filename=x.thumbnail, _external=True),
            #     'posted_at': x.createdAt,
            # }
            news_list.append(x.to_dict())
        return news_list

@news_ns.route('/search/<string:query>')
class SearchNews(Resource):
    @news_ns.doc('search_news')
    @news_ns.marshal_list_with(news_api_model)
    def get(self,query):
        news = News.query.filter(News.title.ilike(f"%{query}%")).all()
        news_list = []
        for x in news:
            news_list.append(x.to_dict())
        return news_list , 200

# End News

# Start User
user_api_model = api.model("User", {
    'id': fields.Integer(readOnly=True, description='User ID'),
    'username': fields.String(required=True, description='Useranme'),
    'email': fields.String(required=True, description='Email'),
    'full_image_path': fields.String(required=False, description='Profile'),
    'createdAt': fields.String(description='User createdAt'),
    'updatedAt': fields.String(description='User updatedAt'),
})

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username', type=str, help='Useranme', required=True, location='form')
create_user_parser.add_argument('email', type=str, help='Email', required=True, location='form')
create_user_parser.add_argument('profile', type=FileStorage, help='Profile', required=False, location='files')
create_user_parser.add_argument('password', type=str, help='Password', required=True, location='form')


@user_ns.route('')
class UserList(Resource):
    @user_ns.doc('get_all_users')
    @user_ns.marshal_with(user_api_model,code=200)
    def get(self):
        users = User.query.all()
        user_list = [ user.to_dict() for user in users]
        return user_list

    @user_ns.doc('create_user',consumes=['application/multipart/form-data'])
    @user_ns.expect(create_user_parser)
    def post(self):
        args = create_user_parser.parse_args()
        username = args.get('username')
        email = args.get('email')
        profile = args.get('profile')

        password = args.get('password')
        hash_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        safe_filename = None
        if profile:
            file_ext = profile.filename.split('.')[-1]
            safe_filename = f"{uuid.uuid4().hex}.{file_ext}"
            os.makedirs(UPLOAD_FOLDER / 'users', exist_ok=True)
            file_path = UPLOAD_FOLDER / 'users' / safe_filename
            profile.save(file_path)

        # check email or username exist
        user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
        if user:
            raise BadRequest("ឈ្មោះនេះមានរួចហើយ សូមជ្រើសរើសឈ្មោះផ្សេងៗ")
        user = User.query.filter(func.lower(User.email) == func.lower(email)).first()
        if user:
            raise BadRequest("អ៊ីមែលនេះមានរួចហើយ សូមជ្រើសរើសអ៊ីមែលផ្សេងៗ")

        user = User(username=username,email=email,profile=safe_filename,password=hash_password.decode('utf-8'))
        db.session.add(user)
        db.session.commit()

        data = user.to_dict()
        return success_response(message="អ្នកប្រើប្រាស់ត្រូវបានបង្កើតដោយជោគជ័យ",data=data,status_code=201) , 201
    
update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('username', type=str, help='Useranme', required=False, location='form')
update_user_parser.add_argument('profile', type=FileStorage, help='Profile', required=False, location='files')
update_user_parser.add_argument('email', type=str, help='Email', required=False, location='form')

@user_ns.route('/<int:id>')
@user_ns.param('id','User ID')
class UserDeleteAndUpdate(Resource):
    @user_ns.doc('update_user',consumes=['multipart/form-data'])
    @user_ns.expect(update_user_parser)
    def put(self,id):
        args = update_user_parser.parse_args()
        username = args.get('username')
        email = args.get('email')
        profile = args.get('profile')
        user = User.query.get(id)
        if not user:
            raise BadRequest("រកមិនឃើញអ្នកប្រើប្រាស់ដែលមាន id = " + str(id) + " នោះទេ.")
        
        # check name exist except current user
        exist_user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
        if exist_user and exist_user.id != id:
            raise BadRequest("ឈ្មោះនេះមានរួចហើយ សូមជ្រើសរើសឈ្មោះផ្សេងៗ")
        exist_user = User.query.filter(func.lower(User.email) == func.lower(email)).first()
        if exist_user and exist_user.id != id:
            raise BadRequest("អ៊ីមែលនេះមានរួចហើយ សូមជ្រើសរើសអ៊ីមែលផ្សេងៗ")

        safe_filename = None
        if profile:
            file_ext = profile.filename.split('.')[-1]
            safe_filename = f"{uuid.uuid4().hex}.{file_ext}"
            os.makedirs(UPLOAD_FOLDER / 'users', exist_ok=True)
            file_path = UPLOAD_FOLDER / 'users' / safe_filename
            profile.save(file_path)

            # delete old profile
            if user.profile:
                old_profile_path = os.path.join(UPLOAD_FOLDER / 'users' / user.profile)
                if os.path.isfile(old_profile_path):
                    os.remove(old_profile_path)
            user.profile = safe_filename

        if username:
            user.username = username
        if email:
            user.email = email
        db.session.commit()

        data = user.to_dict()
        return success_response(message="អ្នកប្រើប្រាស់ត្រូវបានកែប្រែដោយជោគជ័យ",data=data,status_code=200) , 200

    def delete(self,id):
        user = User.query.get(id)
        if not user:
            return {"message" : f"រកមិនឃើញអ្នកប្រើប្រាស់ដែលមាន ID = {id} នោះទេ។"} , 404

        old_profile_path = os.path.join(UPLOAD_FOLDER, 'users', user.profile)
        if os.path.isfile(old_profile_path):
            os.remove(old_profile_path)
        db.session.delete(user)
        db.session.commit()

        return {"message": "អ្នកប្រើប្រាស់ត្រូវបានលុបដោយជោគជ័យ"} , 200
logout_user_parser = api.parser()
logout_user_parser.add_argument('user_id', type=int, help='User ID', required=True, location='form')

@user_ns.route('/account/logout')
class UserLogOut(Resource):
    @user_ns.doc('logout_user')
    @user_ns.expect(logout_user_parser)
    def post(self):
        args = logout_user_parser.parse_args()
        user_id = args.get('user_id')
        user = User.query.get(user_id)
        user.fcm_token = None
        db.session.commit()
        return {"message": "Current user has been logged out."}, 200

login_user_parser = api.parser()
login_user_parser.add_argument('email', type=str, help='Email', required=True, location='form')
login_user_parser.add_argument('password', type=str, help='Password', required=True, location='form')

@user_ns.route('/account/login')
class UserAuthentication(Resource):
    @user_ns.doc('user_login')
    @user_ns.expect(login_user_parser)
    def post(self):
        args = login_user_parser.parse_args()
        email = args.get('email')
        password = args.get('password')
        user = User.query.filter(func.lower(User.email) == func.lower(email)).first()
        if not user:
            raise BadRequest("Invalid email or password.")
        if not bcrypt.checkpw(password.encode('utf-8'),user.password.encode('utf-8')):
            raise BadRequest("Invalid email or password.")
        jwt_token = create_access_token(identity=str(user.id))
        return {
            "status": "success",
            "token": jwt_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }, 200
    
# update fcm token
update_fcm_token_parser = api.parser()
update_fcm_token_parser.add_argument('user_id', type=int, help='User ID', required=True, location='form')
update_fcm_token_parser.add_argument('fcm_token', type=str, help='FCM Token', required=True, location='form')

@user_ns.route('/account/update-fcm-token')
class UpdateFcmToken(Resource):
    @user_ns.doc('update_fcm_token')
    @user_ns.expect(update_fcm_token_parser)
    def post(self):
        args = update_fcm_token_parser.parse_args()
        fcm_token = args.get('fcm_token')
        user_id =  args.get('user_id')
        user = User.query.get(user_id)
        if not user:
            raise BadRequest("User not found.")
        user.fcm_token = fcm_token
        db.session.commit()
        return {"message": "FCM Token has been updated."}, 200  

@user_ns.route('/account/profile')
class UserDetail(Resource):
    @user_ns.doc('fetch_user_details')
    # @user_ns.marshal_with(user_api_model,code=200)
    # @jwt_required
    def get(self):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            raise BadRequest("User not found.")

        return success_response(message="fetch user details successfull.",data=user.to_dict(),status_code=200)    
# End User
if __name__ == '__main__':
    app.run(debug=True)