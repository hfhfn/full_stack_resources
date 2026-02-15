from common.models.user import TimeModel
from common.models import db


class Question(db.Model, TimeModel):
    """
    问题基本信息
    """
    __tablename__ = 'question_basic'

    class STATUS:
        AUDIT = 1
        AUDITED_Y = 2
        AUDITED_N = 3
        DELETED = 4

    id = db.Column('qust_id', db.Integer, primary_key=True, doc='问题ID')
    user_id = db.Column(db.Integer, doc='提问问题的用户ID')
    expertise_id = db.Column(db.Integer,doc='问题所属专业ID')
    city_id = db.Column(db.Integer, doc='事发城市id')
    title = db.Column(db.String, doc='标题')
    cover = db.Column(db.JSON, doc='封面')
    status = db.Column(db.Integer, default=1, doc='提问状态，1-待审核，2-审核通过，3-审核失败，4-已删除')
    reviewer_id = db.Column(db.Integer, doc='审核人员ID')
    review_time = db.Column(db.DateTime, doc='审核时间')
    delete_time = db.Column(db.DateTime, doc='删除时间')
    reject_reason = db.Column(db.String, doc='驳回原因')
    answer_count = db.Column(db.Integer, default=0, doc='已解答数量')
    cover = db.Column(db.JSON, doc='封面')


class QuestionContent(db.Model):
    """
    问题内容信息
    """
    __tablename__ = 'question_content'

    id = db.Column('qust_id', db.Integer, primary_key=True, doc='问题ID')
    content = db.Column(db.String, doc='问题内容')


class Answer(db.Model, TimeModel):
    """
    解答信息
    """
    __tablename__ = 'answer'

    class STATUS:
        AUDIT = 1
        AUDITED_Y = 2
        AUDITED_N = 3
        DELETED = 4

    id = db.Column('answer_id', db.Integer, primary_key=True, doc='解答id')
    lawyer_id = db.Column(db.Integer, doc='律师用户ID')
    qust_id = db.Column(db.Integer, doc='提问的ID')
    content = db.Column(db.String, doc='解答内容')
    status = db.Column(db.Integer, default=1, doc='状态，1-待审核，2-审核通过，3-审核失败，4-已删除')
