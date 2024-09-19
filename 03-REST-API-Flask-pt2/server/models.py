from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Production(db.Model, SerializerMixin):
    __tablename__ = "productions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    director = db.Column(db.String)
    description = db.Column(db.String)
    ongoing = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    cast_members = db.relationship("CastMember", back_populates="production")
    actors = association_proxy(
        "cast_members", "actor", creator=lambda actor_obj: CastMember(actor=actor_obj)
    )

    serialize_rules = (
        "-cast_members.production",  # this rule prevents recursions
        "-cast_members.production_id",
        "-created_at",
        "-updated_at",
    )

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

    serialize_rules = ("-cast_members.actor",)  # this rule prevents recursions

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

    serialize_rules = (
        "-production.cast_members",  # this rule prevents recursions
        "-actor.cast_members",  # this rule prevents recursions
        "-created_at",
        "-updated_at",
    )

    def __repr__(self):
        return f"<Production Name:{self.name}, Role:{self.role}"
