import logger

log = logger.NullLogger()


class Character:
	
	_DEFAULT_HP = 100
	_DEFAULT_ATK = 20
	_DEFAULT_DEF = 20
	_DEFAULT_NAME = 'name'
	
	def __init__(
			self, 
			hp = _DEFAULT_HP, 
			atk = _DEFAULT_ATK, 
			def_ = _DEFAULT_DEF,
			name = _DEFAULT_NAME):
		self._hp = hp
		self._atk = atk
		self._def = def_
		self._name = name
		
	@property
	def hp(self):
		return self._hp
		
	@property
	def name(self):
		return self._name
		
	def is_dead(self):
		return self.hp <= 0
		
	def attack(self, target):
		point = target.damage(self._atk)
		return point
		
	def damage(self, atk):
		point = max(int(atk - self._def/2), 0)
		self._hp = max(self._hp - point, 0)
		return point
		
	def select_target(self, targets):
		if len(targets) == 0:
			return None
		return list(targets)[0]
		

class Action:
	
	def __init__(self, actor, target):
		self._actor = actor
		self._target = target
		
	def exec(self):
		actor = self._actor
		target = self._target
		
		if actor.is_dead():
			return
			
		log.add(f'{actor.name}の攻撃！')
		point = actor.attack(target)
		log.add(f' {target.name} に {point} のダメージ！(残りHP: {target.hp})')
		
		if target.is_dead():
			log.add(f'  {target.name} は倒れた。')

class Turn:
	
	def __init__(self, characters):
		self._characters = characters
		self._actions = self._create_actions(characters)
		
	def _create_actions(self, characters):
		actions = []
		for actor in characters:
			targets = set(characters) - {actor}
			target = actor.select_target(targets)
			action = Action(actor, target)
			actions.append(action)
		return actions
		
	def exec(self):
		for a in self._actions:
			a.exec()
		self._update_dead()
		return list(self._characters)
		
	def _update_dead(self):
		self._characters = {c for c in self._characters if not c.is_dead()}
		

class Battle:
	
	def __init__(self, characters):
		assert 0 < len(characters)
		self._characters = characters
		self._turn_num = 0
		
		self._log_appear()
		
	def _log_appear(self):
		log.add('【Battle Start】')
		for c in self._characters:
			log.add(f'{c.name} があらわれた！')
		
	def exec(self):
		self._turn_num = 1
		while(1 < len(self._characters)):
			log.add(f'■ {self._turn_num} ターン')
			turn = Turn(self._characters)
			self._characters = turn.exec()
			self._turn_num += 1
		winner = self._characters[0]
		log.add(f'--{winner.name} の勝ち--')
		
		print(log)
		log.clear()
		
		return winner

