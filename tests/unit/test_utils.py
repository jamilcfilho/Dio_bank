import pytest
from src.utils import eleva_quadrado, requires_role
from http import HTTPStatus


@pytest.mark.parametrize("test_input,expected", [(2, 4), (10, 100), (3, 9)])
def test_eleva_quadrado_sucesso(test_input, expected):
    resultado = eleva_quadrado(test_input)
    assert resultado == expected


@pytest.mark.parametrize("test_input,exc_class, msg", [("a", TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'"), (None, TypeError, "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'"),])
def test_eleva_quadrado_falha(test_input, exc_class, msg):
    with pytest.raises(exc_class) as exc:
        eleva_quadrado(test_input)
    assert str(
        exc.value) == msg


# Teste unitário através da função 'Mock' (chamamos de 'Mockar') dependências externas, exemplo, o 'get_jwt_identity' e o 'get_or_404'
def test_requires_role_success(mocker):
    # Realizando a estrutura 'GWT' dos testes:
    # Given - É o que forneço para o teste
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"

    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)

    decorated_function = requires_role("admin")(lambda: "Success")

    # When - O que executo
    result = decorated_function()

    # Then - O que eu verifico
    assert result == "Success"


def test_requires_role_fail(mocker):
    # Given
    mock_user = mocker.Mock()
    mock_user.role.name = "normal"

    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)

    decorated_function = requires_role("admin")(lambda: "Success")

    # When
    result = decorated_function()

    # Then
    assert result == (
        {"message": "Usuário não possui acesso!"}, HTTPStatus.UNAUTHORIZED)
