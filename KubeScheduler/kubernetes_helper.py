import os
import json
from plistlib import InvalidFileException
from typing import List
from xml.dom import InvalidStateErr


def is_valid_file(config_file_path: str = None, necessary_file_type: str = None) -> bool:
    if config_file_path is None:
        raise InvalidFileException('Given parameter is none')

    if not os.path.exists(config_file_path):
        raise FileNotFoundError(
            f'File <{config_file_path}> does not exist in current path <{os.getcwd()}>')

    if not os.path.isfile(config_file_path):
        raise InvalidFileException('Object is not a file!')

    if necessary_file_type is not None and not config_file_path.endswith(necessary_file_type):
        return False

    # is a valid file of the correct file type
    return True


class KubernetesDeployment(object):

    def __init__(self, deployment_file_path: str) -> None:
        self.deployment_name: str = None
        self.deployment_note: str = None
        self.deployment_files: List[str] = []
        self._init_container(deployment_file_path)

        if len(self.deployment_files) == 0:
            raise InvalidStateErr('No files to deploy')

    def _init_container(self, deployment_file_path: str) -> None:
        if is_valid_file(deployment_file_path):
            with open(deployment_file_path) as json_file:
                json_object = json.load(json_file)
                # Only one configuration per json file at the moment
                self.deployment_name = list(json_object.keys())[0]

                inner_structure = json_object[self.deployment_name]

                if 'files' not in inner_structure:
                    raise InvalidFileException(
                        'JSON file must have a files field')

                self.deployment_files = inner_structure['files']

                if 'note' in inner_structure:
                    self.deployment_note = inner_structure['note']

    def start_deployment(self) -> None:
        for file in self.deployment_files:
            self.__create_new_pod(file)
            
    def get_deployment_files(self) -> List[str]:
        return self.deployment_files

    def __create_new_pod(self, deployment_file_name: str = None) -> bytes:

        if deployment_file_name is None or len(deployment_file_name) == 0:
            raise InvalidFileException('Invalid deployment file in parameter')

        kubernetes_cmd: str = 'kubectl apply -f '

        kubernetes_file = os.popen(
            f'{kubernetes_cmd}{deployment_file_name}').read()
        command = str.encode(kubernetes_file)
        return command


if __name__ == '__main__':
    deployment_path = './deployment_resources/draft_deployment.json'
    dc = KubernetesDeployment(deployment_path)
    dc.start_deployment()
    # print(dc.get_deployment_files())

    print('done')
