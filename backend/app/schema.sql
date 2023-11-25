CREATE TABLE User (
    UserId INT PRIMARY KEY,
    Username VARCHAR(255),
    Email VARCHAR(255),
    Password VARCHAR(255)
);

CREATE TABLE List (
    ListId INT PRIMARY KEY,
    Name VARCHAR(255),
    IsRecipe BOOLEAN
);

CREATE TABLE ListItem (
    ItemId INT PRIMARY KEY,
    ListId INT,
    Name VARCHAR(255),
    Quantity INT,
    BoughtQuantity INT,
    FOREIGN KEY (ListId) REFERENCES List(ListId)
);

CREATE TABLE ListUser (
    ListId INT,
    UserId INT,
    PRIMARY KEY (ListId, UserId),
    FOREIGN KEY (ListId) REFERENCES List(ListId),
    FOREIGN KEY (UserId) REFERENCES User(UserId)
);

-- Povoar users
INSERT INTO User (UserId, Username, Email, Password) VALUES
(1, 'user1', 'user1@example.com', 'password1'),
(2, 'user2', 'user2@example.com', 'password2');

-- Povoar listas
INSERT INTO List (ListId, Name, IsRecipe) VALUES
(1, 'Grocery List', FALSE),
(2, 'Recipe List', TRUE);

-- Povoar itens em listas
INSERT INTO ListItem (ItemId, ListId, Name, Quantity, BoughtQuantity) VALUES
(1, 1, 'Milk', 2, 0),
(2, 1, 'Eggs', 1, 1),
(3, 2, 'Chicken', 1, 0),
(4, 2, 'Tomatoes', 4, 0);

-- Povoar listas a users
INSERT INTO ListUser (ListId, UserId) VALUES
(1, 1),
(2, 1),
(2, 2);