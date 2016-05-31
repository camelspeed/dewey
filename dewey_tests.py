import os
import dewey
import unittest
import tempfile

class DeweyTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, dewey.app.config['DATABASE'] = tempfile.mkstemp()
        dewey.app.config['TESTING'] = True
        self.app = dewey.app.test_client()
        dewey.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(dewey.app.config['DATABASE'])

    def test_no_books(self):
        rv = self.app.get('/')
        assert 'Reading is FUNdamental' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
                username=username,
                password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You have been logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_messages(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='Domain Driven Design',
            author='Eric Evans',
            description='A book on how to design',
            isbn='123-123-1112'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert 'Domain Driven Design' in rv.data
        assert 'Eric Evans' in rv.data

if __name__ == '__main__':
    unittest.main()
