# from dataclasses import dataclass, field
# from typing import Any, Optional

# from cstest.content.variable import variable_resolve as vr

# resolver_type = vr.ResolveBaseVar | vr.ResolveHashVar | vr.ResolveBracketVar

# RESOLVER_MAP: dict[str, resolver_type] = {
#     "base": vr.ResolveBaseVariable,  # type: ignore
#     "bracket": vr.ResolveBracketVariable,  # type: ignore
#     "hash": vr.ResolveHashVariable,  # type: ignore
#     "bracket_hash": vr.ResolveBracketHashVariable,  # type: ignore
# }


# # from cstest.content.variable.exceptions import VariableStructureInvalid

# # if not self.valid_struct:
# #             raise VariableStructureInvalid(
# #                 f"""Variable: {self.called_name} has an invalid structure and
# #                  can not be resolved."""
# #             )
# #         else:


# @dataclass
# class CalledVariable:
#     called_name: str
#     resolver: resolver_type = field(init=False)
#     valid_struct: bool = field(init=False)
#     valid_name: bool = field(init=False)
#     errors: list[str] = field(default_factory=list)
#     resolved_name: str = field(init=False)
#     value: Any = field(init=False)

#     def identify_resolver(self) -> None:
#         if "[" in self.called_name:
#             if "#" in self.called_name:
#                 self.resolver = RESOLVER_MAP["bracket_hash"]
#             else:
#                 self.resolve = RESOLVER_MAP["bracket"]
#         elif "#" in self.called_name:
#             self.resolve = RESOLVER_MAP["hash"]
#         else:
#             self.resolve = RESOLVER_MAP["base"]

#     def validate_structure(self) -> None:
#         self.valid_struct, errors = self.resolver.validate_struct()
#         self.errors.extend(errors)

#     def resolve_name(self) -> None:
#         errors, self.valid_name, self.name = self.resolve()
#         self.errors.extend(errors)

#     def lookup_value(self) -> None:
#         pass
