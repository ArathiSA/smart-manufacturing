from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

# Secret key for login session
app.secret_key = "smart-manufacturing-secret-key"


# =========================
# DATABASE
# =========================

def create_database():

    connection = sqlite3.connect("manufacturing.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# PRODUCTS
# =========================

@app.route("/products")
def products():
    return render_template("products.html")


# =========================
# PRODUCT DETAILS
# =========================

@app.route("/product/<product_name>")
def product_details(product_name):

    products_data = {

        "machine-parts": {
            "name": "Machine Parts",
            "icon": "⚙️",
            "price": "₹3,500",
            "description": "High-quality machine parts designed for reliable industrial performance and long-term usage.",
            "features": [
                "High-quality materials",
                "Strong and durable construction",
                "Reliable industrial performance",
                "Suitable for different machines"
            ]
        },

        "steel-components": {
            "name": "Steel Components",
            "icon": "🔩",
            "price": "₹5,000",
            "description": "Strong and durable steel components manufactured for industrial applications.",
            "features": [
                "High-strength steel",
                "Corrosion-resistant",
                "Precision manufacturing",
                "Long-lasting performance"
            ]
        },

        "metal-sheets": {
            "name": "Metal Sheets",
            "icon": "🏗️",
            "price": "₹2,000",
            "description": "Quality metal sheets suitable for construction, fabrication and various industrial requirements.",
            "features": [
                "High-quality metal",
                "Smooth surface finish",
                "Different application support",
                "Durable and reliable"
            ]
        },

        "industrial-tools": {
            "name": "Industrial Tools",
            "icon": "🔧",
            "price": "₹1,500",
            "description": "Reliable industrial tools designed to support efficient manufacturing and maintenance work.",
            "features": [
                "Strong construction",
                "Easy to use",
                "Suitable for industrial work",
                "Reliable performance"
            ]
        }
    }

    product = products_data.get(product_name)

    if product is None:
        return "Product Not Found", 404

    return render_template(
        "product_details.html",
        product=product
    )


# =========================
# PRODUCTION
# =========================

@app.route("/production")
def production():
    return render_template("production.html")


# =========================
# CONTACT
# =========================

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        connection = sqlite3.connect("manufacturing.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO messages
            (name, email, subject, message)
            VALUES (?, ?, ?, ?)
        """, (name, email, subject, message))

        connection.commit()
        connection.close()

        print("\n========== CONTACT MESSAGE ==========")
        print("Name:", name)
        print("Email:", email)
        print("Subject:", subject)
        print("Message:", message)
        print("Saved to database successfully!")
        print("=====================================\n")

        return render_template(
            "contact.html",
            success="Your message has been sent successfully!"
        )

    return render_template("contact.html")


# =========================
# ADMIN LOGIN
# =========================

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Demo admin credentials
        if username == "admin" and password == "admin123":

            session["admin_logged_in"] = True

            return redirect("/admin")

        return render_template(
            "admin_login.html",
            error="Invalid username or password!"
        )

    return render_template("admin_login.html")


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin")
def admin():

    # Check login
    if not session.get("admin_logged_in"):
        return redirect("/admin-login")

    connection = sqlite3.connect("manufacturing.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM messages
        ORDER BY id DESC
    """)

    messages = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) FROM messages
    """)

    total_messages = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "admin.html",
        messages=messages,
        total_messages=total_messages
    )


# =========================
# DELETE MESSAGE
# =========================

@app.route("/delete-message/<int:message_id>")
def delete_message(message_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin-login")

    connection = sqlite3.connect("manufacturing.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM messages WHERE id = ?",
        (message_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/admin")


# =========================
# ADMIN LOGOUT
# =========================

@app.route("/admin-logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect("/admin-login")


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    create_database()

    app.run(debug=True)