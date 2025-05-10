import os
from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')

if __name__ == '__main__':
    app.run()