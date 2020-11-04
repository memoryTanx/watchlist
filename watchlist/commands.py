import click

from . import app, db
from .models import User, Movie, Message


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """生成伪造数据"""
    db.create_all()

    name = 'Memory'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    messages = [
        {'movie_id': 1, 'talker': '小1', 'message': '真不错'},
        {'movie_id': 1, 'talker': '小5', 'message': '针不戳...'},
        {'movie_id': 2, 'talker': '小2', 'message': '挺好！'},
        {'movie_id': 3, 'talker': '小3', 'message': '整挺好。'},
        {'movie_id': 4, 'talker': '小4', 'message': '辣鸡...'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    for m in messages:
        message = Message(movie_id=m['movie_id'], talker=m['talker'], message=m['message'])
        db.session.add(message)

    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='登陆用户名')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='登陆密码')
def admin(username, password):
    """创建用户"""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('更新用户...')
        user.username = username
        user.set_password(password) # 设置密码
    else:
        click.echo('添加用户...')
        user = User(username=username, name='Admin')
        user.set_password(password) # 设置密码
        db.session.add(user)

    db.session.commit() # 提交数据库会话
    click.echo('完成！')
