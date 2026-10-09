from connect import connect_wlan
import gc

if connect_wlan():
    from microdot import Microdot, Request

    app = Microdot()

    @app.route('/')
    def home(request: Request):
        return '<h1>Hello from ESP32!</h1>'

    @app.route('/weather')
    def weather(reqest: Request):
        return {"temperature": 22, "condition": "Sunny", "city": "Novocheboksarsk"}


    gc.collect()

    print('Starting Microdot on port 0.0.0.0:5000...')
    app.run(host='0.0.0.0', port=5000)