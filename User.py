from config import db


# USER 类
class User(db.Model):
    __tablename__ = 'user'
    handle = db.Column(db.String(500), primary_key=True)
    email = db.Column(db.String(320), nullable=False)
    city_code = db.Column(db.String(10), nullable=False)
    city_desc = db.Column(db.String(100))
    nickname = db.Column(db.String(100))
    password = db.Column(db.String(13))
    receive_time = db.Column(db.Time)

    def __int__(self, handle, email, city_code, city_desc, nickname, password, receive_time):
        self.handle = handle
        self.email = email
        self.city_code = city_desc
        self.nickname = nickname
        self.password = password
        self.receive_time = receive_time

    def __str__(self):
        return f'User(handle={self.handle}, email={self.email}, city_code={self.city_code}, city_desc={self.city_desc}, nickname={self.nickname}, password={self.password}, receive_time={self.receive_time})'


# 增
def insert_user(user):
    db.session.add(user)
    db.session.commit()
    return f'{user.handle} 新建成功'


# 删
def remove_user_by_handle(handle):
    user = User.query.filter_by(handle=handle).first()
    db.session.delete(user)
    db.session.commit()
    return f'{handle} 删除成功'


# 改
def update_user(handle, user):
    remove_user_by_handle(handle)
    insert_user(user)


# 查（按邮箱查）
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user


def get_user_by_email_and_city(email, city_code):
    user = User.query.filter_by(email=email, city_code=city_code).first()
    return user


# 查（按receive_time）
def get_users_by_time(time):
    # datetime.time(hour=7, minute=15, second=0)
    users = User.query.filter_by(receive_time=time)
    return users


# 查（查所有）
def get_all_users():
    return User.query.all()
