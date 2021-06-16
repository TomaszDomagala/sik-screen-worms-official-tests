import unittest
import configparser
import subprocess
import time

config = configparser.ConfigParser()


class TestServer100(unittest.TestCase):

	def tearDown(self):
		if self.server.poll() is None:
			self.server.kill()
			self.server.communicate()

	def start_server(self, args: str):
		all_args = [config.get("TESTS_100", "SERVER_PATH")] + args.split(" ")

		out = None if config.getboolean("TESTS_100_DEBUG", "PRINT_SERVER_STDOUT") else subprocess.DEVNULL
		err = None if config.getboolean("TESTS_100_DEBUG", "PRINT_SERVER_STDERR") else subprocess.DEVNULL
		self.server = subprocess.Popen(all_args, stdout=out, stderr=err)
		time.sleep(config.getfloat("TEST_100", "EXIT_TIME"))

	def do_test(self, args):
		self.start_server(args)
		exit_code = self.server.poll()
		self.assertIsNot(exit_code, None, "Server didn't exit.")
		self.assertEqual(self.server.poll(), 1, f"return code {exit_code}, expected 1.")

	def test_101(self):
		self.do_test("W")

	def test_102(self):
		self.do_test("WI")

	def test_103(self):
		self.do_test("-wI")


if __name__ == '__main__':
	config.read("test_config.ini")
	unittest.main()
