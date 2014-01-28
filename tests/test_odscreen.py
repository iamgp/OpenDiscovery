from OpenDiscovery.screen import ScreenTests as screenTest

def tests():
	t = screenTest('test')
	assert t.checkSetup() == 'test'