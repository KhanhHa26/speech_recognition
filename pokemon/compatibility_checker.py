"""
This file is used to check your pokemon.py code for compatibility with our
OFFICIAL POKEMON TOURNAMENT STANDARD™.

If your pokemon.py code fails validation by this module,
it cannot be used in our tournament/driver and will be rejected.

"""

import sys
import copy
import inspect
from types import ModuleType
from typing import Union, Callable, List, get_origin, get_args
from collections.abc import Callable as CallableType
from io import StringIO
from unittest.mock import Mock
from contextlib import contextmanager


def check_module(module):
    """
    Checks the given module for compatibility with our
    OFFICIAL POKEMON TOURNAMENT STANDARD™

    Specifically:
        - The module must contain the classes Pokemon, Player, and Move.
        - The module must contain the variables INVALID_MOVE and INVALID_POKEMON.
        - INVALID_MOVE must be a valid instance of the Move class.
        - INVALID_POKEMON must be a valid instance of the Pokemon class.
    
    """

    assert isinstance(module, ModuleType)

    moduleName = module.__name__.rsplit('.', 1)[-1]
    assert moduleName in ('pokemon', 'pokemon_team')

    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    attrs = set(dir(module))

    if moduleName == 'pokemon':
        expectedClassNames = [
            'Pokemon',
            'Player',
            'Move',
        ]

        expectedVarNames = [
            'INVALID_MOVE',
            'INVALID_POKEMON',
        ]

        for className in expectedClassNames:
            check(
                className in attrs,
                f"{moduleName}.py file must contain a '{className}' class!",
            )

        for varName in expectedVarNames:
            check(
                varName in attrs,
                f"{moduleName}.py file must contain a '{varName}' variable!",
            )

        if _spew_errors(errors):
            return False

        Move = module.Move
        Pokemon = module.Pokemon

        expectedTypeForVarName = {
            'Player': type,
            'Pokemon': type,
            'Move': type,
            'INVALID_MOVE': Move,
            'INVALID_POKEMON': Pokemon,
        }

        for varName, ExpectedType in expectedTypeForVarName.items():
            var = getattr(module, varName)
            check(
                isinstance(var, ExpectedType),
                f"'{varName}' must be a {_type_str(ExpectedType)}! "
                f"(Your version was found to be a "
                f"{_type_str(type(var), value=var)})",
            )

    elif moduleName == 'pokemon_team':
        check(
            'create_team' in attrs,
            "team.py file must contain a 'create_team()' function!",
        )

        if _spew_errors(errors):
            return False

        Pokemon = module.Pokemon
        create_team = module.create_team

        check(
            isinstance(create_team, Callable),
            "'create_team()' must be a function that takes nothing "
            "and returns a list of Pokemon! "
            f"(Your version was found to be a {_type_str(create_team)})",
        )

        parameters = inspect.signature(create_team).parameters

        check(
            len(parameters) == 0,
            "'create_team()' should take no arguments! "
            f"(Your version takes {len(parameters)} arguments)",
        )

        if _spew_errors(errors):
            return False

        try:
            returnVal = create_team()
        except Exception as e:
            check(
                False,
                f"Encountered error while calling create_team(): {e}",
            )
        else:
            check(
                isinstance(returnVal, list)
                    and all(isinstance(item, Pokemon) for item in returnVal),
                "'create_team()' must be a function that takes nothing and "
                "returns a list of Pokemon! "
                "(Your version returned "
                f"{_type_str(type(returnVal), value=returnVal)})",
            )

    return not _spew_errors(errors)
    

def check_class(cls):
    """
    Checks the given class for compatibility with our
    OFFICIAL POKEMON TOURNAMENT STANDARD™

    Specifically:

    - Player
        - The Player class must have the following attributes:
            - .name             (str)
            - .pokemon_party    (list of Pokemon objects)
            - .current_pokemon  (Pokemon)
    
        - The Player class must have the following methods:
            - .__init__(str, [list of Pokemon objects])
            - .list_pokemon()
            - .switch(str) -> bool
            - .get_pokemon(str) -> Pokemon
            - .heal()
            - .team_is_alive() -> bool
            - .print_moves()
            - .attack(str, Pokemon)

    - Pokemon
        - The Pokemon class must have the following attributes:
            - .hp       (int)
            - .max_hp   (int)
            - .name     (str)
            - .moves    (list of Move objects)
            - .type     (str)
            - .speed    (int)
    
        - The Pokemon class must have the following methods:
            - .__init__(str, int, [list of Move objects], str, int)
            - .is_alive() -> bool
            - .print_moves()
            - .get_move(str) -> Move
            - .attack(str, Pokemon)
            - .take_damage(int/float)
            - .heal()

    - Move
        - The Move class must have the following attributes:
            - .name     (str)
            - .power    (int)
            - .type     (str)

        - The Move class must have the following methods:
            - .__init__(str, int, str)
            - .__str__() -> str
            - .get_multiplier_against(Pokemon) -> int/float

    """

    assert isinstance(cls, type)
    assert cls.__name__ in ('Player', 'Pokemon', 'Move')
    assert _suppress_output(lambda: check_module(inspect.getmodule(cls)))

    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    module = inspect.getmodule(cls)

    Player = module.Player
    Pokemon = module.Pokemon
    Move = module.Move

    if _spew_errors(errors):
        return False
    
    expectedTypeForFieldForClass = {
        Player: {
            'name': str,
            'pokemon_party': List[Pokemon],
            'current_pokemon': Pokemon,
            '__init__': Callable[[str, List[Pokemon]], None],
            'list_pokemon': Callable[[], None],
            'switch': Callable[[str], bool],
            'get_pokemon': Callable[[str], Pokemon],
            'heal': Callable[[], None],
            'team_is_alive': Callable[[], bool],
            'print_moves': Callable[[], None],
            'attack': Callable[[str, Pokemon], None],
        },
        Pokemon: {
            'hp': int,
            'max_hp': int,
            'name': str,
            'moves': List[Move],
            'type': str,
            'speed': int,
            '__init__': Callable[[str, int, List[Move], str, int], None],
            'is_alive': Callable[[], bool],
            'print_moves': Callable[[], None],
            'get_move': Callable[[str], Move],
            'attack': Callable[[str, Pokemon], None],
            'take_damage': Callable[[Union[int, float]], None],
            'heal': Callable[[], None],
        },
        Move: {
            'name': str,
            'power': int,
            'type': str,
            '__init__': Callable[[str, int, str], None],
            '__str__': Callable[[], str],
            'get_multiplier_against': Callable[[Pokemon], Union[int, float]],
        },
    }

    mockForType = {}
    
    def get_mock(Type):
        try:
            return mockForType[Type]
        except KeyError:
            typeArgs = get_args(Type)
            OriginType = get_origin(Type)
            
            if OriginType is list:
                assert len(typeArgs) == 1
                innerMock = get_mock(typeArgs[0])
                mock = [
                    innerMock,
                    copy.deepcopy(innerMock),
                    copy.deepcopy(innerMock),
                ]
                
            elif OriginType is Union:
                assert len(typeArgs) > 1
                mock = get_mock(typeArgs[0])
                
            elif Type in (int, float, str, bool):
                mock = Type()
                
            else:
                expectedTypeForField = expectedTypeForFieldForClass.get(Type, {})

                mock = Mock(Type)
                
                # Mock attributes
                kwargs = {
                    fieldName: get_mock(FieldType)
                    for fieldName, FieldType in expectedTypeForField.items()
                        if get_origin(FieldType) is not CallableType
                }
                mock.configure_mock(**kwargs)

                # Mock methods
                kwargs = {
                    f'{fieldName}.return_value': get_mock(get_args(FieldType)[1])
                    for fieldName, FieldType in expectedTypeForField.items()
                        if get_origin(FieldType) is CallableType
                            and fieldName not in ('__init__', '__str__')
                }
                mock.configure_mock(**kwargs)
                
            mockForType[Type] = mock
            
            return mock

    expectedTypeForField = expectedTypeForFieldForClass[cls]

    # Determine if the ctor has the right signature.
    ctorArgTypes, _ = get_args(expectedTypeForField['__init__'])
    actualCtorParams = {
        key: value
        for key, value in inspect.signature(cls.__init__).parameters.items()
            if key != 'self'
    }

    check(
        len(ctorArgTypes) == len(actualCtorParams),
        f"{cls.__name__} class constructor should take "
        f"{len(ctorArgTypes)} arguments! "
        f"(Your version takes {len(actualCtorParams)} arguments)",
    )

    if _spew_errors(errors):
        return False
    
    # Attempt to construct an instance of the given class.
    try:
        testObject = cls(*(get_mock(ArgType) for ArgType in ctorArgTypes))
    except Exception as e:
        check(
            False,
            "Encountered error while creating a "
            f"new {cls.__name__} object: {e}",
        )

    if _spew_errors(errors):
        return False

    def typecheck(value, ExpectedType):
        if ExpectedType is None:
            ExpectedType = type(None)

        typeArgs = get_args(ExpectedType)
        OriginType = get_origin(ExpectedType)
        if OriginType is not None:
            ExpectedType = OriginType

        def typecheck_list(value, typeArgs):
            if not isinstance(value, list):
                return False

            assert len(typeArgs) == 1
            
            return all(typecheck(item, typeArgs[0]) for item in value)
            
        def typecheck_method(value, typeArgs):
            if not isinstance(value, CallableType):
                return False

            argTypes, ReturnType = typeArgs

            actualParams = inspect.signature(value).parameters
            
            if len(argTypes) != len(actualParams):
                check(
                    False,
                    f"Method '{type(value.__self__).__name__}.{value.__name__}()' "
                    f"should take {len(argTypes)} arguments! "
                    f"(Your version takes {len(actualParams)} arguments)",
                )
                return False
            
            try:
                with _capture_output():
                    returnVal = value(*(get_mock(ArgType) for ArgType in argTypes))
            except Exception as e:
                check(
                    False,
                    "Encountered error while calling "
                    f"{cls.__name__}.{value.__name__}(): {e}",
                )
                return False

            returnTypeArgs = get_args(ReturnType)
            
            if get_origin(ReturnType) is Union:
                assert len(returnTypeArgs) > 1
                return any(
                    typecheck(returnVal, ReturnTypeArg)
                    for ReturnTypeArg in returnTypeArgs
                )
                
            return typecheck(returnVal, ReturnType)
            
        if ExpectedType is list:
            return typecheck_list(value, typeArgs)
        elif ExpectedType is CallableType:
            return typecheck_method(value, typeArgs)
        elif ExpectedType is Union:
            return any(typecheck(value, TypeArg) for TypeArg in typeArgs)
        else:
            return isinstance(value, ExpectedType)

    # Check each expected attribute of the class to make sure they are present
    # and of the right type.
    for fieldName, ExpectedType in expectedTypeForField.items():
        if fieldName == '__init__':
            continue

        try:
            attr = getattr(testObject, fieldName)
        except AttributeError:
            if get_origin(ExpectedType) is CallableType:
                check(
                    False,
                    f"{cls.__name__} class must have a '.{fieldName}()' method!",
                )
            else:
                check(
                    False,
                    f"{cls.__name__} class must have a '.{fieldName}' attribute!",
                )
        else:
            if get_origin(ExpectedType) is CallableType:
                check(
                    typecheck(attr, ExpectedType),
                    f"Method '{cls.__name__}.{fieldName}()' must be a "
                    f"{_type_str(ExpectedType)}!",
                )
            else:
                check(
                    typecheck(attr, ExpectedType),
                    f"Attribute '{cls.__name__}.{fieldName}' must be a "
                    f"{_type_str(ExpectedType)}! "
                    "(Your version was found to be a "
                        f"{_type_str(type(attr), value=attr)})",
                )

    return not _spew_errors(errors)


def _spew_errors(errors):
    if len(errors) == 0:
        return False

    print(
        f"Found {len(errors)} Pokemon Tournament driver compatibility errors:", 
        file=sys.stderr,
    )
    for error in errors:
        print(f"\t- {error}", file=sys.stderr)

    print("", file=sys.stderr)
    
    return True


@contextmanager
def _capture_output():
    capture = StringIO()

    stdout = sys.stdout
    stderr = sys.stderr
    
    try:
        sys.stdout = capture
        sys.stderr = capture
        
        yield capture
        
    finally:
        sys.stdout = stdout
        sys.stderr = stderr


def _suppress_output(callable):
    with _capture_output():
        return callable()


def _type_str(Type, value=None):
    if Type is None:
        Type = type(None)

    typeArgs = get_args(Type)
    OriginType = get_origin(Type)

    if OriginType is CallableType:
        argTypes, returnType = typeArgs

        if len(argTypes) == 0:
            argStr = 'nothing'
        elif len(argTypes) == 1:
            argStr = _type_str(argTypes[0])
        else:
            argStr = f"({', '.join(_type_str(ArgType) for ArgType in argTypes)})"
            
        return f"method that takes {argStr} and returns {_type_str(returnType)}"
        
    elif OriginType is list:
        assert len(typeArgs) == 1
        ItemType = typeArgs[0]
        return f"list of {_type_str(ItemType, value=value)}" + (
            " objects" if ItemType not in (int, float, str, bool, list) else ""
        )
        
    elif OriginType is Union:
        assert len(typeArgs) > 1
        return " or ".join(
            _type_str(TypeAlternative) for TypeAlternative in typeArgs
        )
        
    elif Type is list and value is not None:
        itemTypes = [
            type(item) if type(item).__name__ != 'Mock' else item.__class__
            for item in value
        ]
        itemTypesDeduped = set(itemTypes)
        
        if len(itemTypesDeduped) == 0:
            return "empty list"
        elif len(itemTypesDeduped) == 1:
            item = value[0]
            ItemType = type(item)
            return f"list of {_type_str(ItemType, value=item)}" + (
                " objects" if ItemType not in (int, float, str, bool, list) else ""
            )
        else:
            return "list containing " + ', '.join(
                _type_str(ItemType, value=item)
                for ItemType, item in zip(itemTypes, value)
            )

    elif Type.__name__ == 'Mock' and value is not None:
        return _type_str(value.__class__, value=value)
    
    elif Type is type:
        return 'class'

    elif Type is type(None):
        return 'nothing'
        
    else:
        return Type.__name__


def _do_checks():
    import pokemon

    failed = False
        
    if not check_module(pokemon):
        failed = True

    try:
        import pokemon_team
    except ImportError:
        pass
    else:
        if not check_module(pokemon_team):
            failed = True
            
    if failed:
        sys.exit(1)

    failed = False
    
    if not check_class(pokemon.Player):
        failed = True
    
    if not check_class(pokemon.Pokemon):
        failed = True
    
    if not check_class(pokemon.Move):
        failed = True

    if failed:
        sys.exit(1)


_do_checks()
