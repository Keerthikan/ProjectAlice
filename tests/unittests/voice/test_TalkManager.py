import unittest

from core.voice.TalkManager import TalkManager

class TestTalkManager(unittest.TestCase):

	def test_chooseTalk(self):
		talkManager = TalkManager()

		# when short and default version exist
		talkManager.langData = {
			'module': {
				'de': {
					'talk': {
						'short': ['shortString'],
						'default': ['defaultString']
					}
				}
			}
		}
		self.assertEqual(talkManager.chooseTalk('talk', 'module', 'de', 'en', False), 'defaultString')
		self.assertEqual(talkManager.chooseTalk('talk', 'module', 'de', 'en', True), 'shortString')


		# when only default version exists
		talkManager.langData = {
			'module': {
				'de': {
					'talk': {
						'default': ['defaultString']
					}
				}
			}
		}
		self.assertEqual(talkManager.chooseTalk('talk', 'module', 'de', 'en', True), 'defaultString')


		# when list instead of dict is used
		talkManager.langData = {
			'module': {
				'de': {
					'talk': ['defaultString']
				}
			}
		}
		self.assertEqual(talkManager.chooseTalk('talk', 'module', 'de', 'en', True), 'defaultString')


		# when only fallback language exists
		talkManager.langData = {
			'module': {
				'en': {
					'talk': ['defaultString']
				}
			}
		}
		self.assertEqual(talkManager.chooseTalk('talk', 'module', 'de', 'en', True), 'defaultString')


		# when required keys do not exist in active and fallback language
		talkManager.langData = {'module': {'en': {}}}
		self.assertEqual(talkManager.chooseTalk('talk', 'module', 'de', 'en', True), '')

		talkManager.langData = {'module': {'de': {}}}
		self.assertEqual(talkManager.chooseTalk('talk', 'module', 'de', 'en', True), '')

		talkManager.langData = {'module': {}}
		self.assertEqual(talkManager.chooseTalk('talk', 'module', 'de', 'en', True), '')

		talkManager.langData = {}
		self.assertEqual(talkManager.chooseTalk('talk', 'module', 'de', 'en', True), '')


if __name__ == "__main__":
	unittest.main()
