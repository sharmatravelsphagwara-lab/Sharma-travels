from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sharma_travels.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.secret_key = "sharma_travels_luxury_secret_key"

# DATABASE--- #

class Package(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    continent = db.Column(db.String(100))
    duration = db.Column(db.String(100))
    price = db.Column(db.String(50))
    featured = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    image = db.Column(db.String(500))
    rating = db.Column(db.Float)


class Booking(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    package = db.Column(db.String(200))
    date = db.Column(db.String(50))
    status = db.Column(db.String(20))
    amount = db.Column(db.String(50))

class Review(db.Model):

    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    verified = db.Column(db.Boolean, default=True)
    approved = db.Column(db.Boolean, default=True)


class BusinessInfo(db.Model):

    __tablename__ = "business_info"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    whatsapp_primary = db.Column(db.String(20))
    whatsapp_secondary = db.Column(db.String(20))
    email = db.Column(db.String(100))
    instagram = db.Column(db.String(200))




with app.app_context():
    db.create_all()

    if BusinessInfo.query.first() is None:
        info = BusinessInfo(
            name="Sharma Travels",
            address="Shri Nath Palace, Old Post Office Road, Phagwara - 144401, Punjab, India",
            phone="01824-358008",
            whatsapp_primary="98880-82082",
            whatsapp_secondary="98880-82082",
            email="sharmatravelsphagwara@gmail.com",
            instagram="https://instagram.com/sharmatravelsphagwara"
        )
        db.session.add(info)
        db.session.commit()

# --- Routes --- #

@app.route("/")
def home():
    featured_packages = Package.query.filter_by(
        featured=True,
        active=True
    ).all()

    approved_reviews = Review.query.filter_by(
        approved=True
    ).all()

    info = BusinessInfo.query.first()

    return render_template(
        "home.html",
        info=info,
        package=featured_packages,
        reviews=approved_reviews
    )

@app.route("/package")
def package():

    category_filter = request.args.get("category", "")
    search_query = request.args.get("search", "")

    packages = Package.query.filter_by(active=True)

    if category_filter:
        packages = packages.filter(
            Package.category.ilike(category_filter)
        )

    if search_query:
        packages = packages.filter(
            (Package.title.ilike(f"%{search_query}%")) |
            (Package.category.ilike(f"%{search_query}%"))
        )

    packages = packages.all()

    info = BusinessInfo.query.first()

    return render_template(
        "package.html",
        info=info,
        package=packages,
        active_category=category_filter
    )

@app.route("/contact",methods=["GET","POST"])
def contact():
    if request.method == "POST":
        data = request.form

        # In production: save to database or send email #

        return render_template("contact.html", info=BusinessInfo, success=True, name=data.get("name"))
    
@app.route("/about",methods=["GET","POST"])
def about():
    return render_template("about.html", info=BusinessInfo, focus_map=True)

@app.route("/admin")
def admin_dashboard():

    info = BusinessInfo.query.first()

    packages = Package.query.all()
    bookings = Booking.query.all()
    reviews = Review.query.all()

    total_revenue = 0

    for booking in bookings:
        if booking.status == "Confirmed":
            amount = Booking.amount.replace("₹", "").replace(",", "")
            total_revenue += int(amount)

    stats = {
        "today_bookings": len(bookings),
        "total_revenue": f"₹{total_revenue:,}",
        "pending_bookings": Booking.query.filter_by(status="Pending").count(),
        "total_packages": Package.query.count(),
        "total_reviews": Review.query.count()
    }

    return render_template(
        "admin.html",
        info=info,
        stats=stats,
        package=packages,
        bookings=bookings,
        reviews=reviews
    )

# --- API Endpoints --- #

@app.route("/api/book", methods=["POST"])
def create_booking():

    booking = Booking(
        customer=request.form.get("name"),
        phone=request.form.get("phone"),
        package=request.form.get("package_title"),
        date=request.form.get("travel_date"),
        amount=request.form.get("price"),
        status="Confirmed"
    )

    db.session.add(booking)
    db.session.commit()

    return redirect(url_for("package"))



if __name__ == "__main__":
    app.run(debug=True, port=5000)

    with app.app_context():
        db.creat_all()