from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# create the database file in the current folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)




#define database model
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    # repr function returns a printable representation of the given object
    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"


# only run below line ones. If you already created the database.db ignore it
# careful, this line should be after the class. Because it will create the table as well
# db.create_all()

# to handle the received JSON message
video_put_args = reqparse.RequestParser()
# help displays that message to the sender in case that argument is not passed
video_put_args.add_argument('name', type=str, help="Name of the video is required", required=True)
video_put_args.add_argument('views', type=int, help="Views of the video is required", required=True)
video_put_args.add_argument('likes', type=int, help="Likes of the video is required", required=True)


# to handle the received JSON message for update request (used in patch method)
# this time not all information needed. So required is False by default
video_update_args = reqparse.RequestParser()
video_update_args.add_argument('name', type=str, help="Name of the video is required")
video_update_args.add_argument('views', type=int, help="Views of the video is required")
video_update_args.add_argument('likes', type=int, help="Likes of the video is required")


# used for serialize the objects
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    # take the return value, serialize it using resource_fields dictionary
    @marshal_with(resource_fields)
    def get(self,video_id):
        # query the database and return the first record
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Could not find video with that id')
        return result

    @marshal_with(resource_fields)
    def put(self,video_id):

        result = VideoModel.query.filter_by(id=video_id).first()

        if result:
            abort(404, message='Video id is already exists')

        args = video_put_args.parse_args()
        video = VideoModel(id = video_id, name = args['name'], views = args['views'], likes = args['likes'])


        db.session.add(video)
        db.session.commit()
        # Status code 201 means "Created"
        return video, 201

    # for updating
    @marshal_with(resource_fields)
    def patch(self, video_id):
        # get the data
        args = video_update_args.parse_args()

        #search for the video
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Video doesnt exists, cannot update')

        # we dont know what sender wants to update
        # the information is in args dict, but we dont know whether it is name, likes, or views
        # if the property is provided in the JSON then update that property
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']           
        if args['likes']:
            result.likes = args['likes']

        # result is an object gathered from VideoModel
        # if you just commmit changes, it will be updated
        db.session.commit()
        print(result)
        return result
        

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        db.session.delete(result)
        db.session.commit()
        # Status code 204 means "Deleted"
        return '',204

# video_id will be given in URL
api.add_resource(Video, "/video/<int:video_id>")


if __name__ == '__main__':
    app.run(debug=True)








    