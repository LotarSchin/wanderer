import yaml


class Config:
    ERR_FILE_NOT_EXIST = "{file} does not exist!"
    ERR_ATTR_ERROR = "Attribute error occurred during the processing of {file}! Message: {error}"
    ERR_KEY_ERROR = "Key error occurred during the processing of {file}! Message: {error}"

    @staticmethod
    def load_config(file):
        with open(file) as cfg:
            try:
                config = yaml.load(cfg, Loader=yaml.FullLoader)
            except FileNotFoundError:
                print(Config.ERR_FILE_NOT_EXIST.format(file=cfg))
            except AttributeError as e:
                print(Config.ERR_ATTR_ERROR.format(file=cfg, error=e))
            except KeyError as e:
                print(Config.ERR_KEY_ERROR.format(file=cfg, error=e))
            finally:
                return config
