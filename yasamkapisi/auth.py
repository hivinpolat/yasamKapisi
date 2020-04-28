import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

#Mail gönderme modülleri
import smtplib #mail gönderme servisi
from email.mime.text import MIMEText # mesaj içeriği üretmek için kullanılır.
from email.mime.multipart import MIMEMultipart
from datetime import datetime

#İhtiyacımız olan model çağrıldı.
from yasamkapisi.models import User

#Mail bilgileri
email = "ktuyapayzekaklubu@gmail.com"
parola = "yasamkapisi123"

bp = Blueprint('auth', __name__, url_prefix='/auth')
""""""""""""""""""
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname=request.form['surname']
        phone = request.form['phone']
        mail=request.form['mail']
        workspace=request.form['workspace']
        gender=request.form['gender']
        birthday=request.form['birthday']
        tc=request.form['tc']
        username=request.form['username']
        password=request.form['password']
        repeatpassword=request.form['repeatpassword']
        
        error = None

        if password != repeatpassword:
            error = "Şifre eşleşmiyor. Tekrar deneyin..."
        elif not User.objects(username=username).first() == None:
            error = "Bu kullanıcı adı bulunmaktadır. Tekrar deneyin..."
        elif not User.objects(mail=mail).first() == None:
            error = "Bu mail adresine ait kayıtlı kullanıcı bulunmaktadır. Tekrar deneyin..."
        else:#Mongodb'ye kullanıcı kaydı yapılıyor.
            user = User(
                name = name,
                surname = surname,
                phone = phone,
                mail = mail,
                workspace = workspace,
                gender = gender,
                birthday = birthday,
                tc = tc,
                username = username,
                password = generate_password_hash(password),
            ).save()
        
            session.clear()
            flash("Kayıt başarılı","success")
            return redirect(url_for('auth.login'))

        flash(error,"danger")
    return render_template('auth/register.html')
""""""""""""""""""""""""""""""""""""

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password=request.form['password']
        
        error = None
        user = User.objects(username=username).first()

        if user is None:
            error = 'Böyle bir kullanıcı bulunmamaktadır. Lütfen tekrar deneyin...'
        elif not check_password_hash(user.password, password):
            error = 'Şifre hatalı. Lütfen tekrar deneyin...'

        if error is None:
           session.clear()
           session["logged_in"] = True
           session['username'] = username
           return session['username']

        flash(error,"danger")
    return render_template('auth/login.html')
"""
@bp.route('/index', methods=('GET', 'POST'))
def index():
   

       


    return render_template('auth/index.html')"""
""""""""""""

@bp.route('/forgot', methods=('GET', 'POST'))
def forgot():
    if request.method == 'POST':
        username = request.form['username']

        error = None
        user = User.objects(username=username).first()

        if user is None:
            error = 'Böyle bir kullanıcı bulunmamaktadır. Lütfen tekrar deneyin...'
            flash(error,"danger")
            return redirect(url_for('auth.forgot'))
        else:
            try:
                tarih = datetime.now()
                mesajIcergi = """
                        Merhaba {username};
                        Şifrenizi {tarih} tarihinde mailinize gönderilmesini talep etmişsiniz.

                        Şifreniz : {sifre}
                """
                organizeMesage = mesajIcergi.format(username=username,tarih=tarih.strftime("%d/%m/%Y - %H:%M:%S"),sifre=user.password)
                #mesaj içeriği oluşturma
                mesaj = MIMEMultipart()
                mesaj["Subject"] = "Şifre Gönderimi"
                mesaj["From"] = email
                mesaj["To"] = user.mail
                mesaj.attach(MIMEText(organizeMesage,"plain"))
                
                #mail gönderme işlemleri
                mailServisi = smtplib.SMTP("smtp.gmail.com",587)
                mailServisi.ehlo()
                mailServisi.starttls()
                mailServisi.login(email,parola)
                mailServisi.sendmail(email,user.mail,mesaj.as_string())
                mailServisi.quit()
                flash("Mailiniz başarıyla gönderildi...","success")
                return redirect(url_for("auth.login"))
            except:
                flash("Mail gönderilirken bir hata oluştu...","danger")
                return redirect(url_for("auth.forgot"))

    return render_template('auth/forgot.html')
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login')) 

#session kontrolünü yapan fonksiyon
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapın...","danger")
            return redirect(url_for("auth.login"))
    return decorated_function