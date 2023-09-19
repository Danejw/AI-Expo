from typing import List
from fastapi import HTTPException
from database.database_connection import DatabaseConnection
from models.ChatHistoryWithKey import ChatHistoryWithKey
from models.UserModels import User, UserRegistration, UserInDB
from models.ChatHistory import ChatHistory
from models.ChatMessage import ChatMessage

import json
from passlib.context import CryptContext


# Creating a CryptContext instance for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def create_user(self, user_data: UserRegistration) -> UserInDB:
        if self.get_user(user_data.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        
        hashed_password = pwd_context.hash(user_data.password)
        user_data.password = hashed_password
        
        query = "INSERT INTO users (username, email, password, full_name) VALUES (?, ?, ?, ?)"
        parameters = (user_data.username, user_data.email, hashed_password, user_data.full_name)
        self.db_connection.execute_query(query, parameters)
        return self.get_user(username=user_data.username)
    
    # get logged in user
    def get_user(self, username:str):
        query = "SELECT username, email, password, full_name, disabled, credits FROM users WHERE username = ?"
        parameters = (username,)
        cursor = self.db_connection.connect()
        cursor.execute(query, parameters)
        result = cursor.fetchone()
        self.db_connection.disconnect()

        if result:
            user_dict = {
                'username': result[0],
                'email': result[1],
                'hashed_password': result[2], # Include the hashed password
                'full_name': result[3],
                'disabled': bool(result[4]),
                'credits': result[5]
            }
            user = UserInDB(**user_dict)

            # Retrieve chat histories and build dictionary
            chat_histories_query = "SELECT key, history FROM chat_histories WHERE username = ?"
            chat_histories_cursor = self.db_connection.connect()
            chat_histories_cursor.execute(chat_histories_query, (username,))
            chat_histories_results = chat_histories_cursor.fetchall()
            self.db_connection.disconnect()

            chat_histories_dict = {result[0]: ChatHistory(history=[ChatMessage(**msg) for msg in json.loads(result[1])]) for result in chat_histories_results}
            user.chat_histories = chat_histories_dict

            return user
        else:
            return None

    # Retricted from users
    def get_all_users(self):
        query = "SELECT * FROM users"
        cursor = self.db_connection.connect()
        cursor.execute(query)
        results = cursor.fetchall()
        self.db_connection.disconnect()
        return [User(username=result[0], email=result[1], full_name=result[2], disabled=bool(result[3]), credits=result[4]) for result in results]

    # Need to be logged in and only have access to their own data
    def update_user(self, username:str, email:str=None, full_name:str=None):
        updates = []
        parameters = []
        if email:
            updates.append("email = ?")
            parameters.append(email)
        if full_name:
            updates.append("full_name = ?")
            parameters.append(full_name)
        parameters.append(username)
        query = f"UPDATE users SET {', '.join(updates)} WHERE username = ?"
        self.db_connection.execute_query(query, parameters)

    # Needs to be logged in and make sure that only the logged in user can delete thier own account
    def delete_user(self, username:str):
        query = "DELETE FROM users WHERE username = ?"
        parameters = (username)
        self.db_connection.execute_query(query, parameters)

    # Needs to be logged in and  only have access to their own history
    def add_chat_history(self, username: str, chat_history: ChatHistoryWithKey):
        query = "INSERT INTO chat_histories (key, username, history) VALUES (?, ?, ?)"
        parameters = (chat_history.key, username, json.dumps([msg.dict() for msg in chat_history.history]))
        self.db_connection.execute_query(query, parameters)

    # Needs to be logged in and make sure that only the logged in user can delete thier own chat histories
    def remove_chat_history(self, username: str, chat_history_key: int):
        query = "DELETE FROM chat_histories WHERE username = ? AND key = ?"
        parameters = (username, chat_history_key)
        self.db_connection.execute_query(query, parameters)

    
    # Needs to be logged in and only have access to their own history
    def get_chat_history_by_key(self, username: str, chat_history_key: int) -> ChatHistoryWithKey:
        query = "SELECT history FROM chat_histories WHERE username = ? AND key = ?"
        parameters = (username, chat_history_key)
        cursor = self.db_connection.connect()
        cursor.execute(query, parameters)
        result = cursor.fetchone()
        self.db_connection.disconnect()

        if result:
            history = [ChatMessage(**msg) for msg in json.loads(result[0])]
            chat_history_with_key = ChatHistoryWithKey(key=chat_history_key, history=history)
            print (chat_history_with_key)
            return chat_history_with_key
        else:
            return None



    def get_all_chat_histories(self, username: str) -> List[ChatHistoryWithKey]:
        query = "SELECT key, history FROM chat_histories WHERE username = ? ORDER BY key ASC"
        parameters = (username,)
        cursor = self.db_connection.connect()
        cursor.execute(query, parameters)
        results = cursor.fetchall()
        self.db_connection.disconnect()

        chat_histories = []
        for result in results:
            chat_history_key = result[0]
            history = [ChatMessage(**msg) for msg in json.loads(result[1])]
            chat_histories.append(ChatHistoryWithKey(key=chat_history_key, history=history))
        return chat_histories


    # Needs to be logged in and make sure that only the logged in user can only edit thier own chat histories
    def edit_message_in_history(self, username: str, chat_history_key: int, message_index: int, new_message: ChatMessage):
        # Retrieve the chat history
        query = "SELECT history FROM chat_histories WHERE username = ? AND key = ?"
        parameters = (username, chat_history_key)
        cursor = self.db_connection.connect()
        cursor.execute(query, parameters)
        result = cursor.fetchone()
        self.db_connection.disconnect()

        # Deserialize and update the chat history
        if result:
            history = [ChatMessage(**msg) for msg in json.loads(result[0])]
            chat_history_with_key = ChatHistoryWithKey(key=chat_history_key, history=history)
            chat_history_with_key.history[message_index] = new_message

            # Serialize and update the chat history in the database
            update_query = "UPDATE chat_histories SET history = ? WHERE username = ? AND key = ?"
            update_parameters = (json.dumps([chat_message.dict() for chat_message in chat_history_with_key.history]), username, chat_history_key)
            self.db_connection.execute_query(update_query, update_parameters)

                     
    # Add credits (needs to signed in and only can add credits to their own account)
    def add_credits(self, username:str, credits:int):
        query = "UPDATE users SET credits = credits + ? WHERE username = ?"
        user = self.get_user(username)
        user.credits + credits
        parameters = (credits, username)
        self.db_connection.execute_query(query, parameters)


    # Remove credits (needs to signed in and only can remove credits of their own account)
    def remove_credits(self, username:str, credits:int):
        query = "UPDATE users SET credits = credits - ? WHERE username = ?"
        user = self.get_user(username)
        if user.credits >= credits:
            user.credits - credits
            parameters = (credits, username)
            self.db_connection.execute_query(query, parameters)