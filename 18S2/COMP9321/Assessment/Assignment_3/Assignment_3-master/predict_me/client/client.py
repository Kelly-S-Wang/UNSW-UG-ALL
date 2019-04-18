import os, glob, re, collections, subprocess, random, csv, json, requests
from flask import Flask, render_template, session, request, redirect, url_for, Response


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
token = None


@app.route('/' , methods=['GET' , 'POST'])
def home():
    return render_template ('index.html')


@app.route('/login' , methods=['GET' , 'POST'])
def login():
    global token
    if request.method == 'POST':
        username = request.form['usrName']
        password = request.form['password']
        url = "http://0.0.0.0:12345/token"
        payload = {'username': username, 'password': password}

        try:
            resp = requests.get(url, params=payload)
        except requests.exceptions.ConnectionError:
            return Response("<script> window.alert('No connection between the server!') </script>")

        if resp.ok:
            token = resp.json()['token']

            return redirect(url_for('search'))
        else:
            return render_template ('login.html', displayAlert=True)
    else:
        return render_template ('login.html', displayAlert=False)


@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        # >>>>> debug
        print(username, password, confirmPassword)
        # <<<<< debug

        if password != confirmPassword:
            return render_template ('register.html', samePassword=False, userExist=False)

        try:
            resp = requests.post('http://0.0.0.0:12345/register', json={'username': username, 'password': password})
        except requests.exceptions.ConnectionError:
            return Response("<script> window.alert('No connection between the server!') </script>")

        # >>>>> debug
        print(resp)
        # <<<<< debug

        if resp.status_code == 201:
            return redirect(url_for('login'))
        elif resp.status_code == 200:
            return render_template ('register.html', samePassword=True, userExist=True)
        else:
            return redirect(url_for('register'))
    else:
        return render_template ('register.html', samePassword=True, userExist=False)


@app.route('/search', methods=['GET','POST'])
def search():
    global token
    if request.method == "POST":
        suburb_name = request.form['suburb']

        try:
            size = int(request.form['size'])
        except ValueError:
            return render_template('search.html')


        if suburb_name in ['Brunswick', 'Fitzroy North', 'Port Melbourne', 'Reservoir', 'Richmond'] and 0 < size <= 250:
            url = 'http://0.0.0.0:12345/predict/' + str(suburb_name) + '/' + str(size)
            headers = {'AUTH-TOKEN': token}

            try:
                resp = requests.get(url, headers=headers)
            except requests.exceptions.ConnectionError:
                return Response("<script> window.alert('No connection between the server!') </script>")

            # >>>>>>> debug
            print(resp)
            # <<<<<<< debug

            if resp.ok:
                json_data = resp.json()
                predicted_price = json_data['predicted_price']
                b64PicString = json_data['b64PicString']

                return render_template('result.html', suburb=suburb_name, price=predicted_price, b64PicString=b64PicString)
            else:
                return render_template('search.html')
        else:
            return render_template ('search.html')
    return render_template('search.html')


@app.route('/logout', methods=['GET'])
def logout():
    global token
    if token is not None:
        headers = {'AUTH-TOKEN': token}
        url = 'http://0.0.0.0:12345/signout/' + token
        try:
            resp = requests.delete(url, headers=headers)
        except requests.exceptions.ConnectionError:
            return Response("<script> window.alert('No connection between the server!') </script>")

    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug =True)






    