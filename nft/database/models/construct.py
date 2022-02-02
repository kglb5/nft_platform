def import_models():
    import os
    all_models = open('all_models.py', 'w')
    imports = 'from run import db \n'
    for module in os.listdir(os.path.dirname(__file__)):
        if str(module) == '__init__.py' or module == '__pycache__' or module == 'base.py':
            pass
        else:
            imports += 'from nft.database.models.{0} import * \n'.format(module.split('.')[0])

    imports += 'db.create_all()'
    all_models.write(imports)

import_models()

from nft.database.models.all_models import *

