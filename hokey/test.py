from grasshopper import GrasshopperEngine as GE
from app import Hokey

if __name__ == '__main__':
        app=Hokey(__name__)
        engine=GE()
        engine.install(app)
        engine.run()