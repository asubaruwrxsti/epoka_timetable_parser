from api import api as api

def main():
    try:
        app = api.API()
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()