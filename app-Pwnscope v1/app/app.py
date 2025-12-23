from flask import Flask, render_template, request, session
import subprocess, sys, os

app = Flask(__name__)
app.secret_key = os.urandom(64)

tests =[
    (1, 1), (2, 4), (3, 9), (4, 16), (5, 25)
]

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    error = ""
    if request.method == "POST":
        user_code = request.form["code"]
        try:
            flag = True
            for test in tests:
                test_input, test_output = map(str, test)
                proc = subprocess.run(
                    [sys.executable, "safe_execute.py", user_code, test_input],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                output = proc.stdout.strip('\n')
                if output != test_output:
                    output = f'you failed the test! we expected {test_output = }.'
                    flag = False
            else:
                if flag:
                    output = "all tests passed!"

        except subprocess.TimeoutExpired:
                error = "uh oh.. too slow :/"

        except Exception as e:
                error = "darn, something went wrong!"

    return render_template("index.html", output=output, error=error)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
