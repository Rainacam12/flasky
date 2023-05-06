from app import db

# create our model
class Crystal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    color = db.Column(db.String)
    powers = db.Column(db.String)

    @classmethod
    # in class methods, cls must come first. it's a reference to the class itself
    def from_dict(cls, crystal_data):
        new_crystal = Crystal(
            name=crystal_data["name"],
            color=crystal_data["color"],
            powers=crystal_data["powers"],
        )

        return new_crystal

    # create function to turn response into dict
    # no decorator needed bc we are using this on an object
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "powers": self.powers
        }