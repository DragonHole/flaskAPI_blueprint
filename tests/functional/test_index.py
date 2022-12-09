import pytest
import json

from project import create_app

def test_insert_user(test_client, reset):
    #test_client.delete("/reset_table")

    # with flask_app.test_client() as test_client:
    userA = dict(id='12', email='helloworld@gmail.com', password='13579', login_date='2022', created_at='2021', updated_at='2022')
    response = test_client.put("/insertUser",
                                json=userA
    )

    assert response.status_code == 201
    user = json.loads(response.data.decode('utf-8'))
    assert user == userA


def test_getAll(test_client, reset):
    response = test_client.get("/users")
    assert response.status_code == 200
    user = json.loads(response.data.decode('utf-8'))
    assert user == []

    userA = dict(id='12', email='helloworld@gmail.com', password='13579', login_date='2022', created_at='2021', updated_at='2022')
    test_client.put("/insertUser",
                                json=userA
    )
    response = test_client.get("/users")
    assert response.status_code == 200
    user = json.loads(response.data.decode('utf-8'))
    assert user == [userA]


    userB = dict(id='13', email='helloUserB@gmail.com', password='13333', login_date='2012', created_at='2008', updated_at='2022')
    response = test_client.put("/insertUser",
                               json=userB
    )
    response = test_client.get("/users")
    assert response.status_code == 200
    user = json.loads(response.data.decode('utf-8'))
    assert user == [userA, userB]


def test_getUserByID(test_client, reset):
    response = test_client.get("/user/30")
    assert response.status_code == 500

    userA = dict(id='12', email='helloworld@gmail.com', password='13579', login_date='2022', created_at='2021', updated_at='2022')
    test_client.put("/insertUser",
                    json=userA
    )
    response = test_client.get("/user/12")
    assert response.status_code == 200
    user = json.loads(response.data.decode('utf-8'))
    assert user == userA


    userB = dict(id='13', email='helloUserB@gmail.com', password='13333', login_date='2012', created_at='2008', updated_at='2022')
    response = test_client.put("/insertUser",
                                json=userB
    )
    response = test_client.get("/user/13")
    assert response.status_code == 200
    user = json.loads(response.data.decode('utf-8'))
    assert user == userB

    # request A again
    response = test_client.get("/user/12")
    assert response.status_code == 200
    user = json.loads(response.data.decode('utf-8'))
    assert user == userA


def test_update_user(test_client, reset):
    userA = dict(id='12', email='helloworld@gmail.com', password='13579', login_date='2022', created_at='2021', updated_at='2022')
    test_client.put("/insertUser",
                                json=userA
    )

    userB = dict(id='12', email='helloUserB@gmail.com', password='13333', login_date='2012', created_at='2008', updated_at='2022')
    response = test_client.post("/updateUser",
                                json=userB
    )
    assert response.status_code == 200
    user = json.loads(response.data.decode('utf-8'))
    assert user == userB

    response = test_client.get("/users")
    assert response.status_code == 200
    user = json.loads(response.data.decode('utf-8'))
    assert user == [userB]


def test_delete_user(test_client, reset):
    userA = dict(id='12', email='helloworld@gmail.com', password='13579', login_date='2022', created_at='2021', updated_at='2022')
    test_client.put("/insertUser",
                                json=userA
    )

    userB = dict(id='14', email='helloUserB@gmail.com', password='13333', login_date='2012', created_at='2008', updated_at='2022')
    test_client.put("/insertUser",
                    json=userB
    )
    response = test_client.delete("/deleteUser/12")
    assert response.status_code == 200
    res = json.loads(response.data.decode('utf-8'))
    assert res == {"status" : "User deleted successfully"}

    response = test_client.get("/users")
    assert response.status_code == 200
    user = json.loads(response.data.decode('utf-8'))
    assert user == [userB]


    response = test_client.delete("/deleteUser/14")
    assert response.status_code == 200
    res = json.loads(response.data.decode('utf-8'))
    assert res == {"status" : "User deleted successfully"}

    response = test_client.get("/users")
    assert response.status_code == 200
    user = json.loads(response.data.decode('utf-8'))
    assert user == []