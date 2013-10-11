from unittest import TestCase
import mock

from minion import request


class TestManager(TestCase):
    def setUp(self):
        self.manager = request.Manager()
        self.request = mock.Mock()
        self.response = mock.Mock()

    def test_after_response(self):
        self.manager.request_started(self.request)
        callback = mock.Mock(return_value=None)

        self.manager.after_response(self.request, callback, 1, kw="abc")

        response = self.manager.request_served(self.request, self.response)

        self.assertEqual(response, self.response)
        callback.assert_called_once_with(self.response, 1, kw="abc")

    def test_after_response_can_modify_the_response(self):
        new_response = mock.Mock()

        self.manager.request_started(self.request)
        def set_thing(response):
            return new_response

        self.manager.after_response(self.request, set_thing)

        response = self.manager.request_served(self.request, self.response)

        self.assertEqual(response, new_response)

    def test_after_response_chaining(self):
        self.manager.request_started(self.request)
        def set_thing(response):
            response.thing = 2

        def add_2(response):
            response.thing += 2

        self.manager.after_response(self.request, set_thing)
        self.manager.after_response(self.request, add_2)

        response = self.manager.request_served(self.request, self.response)

        self.assertEqual(response, self.response)
        self.assertEqual(response.thing, 4)
