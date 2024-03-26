__author__ = "Team 0111"
__version__ = "1"
__email__ = "usavior.info@gmail.com"

from uSavior import app


if __name__ == "__main__":
    app.secret_key = 'save your grades'
    app.config['DEBUG'] = True
    app.config['MAIL_DEBUG'] = True
    app.run(debug=True)
    