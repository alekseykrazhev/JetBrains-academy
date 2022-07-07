from datetime import datetime

from flask import Flask, jsonify, request, abort
from flask_restful import Api, Resource, reqparse, inputs
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)
parser = reqparse.RequestParser()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'

parser.add_argument("event",
                    type=str,
                    help="The event name is required!",
                    required=True)
parser.add_argument("date",
                    type=inputs.date,
                    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
                    required=True)


class EventInfo(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)


class TodayEventResource(Resource):
    def get(self):
        today = datetime.now().date()
        events = EventInfo.query.filter_by(date=today).all()
        if events:
            ans = []
            for event in events:
                ans.append({'id': event.id, 'event': event.event, 'date': event.date.strftime('%Y-%m-%d')})
            return ans
        return jsonify({"data": "There are no events for today!"})


class EventResource(Resource):
    def get(self):
        args = request.args
        start_time = args.get('start_time')
        end_time = args.get('end_time')
        if start_time and end_time:
            events = EventInfo.query.filter(EventInfo.date >= start_time, EventInfo.date <= end_time).all()
        else:
            events = EventInfo.query.all()
        ans = []
        for event in events:
            ans.append({'id': event.id, 'event': event.event, 'date': event.date.strftime('%Y-%m-%d')})
        return ans

    def post(self):
        args = parser.parse_args()
        ei = EventInfo()
        ei.event = args['event']
        ei.date = args['date']
        db.session.add(ei)
        db.session.commit()
        return jsonify({"message": "The event has been added!", "event": str(args['event']), "date": str(datetime.date(args['date']))})


class EventByID(Resource):
    def get(self, event_id):
        event = EventInfo.query.filter(EventInfo.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        return jsonify({"id": event.id, "event": event.event, "date": event.date.strftime('%Y-%m-%d')})

    def delete(self, event_id):
        event = EventInfo.query.filter(EventInfo.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "The event has been deleted!"})


api.add_resource(EventResource, '/event')
api.add_resource(TodayEventResource, '/event/today')
api.add_resource(EventByID, '/event/<int:event_id>')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
