from email_validator import validate_email, EmailNotValidError
import logging
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, url_for, request, redirect, flash, session, make_response
import os
from flask_mail import Mail, Message



app = Flask(__name__)






# app.config["config_key"] = config_value
# config는 앱을 이용하는 데 필요한 설정

# session을 사용하기 위해서는 세션 정보 보안을 위해 시크릿키를 설정해야함
app.config["SECRET_KEY"] = "asdf"

# 리다이렉트를 중단하지 않도록 함
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# flask-mail 확장 등록
mail = Mail(app)


# 디버그툴바 익스텐션에 애플리케이션 설정
toolbar = DebugToolbarExtension(app)



# 로그 레벨 설정
app.logger.setLevel(logging.DEBUG)

# 로그 출력
# app.logger.critical("fatal error")
# app.logger.error("error")
# app.logger.warning("warning")
# app.logger.info("info")
# app.logger.debug("debug")

# current_app, g
# ctx = app.app_context()
# ctx.push()

# print(current_app.name)

# g.connection = 'connection'
# print(g.connection)



# @app.route("/<name>", 
#            methods=['GET', 'POST'])
# def index(name):
#   return render_template("index.html", name = name)


# @app.route("/concat/<name>", 
#            methods=['GET'], 
#            endpoint="hello-endpoint")
#             # endpoint를 지정하지 않으면 함수명 default endpoint
# def hello(name):
#   return f"HHH, {name}!!"
# # f-string 문자열 정의

@app.route("/contact")
def contact():
  return render_template("contact.html")


@app.route("/contact/complete", methods=['GET', 'POST'])
def contact_complete():
  if request.method == "POST":
    username = request.form['username']
    email = request.form['email']
    description = request.form['description']
    print(username)
    print(email)
    print(description)

    send_email(
      email,
      "문의 감사합니다.",
      "contact_mail",
      username = username,
      description = description,
    )





    # 입력 체크
    is_valid = True 

    if not username:
      flash("사용자명은 필수입니다")
      is_valid = False

    if not email:
      flash("메일 주소는 필수입니다")
      is_valid = False
    
    try:
      validate_email(email)
    
    except EmailNotValidError:
      flash("메일 주소의 형식으로 입력해 주세요")
      is_valid = False


    if not description:
        flash("문의 내용은 필수입니다")
        is_valid = False


    if not is_valid:
      return redirect(url_for("contact"))    

    # else:
    flash("문의해 주셔서 감사합니다")
    return redirect(url_for("contact_complete"))
    
    
  return render_template("contact_complete.html")



def send_email(to, subject, template, **kwargs):
  msg = Message(subject, recipients=[to])
  msg.body = render_template(template + ".txt", **kwargs)
  msg.html = render_template(template + ".html", **kwargs)
  mail.send(msg)








if __name__ == '__main__':
  app.run(debug=True)
  #디버그 on (서버 재실행 없이 실시간으로 새로고침)