# final_nb_test.py
from final_nb.py import *
import unittest


class TestDatabase(unittest.TestCase):

    def test_labs_table(self):
    	conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Company FROM Bars'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Sirene',), result_list)
        self.assertEqual(len(result_list), 1795)
        pass 

    def test_projects_table(self):

    	conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        pass 

    def test_hashtags_table(self):

    	conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        pass 

# class TestTopTenw():

	







 unittest.main()