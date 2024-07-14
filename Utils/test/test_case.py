'''
test case for BF,GBF and SSPE 
'''
small_database = ['dog', 'cat', 'giraffe', 'fly', 'mosquito', 'horse', 'eagle',
                  'bird', 'bison', 'boar', 'butterfly', 'ant', 'anaconda', 'bear',
                  'chicken', 'dolphin', 'donkey', 'crow', 'crocodile']

middle_database = ['dog', 'racemosely', 'wrongdoers', 'hi', 'delta-ray', 'archchanter', 'labelings', 'whittler',
                   'sorts', 'quadrillion', 'deceast', 'astrogony', 'Purcell', 'alums', 'LoginModule', 'beltmaker',
                   'congenic', 'imparlance', 'tougher', 'shticks', 'unaidedly', 'rooflike', 'self-pollinated',
                   'dualists', 'shalloon', 'overbearingly', 'tabernacled', 'wumpuses', 'cypres',
                   'Mesoamericanist', 'lesbian', 'grokking', 'whippier', 'infractions', 'Selena', 'rheumatic',
                   'double-whammy', 'accordionist', 'boyology', 'stablemate', 'squabbish', 'whopped', 'esbat',
                   'aweather', 'unpremeditate', 'audiovisual', 'bibliomancy', 'ghettoes', 'intergeneration',
                   'gnatty', 'eucharistic', 'recatch', 'bellarmine', 'major', 'aboding', 'walk-on', 'brushlike',
                   'maiden-tongued', 'viewfinder', 'Marquis', 'unimbodied', 'yekkes', 'multifunction', 'tokenising',
                   'paragraf', 'infestivity', 'rollerskating', 'remission', 'Ponchielli', 'harshly', 'tuchus',
                   'cylindroid', 'thicketed', 'scholarly', 'finnier', 'Saint-Louis', 'stipend', 'shopfront',
                   'undershirt', 'groupies', 'offloaded', 'degerms', 'advertising', 'uninclosed', 'untenured',
                   'oriental', 'punishees', 'druggery', 'channelize', 'homeomorphic', 'selkie', 'announced',
                   'lynton', 'riding-school', 'linecut', 'grimiest', 'plenteous', 'bivouacking', 'moham',
                   'unteachability', 'frumpy', 'trussing-bed', 'melilotus', 'dejunk', 'rumpled', 'briberies',
                   'non-smokers', 'raetam', 'slant-eyed', 'fleeing', 'mesquit', 'deradicalising', 'unimposing',
                   'noggins', 'perfectation', 'prognosis', 'Mervyn', 'integrity', 'ketoglutarate', 'igneous',
                   'Molossian', 'repositor', 'avauntour', 'triad', 'Daly City', 'resorptions', 'Canada Dry',
                   'frizzies', 'desmotomy', 'forbade', 'fan-work', 'tracheotomy', 'upgushed', 'Hellenic',
                   'perverseness', 'throwed', 'sheathes', 'undecomposed', 'asswages', 'wasteful', 'count-cardinal',
                   'synchronicities', 'catapults', 'chateaubriand', 'Schoolman', 'dismaying', 'bigamously',
                   'uncleaned', 'trophical', 'agreeableness', 'nut-brown', 'tressing', 'prescanned', 'roustabouts',
                   'acceptable', 'untrouble', 'bestride', 'smartens', 'Carducci', 'reinfected', 'Titaness',
                   'unclasped', 'pre-incarnate', 'machinery', 'Kirovohrad', 'caplet', 'counsellors', 'waische',
                   'Turnus', 'Gounod', 'enlightener', 'Joan of Arc', 'ungarnished', 'putry', 'literary', 'ushering',
                   'lesche', 'yclept', 'albatross', 'defrostable', 'axiliary', 'weaponised', 'dimmed',
                   'multigravida', 'maid-servant', 'dowral', 'knackered', 'over-crowding', 'unordained', 'rowboats',
                   'subdues', 'degasification', 'fellow-me-lads', 'dollarization', 'Anglicanisms', 'trifling',
                   'pro-celeb', 'ostensibly', 'smeltery', 'preregistering', 'geoarchaeology', 'excreta', 'Noman',
                   'tally-board', 'abaft', 'tipsters', 'slogardie', 'mark-to-model', 'baksheesh', 'pandemoniac',
                   'disorienting', 'sweetens', 'Firefox', 'brushwork', 'water-cock', 'intonate', 'reasonable',
                   'tingle', 'onsetter', 'Hamburgers', 'geostatistical', 'unsalvageably', 'silk-gown', 'resiant',
                   'transferred', 'surbahar', 'lyophilizing', 'intrapreneur', 'steroidally', 'minors', 'subscript',
                   'field-bed', 'rubbings', 'annexures', 'serpent-worship', 'go-slow', 'Beaverton', 'queefs',
                   'toetoe', 'oxazolones', 'Decius', 'mountains', 'carbon-date', 'clarinet', 'vibraculum',
                   'sparsely', 'Matty', 'concatenative', 'wakeful', 'disemburdening', 'far-about', 'traversant',
                   'recouer', 'collusion', 'scrotal', 'reshape', 'short-witted', 'yessum', 'susurrus', 'numberings',
                   'primarily', 'librariana', 'tracklistings', 'others', 'markspersons', 'ponto', 'Brummie',
                   'dandifying', 'calligrapher', 'valvuloplasty', 'mosque', 'lucriferous', 'uncontrolledly',
                   'unknotted', 'octillion', 'advisories', 'diseasy', 'neurotoxicity', 'rescued', 'subdolous',
                   'jacchus', 'adheres', 'Sarah', 'ruralness', 'follow-up', 'onward', 'Aachen', 'beautyberries',
                   'clemizole', 'tongued', 'vernacular', 'distributed', 'periplasm', 'seaquarium', 'skeine',
                   'nutraceutical', 'Salem', 'belatedness', 'tusks', 'micrify']