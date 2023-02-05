class Logger:
	
	def __init__(self):
		self._logs = []
		
	@property
	def length(self):
		return len(self._logs)
		
	def add(self, log):
		self._logs.append(log)
		
	def clear(self):
		self._logs.clear()
		
	def __str__(self):
		log = ''
		for l in self._logs:
			log += f'{l}\n'
		return log
	
			
class NullLogger(Logger):
	
	def __init__(self):
		pass
		
	@property
	def length(self):
		return 0
		
	def add(self, log):
		pass
		
	def clear(self):
		pass
		
	def __str__(self):
		return ''
		
