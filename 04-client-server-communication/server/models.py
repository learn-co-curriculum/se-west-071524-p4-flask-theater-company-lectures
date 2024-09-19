# 📚 Review With Students:
# Validations and Invalid Data

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# 1.✅ Import validates from sqlalchemy.orm
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy(
    metadata=MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
)


class Production(db.Model, SerializerMixin):
    __tablename__ = "productions"

    id = db.Column(db.Integer, primary_key=True)

    # 2.✅ Add Constraints to the Columns

    title = db.Column(db.String, nullable=False, unique=True)
    genre = db.Column(db.String, nullable=False)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    director = db.Column(db.String)
    description = db.Column(db.String)
    ongoing = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    cast_members = db.relationship("CastMember", back_populates="production")

    serialize_rules = ("-cast_members.production",)

    # 3.✅ Use the "validates" decorator to create a validation for images
    # 3.1 Pass the decorator 'image'
    # 3.2 Define a validate_image method, pass it self, key and image_path
    # 3.3 If .jpg is not in the image passed, raise the ValueError exceptions else
    # return the image_path
    # Note: Feel free to try out more validations!

    @validates("image")
    def validate_image(self, key, image_url):
        if ".jpg" not in image_url:
            raise ValueError("Image file type must be .jpg")
        return image_url

    # 4.✅ navigate to app.py
    def __repr__(self):
        return f"<Production Title:{self.title}, Genre:{self.genre}, Budget:{self.budget}, Image:{self.image}, Director:{self.director},ongoing:{self.ongoing}>"


class Actor(db.Model, SerializerMixin):
    __tablename__ = "actors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    cast_members = db.relationship("CastMember", back_populates="actor")

    serialize_rules = ("-cast_members.actor",)

    def __repr__(self):
        return f"<Actor id: {self.id} name: {self.name} email: {self.email} >"


class CastMember(db.Model, SerializerMixin):
    __tablename__ = "cast_members"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    production_id = db.Column(db.Integer, db.ForeignKey("productions.id"))
    actor_id = db.Column(db.Integer, db.ForeignKey("actors.id"))

    production = db.relationship("Production", back_populates="cast_members")
    actor = db.relationship("Actor", back_populates="cast_members")

    serialize_rules = ("-production.cast_members", "-actor.cast_members")

    def __repr__(self):
        return f"<Production Name:{self.name}, Role:{self.role}"
