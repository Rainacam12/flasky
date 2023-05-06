def test_read_all_crystals_returns_empty_list(client):
    # act
    response = client.get("/crystals")
    response_body = response.get_json()

    # assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_crystal(client, make_two_crystals):
    # Act
    response = client.get("/crystals/2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 2,
        "name": "Garnet",
        "color": "Red",
        "powers": "Awesomeness"
    }

def test_create_crystal_route(client):
     # Act
    response = client.post("/crystals", json={
        "name": "tiger's eye",
        "color": "golden brown",
        "powers": "mental clarity"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Crystal tiger's eye successfully created"