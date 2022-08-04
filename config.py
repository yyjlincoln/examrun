import os
import typing as t
import json


class ConfigDoesNotExistError(Exception):
    'Config file can not be found.'


class InvalidConfig(Exception):
    'Invalid Config.'


class ExamConfig(t.TypedDict):
    deadline: str
    title: str
    questions: t.Dict[str, str]


def get_config_location() -> ExamConfig:
    return os.path.join(os.getcwd(), "config.json")


def check_config_type(cfg: t.Any) -> bool:
    if type(cfg) != dict:
        return False
    try:
        assert 'deadline' in cfg
        assert type(cfg['deadline']) == int
        assert 'title' in cfg
        assert type(cfg['title']) == str
        assert 'questions' in cfg
        assert type(cfg['questions']) == dict
        for k, v in cfg['questions'].items():
            assert type(k) == str
            assert type(v) == str
    except AssertionError:
        return False
    return True


def parse_files_from_give_command(give_command: str):
    if not give_command.startswith('give '):
        raise ValueError("Not a give command.")
    cmd_split = give_command.split(' ')
    if len(cmd_split) < 4:
        raise ValueError("Invalid give command: Expecting at least 4 args.")
    files = cmd_split[3:]
    return files


def parse_files_from_config(cfg: ExamConfig) -> t.Dict[str, t.List[str]]:
    'Returns a map: question_name -> fileNames[]'
    questions = cfg['questions']
    result: t.Dict[str, t.List[str]] = {}
    for question_name, give_command in questions.items():
        result[question_name] = parse_files_from_give_command(give_command)
    return result


def read_config() -> ExamConfig:
    if not os.path.exists(get_config_location()):
        raise ConfigDoesNotExistError()

    with open(get_config_location()) as f:
        config = f.read()
        cfg = json.loads(config)
        if not check_config_type(cfg):
            raise InvalidConfig()
        return cfg
