from OpenDiscovery.screen import ScreenTests as screenTest




def testss():
	t = screenTest('test')
	assert t.checkSetup() == 'test'