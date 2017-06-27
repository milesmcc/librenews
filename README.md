# LibreNews-Server

LibreNews-Server is the server side of the LibreNews ecosystem. It provides a RESTful JSON api by which clients can retrieve the twenty latest breaking news notifications. This implementation uses Twitter's BBC breaking news account to detect breaking news, however it is possible to implement a LibreNews that uses a different source of implementation — just update the `flashes.py` file as necessary.

This file will provide three documentations: 1) how to use LibreNews-Server from the perspective of a user, 2) how to use LibreNews server from the perspective of a developer who is making a LibreNews client, and 3) from the perspective of a developer who wants to modify or build a new LibreNews-Server.

## 1. End-user documentation
