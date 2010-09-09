import itertools
from contextlib import contextmanager
from .stub import FunctionStub
from .queue import ForgeQueue
from .instance_mock_object import InstanceMockObject
from .wildcard_mock_object import WildcardMockObject
from .stub_installer import StubInstaller
from .mock_method_manager import MockMethodManager
from .sentinel import Sentinel
from .dtypes import WILDCARD_FUNCTION

class Forge(object):
    def __init__(self):
        super(Forge, self).__init__()
        self.stub_installer = StubInstaller(self)
        self.reset()
        self._id_allocator = itertools.count()
    def get_new_handle_id(self):
        return self._id_allocator.next()
    def is_replaying(self):
        return self._is_replaying
    def is_recording(self):
        return not self.is_replaying()
    def replay(self):
        self._is_replaying = True
    def reset(self):
        self._is_replaying = False
        self.queue = ForgeQueue(self)
        self.methods = MockMethodManager(self)
    @contextmanager
    def verified_replay_context(self):
        self.replay()
        yield
        self.verify()
        self.reset()
    def pop_expected_call(self):
        return self.queue.pop()
    def verify(self):
        self.queue.verify()

    def create_function_stub(self, func):
        return FunctionStub(self, func)
    def create_wildcard_function_stub(self):
        return self.create_function_stub(WILDCARD_FUNCTION)
    def create_method_stub(self, method):
        return FunctionStub(self, method)
    def create_mock(self, mocked_class):
        return InstanceMockObject(self, mocked_class)
    def create_wildcard_mock(self):
        return WildcardMockObject(self)
    def create_sentinel(self, name=None):
        return Sentinel(name)
    def replace_with_stub(self, obj, method_name):
        return self.stub_installer.replace_with_stub(obj, method_name)
    def restore_all_stubs(self):
        self.stub_installer.restore_all_stubs()
    def any_order(self):
        return self.queue.get_unordered_group_context()
