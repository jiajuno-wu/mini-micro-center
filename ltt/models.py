from ltt import db,app
  #from this package import the db object 

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer,primary_key = True)
    item_name = db.Column(db.String(20))
    item_price = db.Column(db.Integer)
    item_image = db.Column(db.String(20), default = "default.jpg")
    item_type = db.Column(db.String(20))
    item_c = db.Column(db.Integer)
    comments = db.relationship("Comment",backref ="item")
    rate_count = db.Column(db.Integer, default = 0)
    rate_acc = db.Column(db.Integer,default = 0)
    def __repr__(self):
        return f'<Item"{self.item_name}">'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(120))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    
    def __repr__(self):
        return f'<Comment"{self.content}">'


with app.app_context():
    #db.drop_all()
    db.create_all()

