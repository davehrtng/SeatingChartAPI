#!/usr/bin/env python

from app import app

app.run(host='0.0.0.0', port=5000, debug=True)

# host value makes it try to bind to all available hosts