#encoding:utf-8
from flask import Flask,render_template,url_for,request,session,redirect
import flask
import base64
import config
from exts import db
from forms import UploadForm,UserForm
from models import UserModel,AdvertisementModel,NewsModel
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)





# @app.route('/')
# def hello_world():
#     return 'Hello World!'


@app.route('/upload11',methods=['POST','GET'])
def upload_file11():
    return render_template('upload.html')


@app.route('/upload/')
def upload_file():
    # # ...
    # # if request.method == 'POST':
    # #     file11 = request.form.get('file')
    # #     #file11.save(os.path.join(UPLOAD_FOLDER, file11.filename))
    # #     file11.save(UPLOAD_FOLDER,file11.filename)
    # #     return sucess
    # # f = request.files['file'] #获取form表单传过来的文件
    # #
    # # basepath = os.path.dirname(__file__) #获得当前文件路径，并且赋值给basepath
    # #
    # # upload_path = os.path.join(basepath, 'static/upload', secure_filename(f.filename)) #获得上传文件所在的全部路径和文件名称
    # #
    # # f.save(upload_path) #保存
    # #
    # # return sucess
    # ds = AdvertisementModel.query.all()
    # form = UploadForm()
    # return render_template('upload.html', form=form, ds=ds, base64=base64)
    pass


@app.route('/')
def index():
    advertisements=AdvertisementModel.query.order_by('-id')
    advertisement=advertisements.limit(2)
    news=NewsModel.query.order_by('-id')
    news_five=news.limit(5)
    # print advertisements
    a=1
    context={'advertisements':advertisement,'base64':base64,'a':a,'news':news_five}
    return render_template('index.html',**context)


@app.route('/admin/login/',methods=['GET','POST'])
def admin_login():
    form=UserForm()
    if request.method == 'POST' and form.validate():
        name=request.form.get('username')
        word=request.form.get('password')
        user=UserModel.query.filter(UserModel.username == name, UserModel.password == word).first()
        if user:
            session['user_id']=user.id
            print user.id
            session.permanent=True
            return redirect(url_for('admin'))
        else:
            return u'用户名或密码错误！'
    else:
        return render_template('login.html')


@app.route('/admin/logout/')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))


@app.route('/admin/')
def admin():
    if session.get('user_id'):
        user1=UserModel.query.filter(UserModel.id == session.get('user_id')).first()
        context={'user':user1}
        return render_template('admin_index.html',**context)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/news/')
def admin_news():
    if session.get('user_id'):
        page=request.args.get('page',1,type=int)

        news_all=NewsModel.query.order_by('-id')
        pagination=news_all.paginate(page,per_page=1,error_out=False)
        news=pagination.items
        context={'news_all':news,'pagination':pagination}
        return render_template('admin_news.html',**context)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/news/delete/<id>/')
def delete_news(id):
    if session.get('user_id'):
        news_delete=NewsModel.query.filter(NewsModel.id == id).first()
        db.session.delete(news_delete)
        db.session.commit()
        return redirect(url_for('admin_news'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/advertisement/')
def admin_advertisement():
    if session.get('user_id'):
        return render_template('advertisement.html')
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/advertisement/upload',methods=['GET','POST'])
def admin_adverupload():
    if session.get('user_id'):
        form=UploadForm()
        if request.method=='POST' and form.validate():
            file=request.files['file'].read()
            file_name=flask.request.form.get('title')
            advertisment_file = AdvertisementModel(picture_name=file_name,picture=file)
            db.session.add(advertisment_file)
            db.session.commit()
            return u'发布成功！'
        else:
            return render_template(url_for(admin_advertisement))
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin/news_insert', methods=['POST','GET'])
def admin_newsinsert():
    if session.get('user_id'):
        # form=NewsForm()
        if request.method == 'POST':
        #     if form.validate():
        #         file=request.files['file'].read()
        #         news_file=NewsModel(image=file)
        #         db.session.add(news_file)
        #         db.session.commit()
            file=request.files['file'].read()
            # news_file=NewsModel(image=file)
            title=request.form.get('title')
            content=request.form.get('content')
            news=NewsModel(title=title,image=file,content=content)
            db.session.add(news)
            db.session.commit()
            return u'发布新闻成功!'
        else:
            return render_template('news_insert.html')
    else:
        return redirect(url_for('admin_login'))


@app.route('/news/')
def news():
    news_all=NewsModel.query.order_by('-id')
    head_news=news_all.first()
    page=request.args.get('page',1,type=int)
    pagination=news_all.paginate(page,per_page=4,error_out=False)
    news=pagination.items
    a=2
    context={'news_all':news,'pagination':pagination,'head_news':head_news,'base64':base64,'a':a}

    return render_template('news.html',**context)


@app.route('/news/detail/<id>/')
def news_detail(id):
    detail=NewsModel.query.filter(NewsModel.id == id).first()
    context={'detail':detail,'base64':base64}
    return render_template('news_detail.html',**context)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),500


if __name__ == '__main__':
    app.run(host='0.0.0.0')
