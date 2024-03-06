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

    def __int__(self, handle, email, city_code, city_desc, nickname, password):
        self.handle = handle
        self.email = email
        self.city_code = city_desc
        self.nickname = nickname
        self.password = password

    def __str__(self):
        return f'User(handle={self.handle}, email={self.email}, city_code={self.city_code}, nickname={self.nickname}, password={self.password})'


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


# 查（查所有）
def get_all_users():
    return User.query.all()
