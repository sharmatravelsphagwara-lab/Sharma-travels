from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    
)
import json
with open("Travel.json", "r") as file:
    config = json.load(file)


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sharma_travels.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "sharma_travels_luxury_secret_key"

db = SQLAlchemy(app)


# =========================================================
# USER MODEL
# =========================================================

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    phone = db.Column(
        db.String(30)
    )


# =========================================================
# PACKAGE MODEL
# =========================================================

class Package(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    category = db.Column(
        db.String(100)
    )

    continent = db.Column(
        db.String(100)
    )

    duration = db.Column(
        db.String(100)
    )

    price = db.Column(
        db.String(50)
    )

    featured = db.Column(
        db.Boolean,
        default=False
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    image = db.Column(
        db.String(500)
    )

    rating = db.Column(
        db.Float,
        default=0
    )


# =========================================================
# BOOKING MODEL
# =========================================================

class Booking(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer
    )

    customer = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100)
    )

    phone = db.Column(
        db.String(30)
    )

    age = db.Column(
        db.Integer
    )

    gender = db.Column(
        db.String(30)
    )

    package = db.Column(
        db.String(200)
    )

    destination = db.Column(
        db.String(150)
    )

    date = db.Column(
        db.String(50)
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    amount = db.Column(
        db.String(50)
    )


# =========================================================
# REVIEW MODEL
# =========================================================

class Review(db.Model):

    __tablename__ = "reviews"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100)
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    comment = db.Column(
        db.Text,
        nullable=False
    )

    verified = db.Column(
        db.Boolean,
        default=True
    )

    approved = db.Column(
        db.Boolean,
        default=True
    )


# =========================================================
# BUSINESS INFORMATION MODEL
# =========================================================

class BusinessInfo(db.Model):

    __tablename__ = "business_info"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100)
    )

    address = db.Column(
        db.Text
    )

    phone = db.Column(
        db.String(30)
    )

    whatsapp_primary = db.Column(
        db.String(30)
    )

    whatsapp_secondary = db.Column(
        db.String(30)
    )

    email = db.Column(
        db.String(100)
    )

    instagram = db.Column(
        db.String(200)
    )


# =========================================================
# CONTACT MODEL
# =========================================================

class Contact(db.Model):

    __tablename__ = "contacts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100)
    )

    phone = db.Column(
        db.String(30)
    )

    destination = db.Column(
        db.String(100)
    )

    travel_date = db.Column(
        db.String(50)
    )

    travellers = db.Column(
        db.String(20)
    )

    message = db.Column(
        db.Text
    )


# =========================================================
# WISHLIST MODEL
# =========================================================

class Wishlist(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    package_id = db.Column(
        db.Integer,
        nullable=False
    )


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

with app.app_context():

    db.create_all()

    # -----------------------------------------------------
    # BUSINESS INFORMATION
    # -----------------------------------------------------

    if BusinessInfo.query.first() is None:

        db.session.add(
            BusinessInfo(

                name="Sharma Travels",

                address=(
                    "Shri Nath Palace, Old Post Office Road, "
                    "Phagwara - 144401, Punjab"
                ),

                phone="01824-358008",

                whatsapp_primary="9888082082",

                whatsapp_secondary="9888501312",

                email="sharmatravelsphagwara@gmail.com",

                instagram=(
                    "https://instagram.com/"
                    "sharmatravelsphagwara"
                )
            )
        )


    # -----------------------------------------------------
    # DEFAULT PACKAGES
    # -----------------------------------------------------

    if Package.query.count() == 0:

        db.session.add_all([

            Package(
                title="Dubai Luxury Tour",
                category="International",
                continent="Asia",
                duration="5 Days / 4 Nights",
                price="₹59,999",
                featured=True,
                active=True,
                image="dubai.jpg",
                rating=4.9
            ),

            Package(
                title="Bali Paradise",
                category="International",
                continent="Asia",
                duration="6 Days / 4 Nights",
                price="₹49,999",
                featured=True,
                active=True,
                image="bali.jpg",
                rating=4.8
            ),

            Package(
                title="Singapore Explorer",
                category="International",
                continent="Asia",
                duration="5 Days / 4 Nights",
                price="₹54,999",
                featured=True,
                active=True,
                image="singapore.jpg",
                rating=4.9
            ),

            Package(
                title="Maldives Luxury Holiday",
                category="Luxury",
                continent="Asia",
                duration="5 Days / 4 Nights",
                price="₹69,999",
                featured=True,
                active=True,
                image="maldives.jpg",
                rating=5.0
            )

        ])


    # -----------------------------------------------------
    # DEFAULT REVIEWS
    # -----------------------------------------------------

    if Review.query.count() == 0:

        db.session.add_all([

            Review(
                name="Rahul Sharma",
                rating=5,
                comment="Excellent Service",
                verified=True,
                approved=True
            ),

            Review(
                name="Priya Kaur",
                rating=5,
                comment="Best Travel Agency",
                verified=True,
                approved=True
            ),

            Review(
                name="Aman Singh",
                rating=4,
                comment="Great Experience",
                verified=True,
                approved=True
            )

        ])


    db.session.commit()


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    info = BusinessInfo.query.first()

    featured_packages = Package.query.filter_by(
        featured=True,
        active=True
    ).all()

    approved_reviews = Review.query.filter_by(
        approved=True
    ).all()

    return render_template(
        "home.html",
        info=info,
        package=featured_packages,
        reviews=approved_reviews
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    info = BusinessInfo.query.first()

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if not name or not email or not password:

            return render_template(
                "register.html",
                info=info,
                error="Please fill all fields."
            )

        if len(password) < 6:

            return render_template(
                "register.html",
                info=info,
                error="Password must be at least 6 characters."
            )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            return render_template(
                "register.html",
                info=info,
                error="Email already registered."
            )

        hashed_password = generate_password_hash(
            password
        )

        user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html",
        info=info
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    info = BusinessInfo.query.first()

    if request.method == "POST":

        email = request.form.get("Email")

        if not email:
            email = request.form.get("email")

        password = request.form.get(
            "password",
            ""
        )

        email = (
            email.strip().lower()
            if email
            else ""
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session["user_id"] = user.id
            session["user_name"] = user.name
            session["user_email"] = user.email

            return redirect(
                url_for("home")
            )

        return render_template(
            "login.html",
            info=info,
            error="Invalid Email or Password"
        )

    return render_template(
        "login.html",
        info=info
    )


# =========================================================
# USER LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.pop(
        "user_id",
        None
    )

    session.pop(
        "user_name",
        None
    )

    session.pop(
        "user_email",
        None
    )

    return redirect(
        url_for("home")
    )


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():

    if not session.get("user_id"):

        return redirect(
            url_for("login")
        )

    user = User.query.get(
        session.get("user_id")
    )

    if not user:

        session.clear()

        return redirect(
            url_for("login")
        )

    bookings = Booking.query.filter_by(
        user_id=user.id
    ).all()

    reviews = Review.query.filter_by(
        user_id=user.id
    ).all()

    wishlist = Wishlist.query.filter_by(
        user_id=user.id
    ).all()

    return render_template(
        "profile.html",
        user=user,
        bookings=bookings,
        reviews=reviews,
        wishlist=wishlist
    )

# =========================================================
# PACKAGES
# =========================================================

@app.route("/package")
def package():

    info = BusinessInfo.query.first()

    category_filter = request.args.get(
        "category",
        ""
    ).strip()

    search_query = request.args.get(
        "search",
        ""
    ).strip()

    packages = Package.query.filter_by(
        active=True
    )

    if category_filter:

        packages = packages.filter(
            Package.category.ilike(
                f"%{category_filter}%"
            )
        )

    if search_query:

        packages = packages.filter(
            or_(
                Package.title.ilike(
                    f"%{search_query}%"
                ),

                Package.category.ilike(
                    f"%{search_query}%"
                ),

                Package.continent.ilike(
                    f"%{search_query}%"
                )
            )
        )

    packages = packages.all()

    return render_template(
        "package.html",
        info=info,
        package=packages,
        active_category=category_filter,
        search=search_query
    )


# =========================================================
# PACKAGE DETAILS
# =========================================================

@app.route("/package/<int:id>")
def package_details(id):

    info = BusinessInfo.query.first()

    package_item = Package.query.get_or_404(id)

    return render_template(
        "package_details.html",
        info=info,
        package=package_item
    )


# =========================================================
# DESTINATION
# =========================================================

@app.route("/destination")
def destination():

    info = BusinessInfo.query.first()

    packages = Package.query.filter_by(
        active=True
    ).all()

    return render_template(
        "destination.html",
        info=info,
        package=packages
    )


# =========================================================
# CONTACT
# =========================================================

@app.route(
    "/contact",
    methods=["GET", "POST"]
)
def contact():

    info = BusinessInfo.query.first()

    if request.method == "POST":

        enquiry = Contact(

            name=request.form.get(
                "name",
                ""
            ).strip(),

            email=request.form.get(
                "email",
                ""
            ).strip(),

            phone=request.form.get(
                "phone",
                ""
            ).strip(),

            destination=request.form.get(
                "destination",
                ""
            ).strip(),

            travel_date=request.form.get(
                "travel_date"
            ),

            travellers=request.form.get(
                "travellers"
            ),

            message=request.form.get(
                "message",
                ""
            ).strip()
        )

        db.session.add(enquiry)

        db.session.commit()

        return render_template(
            "thanks.html",
            info=info,
            name=enquiry.name
        )

    return render_template(
        "contact.html",
        info=info
    )


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
def about():

    info = BusinessInfo.query.first()

    return render_template(
        "about.html",
        info=info
    )


# =========================================================
# REVIEWS
# =========================================================

@app.route(
    "/review",
    methods=["GET", "POST"]
)
def review():

    info = BusinessInfo.query.first()

    # -----------------------------------------------------
    # SUBMIT REVIEW
    # -----------------------------------------------------

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        rating = request.form.get(
            "rating"
        )

        comment = request.form.get(
            "comment",
            ""
        ).strip()

        if not name or not rating or not comment:

            reviews = Review.query.filter_by(
                approved=True
            ).order_by(
                Review.id.desc()
            ).all()

            return render_template(
                "review.html",
                info=info,
                reviews=reviews,
                error="Please fill all review fields."
            )

        try:
            rating = int(rating)
        except ValueError:

            return render_template(
                "review.html",
                info=info,
                reviews=Review.query.filter_by(
                    approved=True
                ).all(),
                error="Invalid rating."
            )

        if rating < 1 or rating > 5:

            return render_template(
                "review.html",
                info=info,
                reviews=Review.query.filter_by(
                    approved=True
                ).all(),
                error="Rating must be between 1 and 5."
            )

        new_review = Review(

            user_id=session.get(
                "user_id"
            ),

            name=name,

            email=session.get(
                "user_email"
            ),

            rating=rating,

            comment=comment,

            verified=True,

            approved=True
        )

        db.session.add(new_review)

        db.session.commit()

        return redirect(
            url_for("review")
        )

    # -----------------------------------------------------
    # SHOW REVIEWS
    # -----------------------------------------------------

    reviews = Review.query.filter_by(
        approved=True
    ).order_by(
        Review.id.desc()
    ).all()

    return render_template(
        "review.html",
        info=info,
        reviews=reviews
    )


# =========================================================
# BOOKING
# =========================================================

@app.route(
    "/booking",
    methods=["GET", "POST"]
)
def booking():

    # Login required

    if not session.get("user_id"):

        return redirect(
            url_for("login")
        )

    info = BusinessInfo.query.first()

    user = User.query.get(
        session.get("user_id")
    )

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        age = request.form.get(
            "age"
        )

        gender = request.form.get(
            "gender"
        )

        plan = request.form.get(
            "plan"
        )

        package_title = request.form.get(
            "package_title"
        )

        destination = request.form.get(
            "destination"
        )

        travel_date = request.form.get(
            "travel_date"
        )

        # ---------------------------------------------
        # VALIDATION
        # ---------------------------------------------

        if not name or not email or not phone:

            return render_template(
                "booking.html",
                info=info,
                user=user,
                error="Please fill all required fields."
            )

        # ---------------------------------------------
        # GET PACKAGE PRICE
        # ---------------------------------------------

        selected_package = None

        if package_title:

            selected_package = Package.query.filter_by(
                title=package_title
            ).first()

        amount = None

        if selected_package:

            amount = selected_package.price

        # If form sends price separately

        if not amount:

            amount = request.form.get(
                "price"
            )

        # ---------------------------------------------
        # CREATE BOOKING
        # ---------------------------------------------

        new_booking = Booking(

            user_id=session.get(
                "user_id"
            ),

            customer=name,

            email=email,

            phone=phone,

            age=int(age) if age and age.isdigit() else None,

            gender=gender,

            package=package_title or plan,

            destination=destination,

            date=travel_date,

            status="Pending",

            amount=amount
        )

        db.session.add(
            new_booking
        )

        db.session.commit()

        return redirect(
            url_for("booking_success")
        )

    # ---------------------------------------------
    # GET REQUEST
    # ---------------------------------------------

    package_title = request.args.get(
        "package",
        ""
    )

    selected_package = None

    if package_title:

        selected_package = Package.query.filter_by(
            title=package_title
        ).first()

    packages = Package.query.filter_by(
        active=True
    ).all()

    return render_template(
        "booking.html",
        info=info,
        user=user,
        packages=packages,
        selected_package=selected_package
    )


# =========================================================
# BOOKING SUCCESS
# =========================================================

@app.route("/booking_success")
def booking_success():

    if not session.get("user_id"):

        return redirect(
            url_for("login")
        )

    info = BusinessInfo.query.first()

    return render_template(
        "booking_success.html",
        info=info
    )



# =========================================================
# WISHLIST
# =========================================================

@app.route("/wishlist")
def wishlist():

    # User login check
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Business information
    info = BusinessInfo.query.first()

    # Get wishlist records of current user
    wishlist_items = Wishlist.query.filter_by(
        user_id=session.get("user_id")
    ).all()

    # Get actual packages
    wishlist_packages = []

    for item in wishlist_items:

        package_item = db.session.get(
            Package,
            item.package_id
        )

        if package_item:
            wishlist_packages.append(package_item)

    return render_template(
        "wishlist.html",
        info=info,
        wishlist=wishlist_packages
    )


# =========================================================
# ADD TO WISHLIST
# =========================================================

@app.route(
    "/wishlist/add/<int:package_id>",
    methods=["GET", "POST"]
)
def add_to_wishlist(package_id):

    # User login check
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Check package exists
    package_item = db.session.get(
        Package,
        package_id
    )

    if not package_item:
        return redirect(url_for(""))

    # Check if already in wishlist
    existing = Wishlist.query.filter_by(
        user_id=session.get("user_id"),
        package_id=package_item.id
    ).first()

    # Add only if not already present
    if not existing:

        wishlist_item = Wishlist(
            user_id=session.get("user_id"),
            package_id=package_item.id
        )

        db.session.add(wishlist_item)
        db.session.commit()

    # Return to previous page
    return redirect(
        request.referrer or
        url_for("wishlist")
    )


# =========================================================
# REMOVE FROM WISHLIST
# =========================================================

@app.route(
    "/wishlist/remove/<int:package_id>"
)
def remove_from_wishlist(package_id):

    # User login check
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Find wishlist item
    wishlist_item = Wishlist.query.filter_by(
        user_id=session.get("user_id"),
        package_id=package_id
    ).first()

    # Delete item
    if wishlist_item:

        db.session.delete(
            wishlist_item
        )

        db.session.commit()

    return redirect(
        url_for("wishlist")
    )


# =========================================================
# SEARCH API
# =========================================================

@app.route("/search")
def search():

    query = request.args.get(
        "q",
        ""
    ).strip()

    if not query:
        return jsonify([])

    packages = Package.query.filter(

        or_(
            Package.title.ilike(
                f"%{query}%"
            ),

            Package.category.ilike(
                f"%{query}%"
            ),

            Package.continent.ilike(
                f"%{query}%"
            )
        )

    ).filter_by(
        active=True
    ).all()

    return jsonify([

        {
            "id": package.id,
            "title": package.title,
            "category": package.category,
            "continent": package.continent,
            "duration": package.duration,
            "price": package.price,
            "image": package.image,
            "rating": package.rating
        }

        for package in packages

    ])
# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if session.get("admin"):
        return redirect(
            url_for("admin_dashboard")
        )

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        # -------------------------------------------------
        # ADMIN LOGIN DETAILS
        # -------------------------------------------------

        if (
            username == "admin"
            and password == "765809"
        ):

            session["admin"] = True

            return redirect(
                url_for("admin_dashboard")
            )

        return render_template(
            "admin_login.html",
            error="Invalid Username or Password"
        )

    return render_template(
        "admin_login.html"
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "admin",
        None
    )

    return redirect(
        url_for("admin_login")
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
def admin_dashboard():

    # -----------------------------------------------------
    # ADMIN SECURITY
    # -----------------------------------------------------

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    info = BusinessInfo.query.first()

    # -----------------------------------------------------
    # DATABASE DATA
    # -----------------------------------------------------

    users = User.query.order_by(
        User.id.desc()
    ).all()

    packages = Package.query.order_by(
        Package.id.desc()
    ).all()

    bookings = Booking.query.order_by(
        Booking.id.desc()
    ).all()

    reviews = Review.query.order_by(
        Review.id.desc()
    ).all()

    contacts = Contact.query.order_by(
        Contact.id.desc()
    ).all()

    # -----------------------------------------------------
    # REVENUE CALCULATION
    # -----------------------------------------------------

    total_revenue = 0

    for booking_item in bookings:

        if booking_item.status == "Confirmed":

            try:

                amount = str(
                    booking_item.amount or ""
                )

                amount = amount.replace(
                    "₹",
                    ""
                )

                amount = amount.replace(
                    ",",
                    ""
                )

                amount = amount.strip()

                total_revenue += float(
                    amount
                )

            except (
                ValueError,
                TypeError
            ):

                pass

    # -----------------------------------------------------
    # BOOKING COUNTS
    # -----------------------------------------------------

    pending_bookings = Booking.query.filter_by(
        status="Pending"
    ).count()

    confirmed_bookings = Booking.query.filter_by(
        status="Confirmed"
    ).count()

    cancelled_bookings = Booking.query.filter_by(
        status="Cancelled"
    ).count()

    # -----------------------------------------------------
    # STATS
    # -----------------------------------------------------

    stats = {

        "users": User.query.count(),

        "packages": Package.query.count(),

        "bookings": Booking.query.count(),

        "reviews": Review.query.count(),

        "contacts": Contact.query.count(),

        "revenue": f"₹{total_revenue:,.0f}",

        "pending_bookings": pending_bookings,

        "confirmed_bookings": confirmed_bookings,

        "cancelled_bookings": cancelled_bookings
    }

    # -----------------------------------------------------
    # ADMIN TEMPLATE
    # -----------------------------------------------------

    return render_template(

        "admin.html",

        info=info,

        stats=stats,

        users=users,

        package=packages,

        packages=packages,

        bookings=bookings,

        reviews=reviews,

        contacts=contacts
    )


# =========================================================
# ADD PACKAGE
# =========================================================

@app.route(
    "/admin/add-package",
    methods=["GET", "POST"]
)
def add_package():

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    info = BusinessInfo.query.first()

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        continent = request.form.get(
            "continent",
            ""
        ).strip()

        duration = request.form.get(
            "duration",
            ""
        ).strip()

        price = request.form.get(
            "price",
            ""
        ).strip()

        image = request.form.get(
            "image",
            ""
        ).strip()

        rating = request.form.get(
            "rating",
            "0"
        )

        featured = request.form.get(
            "featured"
        )

        active = request.form.get(
            "active"
        )

        # -------------------------------------------------
        # RATING VALIDATION
        # -------------------------------------------------

        try:

            rating_value = float(
                rating
            )

        except (
            ValueError,
            TypeError
        ):

            rating_value = 0

        # -------------------------------------------------
        # CREATE PACKAGE
        # -------------------------------------------------

        new_package = Package(

            title=title,

            category=category,

            continent=continent,

            duration=duration,

            price=price,

            image=image,

            rating=rating_value,

            featured=True
            if featured
            else False,

            active=True
            if active != "0"
            else False
        )

        db.session.add(
            new_package
        )

        db.session.commit()

        return redirect(
            url_for("admin_dashboard")
        )

    return render_template(
        "add_package.html",
        info=info
    )


# =========================================================
# EDIT PACKAGE
# =========================================================

@app.route(
    "/admin/edit-package/<int:id>",
    methods=["GET", "POST"]
)
def edit_package(id):

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    info = BusinessInfo.query.first()

    package_item = Package.query.get_or_404(
        id
    )

    if request.method == "POST":

        package_item.title = request.form.get(
            "title",
            ""
        ).strip()

        package_item.category = request.form.get(
            "category",
            ""
        ).strip()

        package_item.continent = request.form.get(
            "continent",
            ""
        ).strip()

        package_item.duration = request.form.get(
            "duration",
            ""
        ).strip()

        package_item.price = request.form.get(
            "price",
            ""
        ).strip()

        package_item.image = request.form.get(
            "image",
            ""
        ).strip()

        rating = request.form.get(
            "rating",
            "0"
        )

        try:

            package_item.rating = float(
                rating
            )

        except (
            ValueError,
            TypeError
        ):

            package_item.rating = 0

        package_item.featured = (
            True
            if request.form.get("featured")
            else False
        )

        package_item.active = (
            False
            if request.form.get("active") == "0"
            else True
        )

        db.session.commit()

        return redirect(
            url_for("admin_dashboard")
        )

    return render_template(
        "edit_package.html",
        info=info,
        package=package_item
    )


# =========================================================
# DELETE PACKAGE
# =========================================================

@app.route(
    "/admin/delete-package/<int:id>"
)
def delete_package(id):

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    package_item = Package.query.get_or_404(
        id
    )

    # -----------------------------------------------------
    # REMOVE WISHLIST REFERENCES FIRST
    # -----------------------------------------------------

    Wishlist.query.filter_by(
        package_id=package_item.id
    ).delete(
        synchronize_session=False
    )

    db.session.delete(
        package_item
    )

    db.session.commit()

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# UPDATE BOOKING STATUS
# =========================================================

@app.route(
    "/admin/booking/<int:id>/status",
    methods=["POST"]
)
def update_booking_status(id):

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    booking_item = Booking.query.get_or_404(
        id
    )

    status = request.form.get(
        "status",
        "Pending"
    )

    allowed_statuses = [
        "Pending",
        "Confirmed",
        "Cancelled"
    ]

    if status in allowed_statuses:

        booking_item.status = status

        db.session.commit()

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# DELETE BOOKING
# =========================================================

@app.route(
    "/admin/delete-booking/<int:id>"
)
def delete_booking(id):

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    booking_item = Booking.query.get_or_404(
        id
    )

    db.session.delete(
        booking_item
    )

    db.session.commit()

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# APPROVE REVIEW
# =========================================================

@app.route(
    "/admin/review/<int:id>/approve"
)
def approve_review(id):

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    review_item = Review.query.get_or_404(
        id
    )

    review_item.approved = True

    db.session.commit()

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# HIDE REVIEW
# =========================================================

@app.route(
    "/admin/review/<int:id>/hide"
)
def hide_review(id):

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    review_item = Review.query.get_or_404(
        id
    )

    review_item.approved = False

    db.session.commit()

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# DELETE REVIEW
# =========================================================

@app.route(
    "/admin/delete-review/<int:id>"
)
def delete_review(id):

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    review_item = Review.query.get_or_404(
        id
    )

    db.session.delete(
        review_item
    )

    db.session.commit()

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# DELETE CONTACT
# =========================================================

@app.route(
    "/admin/delete-contact/<int:id>"
)
def delete_contact(id):

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    contact_item = Contact.query.get_or_404(
        id
    )

    db.session.delete(
        contact_item
    )

    db.session.commit()

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# DELETE USER
# =========================================================

@app.route(
    "/admin/delete-user/<int:id>"
)
def delete_user(id):

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )

    user = User.query.get_or_404(
        id
    )

    # -----------------------------------------------------
    # DELETE USER'S WISHLIST
    # -----------------------------------------------------

    Wishlist.query.filter_by(
        user_id=user.id
    ).delete(
        synchronize_session=False
    )

    # -----------------------------------------------------
    # DELETE USER'S BOOKINGS
    # -----------------------------------------------------

    Booking.query.filter_by(
        user_id=user.id
    ).delete(
        synchronize_session=False
    )

    # -----------------------------------------------------
    # DELETE USER'S REVIEWS
    # -----------------------------------------------------

    Review.query.filter_by(
        user_id=user.id
    ).delete(
        synchronize_session=False
    )

    db.session.delete(
        user
    )

    db.session.commit()

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# ADMIN QUICK STATS API
# =========================================================

@app.route("/admin/api/stats")
def admin_stats_api():

    if not session.get("admin"):

        return jsonify({
            "error": "Unauthorized"
        }), 401

    total_revenue = 0

    confirmed_bookings = Booking.query.filter_by(
        status="Confirmed"
    ).all()

    for booking_item in confirmed_bookings:

        try:

            amount = str(
                booking_item.amount or ""
            )

            amount = amount.replace(
                "₹",
                ""
            )

            amount = amount.replace(
                ",",
                ""
            )

            total_revenue += float(
                amount
            )

        except (
            ValueError,
            TypeError
        ):

            pass

    return jsonify({

        "users": User.query.count(),

        "packages": Package.query.count(),

        "bookings": Booking.query.count(),

        "reviews": Review.query.count(),

        "contacts": Contact.query.count(),

        "revenue": total_revenue,

        "pending": Booking.query.filter_by(
            status="Pending"
        ).count(),

        "confirmed": Booking.query.filter_by(
            status="Confirmed"
        ).count(),

        "cancelled": Booking.query.filter_by(
            status="Cancelled"
        ).count()
    })


# =========================================================
# 404 ERROR
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    info = BusinessInfo.query.first()

    return render_template(
        "404.html",
        info=info
    ), 404


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )