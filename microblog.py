from app import create_app, db, cli
import unittest
from app.models import User, Post, Message, Notification, Task, TrainerProfile, CustomerProfile

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notification, 'Task': Task,
             'TrainerProfile': TrainerProfile,
             'CustomerProfile': CustomerProfile,
             'unittest': unittest}
