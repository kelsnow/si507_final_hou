# final_nb_test.py
import unittest
from final_nb import *


class TestDatabase(unittest.TestCase):
	def test_labs_table(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()

		sql = 'SELECT PeopleNumber FROM Labs WHERE Id=2'
		results = cur.execute(sql)
		result_list = results.fetchall()
		# self.assertIn(('Sirene',), result_list)
		for i in result_list:
			self.assertEqual(i[0], 62)

		sql = 'SELECT Name FROM Labs WHERE Id=8'
		results = cur.execute(sql)
		result_list = results.fetchall()
		for i in result_list:
			self.assertEqual(i[0], 'design-fiction')
		

	def test_projects_table(self):

		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()


		sql = 'SELECT LabId FROM Projects WHERE Projects.Id=10'
		results = cur.execute(sql)
		result_list = results.fetchall()
		# self.assertIn(('Sirene',), result_list)
		for i in result_list:
			self.assertEqual(i[0], 1)

		sql = 'SELECT Count(LabId) FROM Projects GROUP BY LabId'
		results = cur.execute(sql)
		result_list = results.fetchall()

		self.assertGreater(len(result_list),10)


		

	def test_hashtags_table(self):

		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
		
		sql = 'SELECT Name FROM Hashtags WHERE Id=15'
		results = cur.execute(sql)
		result_list = results.fetchall()
		for i in result_list:
		# self.assertIn(('Sirene',), result_list)
			self.assertEqual(i[0], 'robotics')




unittest.main()