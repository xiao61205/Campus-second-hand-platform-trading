from flask import Flask, render_template, request, jsonify
from flask import redirect, url_for
from models import init_db, db, User, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 初始化数据库
with app.app_context():
    init_db()

# 路由：主页面
@app.route('/')
def main_page():
    # 模拟推荐商品信息（可以从数据库中动态获取）
    products = [
        {"image": "1d8f9072bae04a06ae102d86d383dc7e.jpeg", "category": "Teaching materials and teaching aids"},
        {"image": "R-C.jfif", "category": "Electronics"},
        {"image": "KGlknWS1k3.jpg", "category": "Household items"},
    ]
    return render_template('主页面.html', products=products)

# 路由：登录页面
@app.route('/login')
def login_page():
    return render_template('index.html')

# 登录逻辑
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    passcode = request.form['passcode']

    # 登录验证逻辑
    if username and passcode:  # 这里是简单的验证，实际应该是数据库验证
        return redirect(url_for('index'))  # 登录成功后跳转到主页
    else:
        return "Invalid credentials, please try again."

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    username = request.form['username']
    passcode = request.form['passcode']
    email = request.form['email']
    phone = request.form['phone']

    # 注册验证逻辑
    if username and passcode and email and phone:  # 同样是简单验证
        return redirect(url_for('index'))  # 注册成功后跳转到主页
    else:
        return "All fields must be filled out."

@app.route('/')
def index():
    return render_template('index.html')

# 路由：个人中心页面
@app.route('/personal_center')
def personal_center():
    return render_template('个人中心(1).html')

# 更新个人信息
@app.route('/update_profile', methods=['POST'])
def update_profile():
    nickname = request.form.get('nickname')
    bio = request.form.get('bio')
    # 假设当前用户ID为1
    user = User.query.get(1)
    user.nickname = nickname
    user.bio = bio
    db.session.commit()
    return jsonify({"message": "Personal information has been updated"})

# 发布商品
@app.route('/publish_product', methods=['POST'])
def publish_product():
    product_name = request.form.get('productName')
    product_desc = request.form.get('productDesc')
    product_price = request.form.get('productPrice')
    new_product = Product(name=product_name, description=product_desc, price=product_price, user_id=1)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product released"})

# 路由：帮助中心
@app.route('/help_center')
def help_center():
    return render_template('帮助中心.html')

# 路由：评论与反馈
@app.route('/feedback')
def feedback_page():
    return render_template('评论与反馈.html')

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    feedback_data = request.form.get('feedback')
    print("Receive feedback:", feedback_data)  # 在实际应用中，将其存储到数据库
    return jsonify({"message": "Feedback submitted successfully", "status": "success"})

@app.route('/review', methods=['POST'])
def submit_review():
    review_data = {
        "service": request.form.get('service'),
        "quality": request.form.get('quality'),
        "speed": request.form.get('speed'),
        "comment": request.form.get('comment')
    }
    print("Receive a comment:", review_data)  # 在实际应用中，将其存储到数据库
    return jsonify({"message": "Comment submitted successfully", "status": "success"})

@app.route('/product_management')
def product_management():
    products = [
        {"id": 1, "title": "Commodity 1", "status": "Putaway"},
        {"id": 2, "title": "Commodity 2", "status": "Removal"},
    ]
    return render_template('商品管理.html', products=products)

@app.route('/product/edit', methods=['POST'])
def edit_product():
    product_id = request.json.get('id')
    new_title = request.json.get('title')
    print(f"Editorial goods ID: {product_id}, New name: {new_title}")  # 示例日志
    # 在这里处理数据库更新逻辑
    return jsonify({"message": "Product information has been updated"})

@app.route('/product/delete', methods=['POST'])
def delete_product():
    product_id = request.json.get('id')
    print(f"Delete goods ID: {product_id}")  # 示例日志
    # 在这里处理数据库删除逻辑
    return jsonify({"message": "Item deleted"})

@app.route('/product/toggle_status', methods=['POST'])
def toggle_product_status():
    product_id = request.json.get('id')
    current_status = request.json.get('status')
    new_status = "Putaway" if current_status == "Removal" else "Removal"
    print(f"Switch goods ID: {product_id}, New state: {new_status}")  # 示例日志
    # 在这里处理数据库更新逻辑
    return jsonify({"message": "Item status had been switched", "new_status": new_status})


@app.route('/product/edit/<int:product_id>')
def edit_product_page(product_id):
    # 示例商品信息（可以从数据库中获取）
    product = {
        "id": product_id,
        "title": f"Commodity {product_id}",
        "description": "This is a sample product description.",
        "price": 100.0
    }
    return render_template('商品编辑.html', product=product)


# 路由：更新商品信息
@app.route('/product/update', methods=['POST'])
def update_product():
    product_id = request.form.get('id')
    new_title = request.form.get('title')
    new_description = request.form.get('description')
    new_price = request.form.get('price')
    print(f"Renewal of goods ID: {product_id}, New name: {new_title}, New description: {new_description}, New price: {new_price}")
    # 示例：此处应更新数据库中的商品信息

    return redirect(url_for('product_management'))

@app.route('/product_browsing')
def product_browsing():
    products = [
        {"id": 1, "title": "Product 1", "price": "$19", "image": "8edd33b3a18eadc00e963eb01c66dfc3.jpg"},
        {"id": 2, "title": "Product 2", "price": "$22", "image": "64411636-60e2-4959-8d03-08ead7eddff9.jpg"},
        {"id": 3, "title": "Product 3", "price": "$799", "image": "d5cc755d7759b7abc226088e2ad5c4c9.png"},
        {"id": 4, "title": "Product 4", "price": "$599", "image": "depositphotos_464980234-stock-photo-single-white-bluetooth-wireless-headphones.jpg"},
    ]
    return render_template('商品浏览.html', products=products)

# 商品详情页面
@app.route('/product_detail/<int:product_id>')
def product_detail(product_id):
    products = {
        4: {"title": "High-Quality Headphones", "description": "These headphones provide clear sound quality.", "price": "¥ 599", "condition": "90% New", "image": "depositphotos_464980234-stock-photo-single-white-bluetooth-wireless-headphones.jpg"},
        2: {"title": "Product 2", "description": "This is product 2 description.", "price": "¥ 22", "condition": "80% New", "image": "64411636-60e2-4959-8d03-08ead7eddff9.jpg"},
        3: {"title": "Product 3", "description": "This is product 3 description.", "price": "¥ 799", "condition": "100% New", "image": "d5cc755d7759b7abc226088e2ad5c4c9.png"},
        1: {"title": "Product 4", "description": "This is product 4 description.", "price": "¥ 19", "condition": "70% New", "image": "8edd33b3a18eadc00e963eb01c66dfc3.jpg"},
    }
    product = products.get(product_id, {})
    return render_template('商品详情.html', product=product)




if __name__ == '__main__':
    app.run(debug=True)
