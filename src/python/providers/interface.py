from typing import Dict, Union, cast

from constants import ProcessId
from defs import *
from providers import global_kernel_handle


def make_indent(indent: int) -> str:
    result = []
    for i in range(0, indent):
        result.append('\t')
    return ''.join(result)


class InterfaceMeta(Dict[str, 'InterfaceMeta']):
    def __init__(self) -> None:
        sub_interfaces = self.instantiate()
        self._interfaces = Object.keys(sub_interfaces)
        self._interface_help = {}  # type: Dict[str, str]
        for sub in Object.keys(sub_interfaces):
            if _.isString(sub_interfaces[sub]):
                self._interface_help[sub] = cast(str, sub_interfaces[sub])
            else:
                self[sub] = cast(InterfaceMeta, sub_interfaces[sub])

    def instantiate(self) -> Dict[str, Union[str, 'InterfaceMeta']]:
        return {}

    def short_help(self) -> str:
        return "interface meta"

    def help(self) -> str:
        result = ["--- {} ---".format(self.short_help())]
        for sub in self._interfaces:
            if sub in self._interface_help:
                func = True
                value_help = self._interface_help[sub]
            else:
                func = False
                value_help = self[sub].short_help()
            result.append("\t{}{}: {}".format(sub, '()' if func else '', value_help))
        return "\n".join(result)

    def toString(self) -> str:
        return self.help()


class RootInterface(InterfaceMeta):
    def instantiate(self) -> Dict[str, Union[str, InterfaceMeta]]:
        return {
            'kernel': Kernel(),
        }

    def short_help(self) -> str:
        return "dxnr top-level interface"


class Kernel(InterfaceMeta):
    def instantiate(self) -> Dict[str, Union[str, InterfaceMeta]]:
        return {
            'process_table': "shows running processes"
        }

    def short_help(self) -> str:
        return "kernel related functions"

    def process_table(self) -> str:
        kernel = global_kernel_handle.get_kernel()
        if not kernel:
            return "no kernel"

        root_pids = []
        for pid in kernel.get_all_process_ids():
            if kernel.get_parent_of(pid) is None:
                root_pids.append(pid)

        result = []

        def walk_tree(pid: ProcessId, indent: int) -> None:
            children = kernel.get_children_of(pid)

            name = kernel.get_instance(pid).__class__.__name__
            indent_str = make_indent(indent)
            if indent > 0:
                if len(children) > 0:
                    result.append("{}- {}: {}:".format(indent_str, pid, name))
                else:
                    result.append("{}- {}: {}".format(indent_str, pid, name))
            else:
                if len(children) > 0:
                    result.append("{}{}: {}".format(indent_str, pid, name))
                else:
                    result.append("{}{}: {}:".format(indent_str, pid, name))

            for child in children:
                walk_tree(child, indent + 1)

        for pid in root_pids:
            walk_tree(pid, 0)

        return '\n'.join(result)
