from App import create_app
import os
app = create_app()

if __name__ == '__main__':
    current_path = os.getcwd()
    print("当前路径是:", current_path)
    app.run(debug=True)
