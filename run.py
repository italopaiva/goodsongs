"""Application runner helper."""

from goodsongs.factory import create_app

app = create_app('../config/development.py')

app.run(host='0.0.0.0', debug=True)
