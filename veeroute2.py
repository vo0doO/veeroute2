from lib.data import Wrapper
import lib.config as config



if __name__ == "__main__":
    wrapper = Wrapper(config.read("config.json"))
    wrapper.group()
    wrapper.save()