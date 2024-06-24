from datetime import datetime
import logging
from typing import Union
from bson import ObjectId
from fastapi.responses import JSONResponse
from api.controller.UserController import UserController
from api.model.ChatModel import Chat
from api.model.MessageModel import MessageModel
from api.model.ParticipantModel import Participant
from api.schema.ParticipantSchema import RequestAddMessage, RequestAddParticipant
from api.schema.UserSchema import UserToken
from helper.database import (
    chat_collection,
    user_collection,
    message_collection,
    participant_collection,
)


def contact_helper(contact) -> dict:
    return {
        "id": str(contact["_id"]),
        "name": contact["name"],
        "is_group": contact["is_group"],
        "created_by": contact["created_by"],
        "created_at": contact["created_at"],
    }


def chat_helper(chat) -> dict:
    return {
        "id": str(chat["_id"]),
        "name": chat["name"],
        "is_group": chat["is_group"],
        "created_by": chat["created_by"],
        "created_at": chat["created_at"],
    }


class ChatController:
    @staticmethod
    async def get_chats(user: UserToken):
        contacts = await participant_collection.find(
            {"created_by": user.get("id")}
        ).to_list(100)
        if not contacts:
            html_contacts = "No contacts found"
        else:
            html_contacts = ""
            for contact in contacts:
                contact_name = await user_collection.find_one(
                    {"_id": str(ObjectId(contact["user_id"]))}
                )
                html_contacts += f"""
                    <li>
                        <a onclick="openChat('{contact['chat_id']}')" style="cursor: pointer" id="contact-{contact['chat_id']}" class="list-contact">
                            <div class="d-flex align-items-start">
                                <div class="flex-shrink-0 me-3 align-self-center">
                                    <div class="user-img online">
                                        <div class="avatar-xs align-self-center">
                                            <span
                                                class="avatar-title rounded-circle bg-primary-subtle text-primary">
                                                {contact_name["name"][0]}
                                            </span>
                                        </div>
                                        <span class="user-status"></span>
                                    </div>
                                </div>

                                <div class="flex-grow-1 overflow-hidden">
                                    <h5 class="text-truncate font-size-14 mb-1">
                                       {contact_name["name"]}
                                    </h5>
                                    <p class="text-truncate mb-0">
                                        Hello
                                    </p>
                                </div>

                                <div class="flex-shrink-0">
                                    <div class="font-size-11">02 min</div>
                                </div>
                            </div>
                        </a>
                    </li>
                """

        html_sidebar = f"""
            <div class="chat-leftsidebar card" style="height: 100vh !important">
                <div class="p-3 px-4">
                    <div class="d-flex align-items-start">
                        <div class="flex-shrink-0 me-3 align-self-center">
                            
                        </div>

                        <div class="flex-grow-1">
                            <h5 class="font-size-16 mb-1">
                                <a href="#" class="text-reset">{user.get("name")}
                                    <i class="mdi mdi-circle text-success align-middle font-size-10 ms-1"></i></a>
                            </h5>
                            <p class="text-muted mb-0">Available</p>
                        </div>

                        <div class="flex-shrink-0">
                            <div class="dropdown chat-noti-dropdown">
                                <button class="btn dropdown-toggle py-0" type="button" data-bs-toggle="dropdown"
                                    aria-haspopup="true" aria-expanded="false">
                                    <i class="uil uil-ellipsis-h"></i>
                                </button>
                                <div class="dropdown-menu dropdown-menu-end">
                                    <a class="dropdown-item" href="#" data-bs-toggle="modal"
                                        data-bs-target="#profileModal">Profile</a>
                                    <a class="dropdown-item" href="#">Edit</a>
                                    <a class="dropdown-item" href="#">Add Contact</a>
                                    <a class="dropdown-item" href="#">Setting</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="p-3">
                    <div class="search-box chat-search-box">
                        <div class="position-relative">
                            <input type="text" class="form-control bg-light border-light rounded" placeholder="Search..." />
                            <i class="uil uil-search search-icon"></i>
                        </div>
                    </div>
                </div>

                <div class="pb-3 h-100 overflow-auto">
                    <div class="chat-message-list" data-simplebar style="height: 100vh !important">
                        <div class="p-4 border-top">
                            <div>
                                <div class="float-end">
                                    <a href="javascript:void(0);" class="text-primary"><i class="mdi mdi-plus"></i> New
                                        Group</a>
                                </div>
                                <h5 class="font-size-16 mb-3">
                                    <i class="uil uil-users-alt me-1"></i> Groups
                                </h5>

                                <ul class="list-unstyled chat-list group-list">
                                    
                                </ul>
                            </div>
                        </div>

                        <div class="p-4 border-top">
                            <div>
                                <div class="float-end">
                                    <a href="" class="text-primary" data-bs-toggle="modal"
                                        data-bs-target="#addContactModal"><i class="mdi mdi-plus"></i> New
                                        Contact</a>
                                </div>
                                <h5 class="font-size-16 mb-3">
                                    <i class="uil uil-user me-1"></i> Contacts
                                </h5>

                                <ul class="list-unstyled chat-list">
                                    {html_contacts}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- end chat-leftsidebar -->

            <div class="w-100 user-chat mt-4 mt-sm-0 ms-lg-1" id="chat-content">

            </div>
        """

        # Get all users
        users = await UserController.get_users(user)
        html_chats = ""
        for item in users:
            html_chats += f"""
                <li>
                    <a href="#" onclick="addContact('{item.get('id')}')">
                        <div class="d-flex align-items-start">
                            <div class="flex-shrink-0 me-3 align-self-center">
                                <div class="user-img online">
                                    <div class="avatar-xs align-self-center">
                                        <span
                                            class="avatar-title rounded-circle bg-primary-subtle text-primary">
                                            {item.get('name')[0]}
                                        </span>
                                    </div>
                                    <span class="user-status"></span>
                                </div>
                            </div>

                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="text-truncate font-size-14 mb-1">
                                    {item.get('name')}
                                </h5>
                                <p class="text-truncate text-body mb-0">
                                    {item.get('email')} | {item.get('phone')}
                                </p>
                            </div>
                            <div class="flex-shrink-0">
                                <div class="font-size-11">02 min</div>
                            </div>
                        </div>
                    </a>
                </li>
            """

        return {"html_sidebar": html_sidebar, "html_chats": html_chats}

    @staticmethod
    async def add_chat(request: RequestAddParticipant, user: UserToken):
        try:
            get_user = await user_collection.find_one(
                {"_id": str(ObjectId(request.user_id))}
            )
            if get_user is None:
                return JSONResponse(
                    status_code=404, content={"message": "User not found"}
                )
            if request.user_id == user.get("id"):
                return JSONResponse(
                    status_code=400, content={"message": "You can't add yourself"}
                )

            # Check if chat already exists
            get_participant = await participant_collection.find_one(
                {"user_id": request.user_id, "created_by": user.get("id")}
            )
            if get_participant:
                return JSONResponse(
                    status_code=400, content={"message": "Chat already exists"}
                )
            else:
                # Add chat
                chat = Chat(created_by=str(ObjectId(user.get("id"))))
                chat.id = str(ObjectId())
                insert_result = await chat_collection.insert_one(
                    chat.dict(by_alias=True)
                )
                chat.id = str(insert_result.inserted_id)
                # Add participant
                participant = Participant(
                    chat_id=str(ObjectId(chat.id)),
                    user_id=str(ObjectId(request.user_id)),
                    created_by=str(ObjectId(user.get("id"))),
                )
                participant.id = str(ObjectId())
                insert_result = await participant_collection.insert_one(
                    participant.dict(by_alias=True)
                )
                participant.id = str(insert_result.inserted_id)

                # Add user to chat
                participant = Participant(
                    chat_id=str(ObjectId(chat.id)),
                    user_id=str(ObjectId(user.get("id"))),
                    created_by=str(ObjectId(request.user_id)),
                )
                participant.id = str(ObjectId())
                insert_result = await participant_collection.insert_one(
                    participant.dict(by_alias=True)
                )
                participant.id = str(insert_result.inserted_id)
                return JSONResponse(status_code=201, content={"message": "Chat added"})
        except Exception as e:
            logging.exception(e)
            return JSONResponse(
                status_code=500, content={"message": "Internal server error"}
            )

    @staticmethod
    async def get_chat(chat_id: str, user: UserToken):
        try:
            # Find the participant document
            get_participants = await participant_collection.find_one(
                {
                    "chat_id": str(ObjectId(chat_id)),
                    # Uncomment and modify this line if needed
                    "user_id": {"$ne": str(ObjectId(user.get("id")))},
                }
            )

            # If no participants found, return a 404 error
            if get_participants is None:
                return JSONResponse(
                    status_code=404, content={"message": "Participants not found"}
                )

            # Get user
            get_user = await user_collection.find_one(
                {"_id": str(ObjectId(get_participants["user_id"]))}
            )
            # return JSONResponse(status_code=200, content=get_user['name'])

            get_message = await message_collection.find(
                {"chat_id": str(ObjectId(chat_id))}
            ).to_list(100)
            html_message = ""
            if get_message is not None or len(get_message) > 0:
                for item in get_message:
                    if item["user_id"] == user.get("id"):
                        html_message += f"""
                        <li class="right">
                            <div class="conversation-list">
                                <div class="ctext-wrap">
                                    <div class="ctext-wrap-content">
                                        <h5 class="font-size-14 conversation-name">
                                            <a href="#" class="text-reset">You</a>
                                            <span
                                                class="d-inline-block font-size-12 text-muted ms-2">{item['created_at']}</span>
                                        </h5>
                                        <p class="mb-0">{item['content']}</p>
                                    </div>
                                    <div class="dropdown align-self-start">
                                        <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                                            aria-haspopup="true" aria-expanded="false">
                                            <i class="uil uil-ellipsis-v"></i>
                                        </a>
                                        <div class="dropdown-menu">
                                            <a class="dropdown-item" href="#">Copy</a>
                                            <a class="dropdown-item" href="#">Save</a>
                                            <a class="dropdown-item" href="#">Forward</a>
                                            <a class="dropdown-item" href="#">Delete</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </li>
                        """
                    else:
                        contact_name = await user_collection.find_one(
                            {"_id": str(ObjectId(item["user_id"]))}
                        )
                        html_message += f"""
                        <li>
                            <div class="conversation-list">
                                <div class="ctext-wrap">
                                    <div class="ctext-wrap-content">
                                        <h5 class="font-size-14 conversation-name">
                                            <a href="#" class="text-reset">{contact_name['name']}</a>
                                            <span
                                                class="d-inline-block font-size-12 text-muted ms-2">{item['created_at']}</span>
                                        </h5>
                                        <p class="mb-0">{item['content']}</p>
                                    </div>
                                    <div class="dropdown align-self-start">
                                        <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                                            aria-haspopup="true" aria-expanded="false">
                                            <i class="uil uil-ellipsis-v"></i>
                                        </a>
                                        <div class="dropdown-menu">
                                            <a class="dropdown-item" href="#">Copy</a>
                                            <a class="dropdown-item" href="#">Save</a>
                                            <a class="dropdown-item" href="#">Forward</a>
                                            <a class="dropdown-item" href="#">Delete</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </li>
                        """

            html_contacts = f"""
            <div class="card h-100" style="overflow: hidden">
                <div class="p-3 px-lg-4 border-bottom">
                    <div class="row">
                        <div class="col-md-4 col-6">
                            <h5 class="font-size-16 mb-1 text-truncate">
                                <a href="#" class="text-reset">
                                    {get_user["name"]}
                                </a>
                            </h5>
                            <p class="text-muted text-truncate mb-0">
                                Available
                            </p>
                        </div>
                        <div class="col-md-8 col-6">
                            <ul class="list-inline user-chat-nav text-end mb-0">
                                <li class="list-inline-item">
                                    <div class="dropdown">
                                        <button class="btn nav-btn dropdown-toggle" type="button" data-bs-toggle="dropdown"
                                            aria-haspopup="true" aria-expanded="false">
                                            <i class="uil uil-search"></i>
                                        </button>
                                        <div class="dropdown-menu dropdown-menu-end dropdown-menu-md">
                                            <form class="p-2">
                                                <div>
                                                    <input type="text" class="form-control rounded" placeholder="Search..." />
                                                </div>
                                            </form>
                                        </div>
                                    </div>
                                </li>

                                <li class="list-inline-item">
                                    <div class="dropdown">
                                        <button class="btn nav-btn dropdown-toggle" type="button" data-bs-toggle="dropdown"
                                            aria-haspopup="true" aria-expanded="false">
                                            <i class="uil uil-ellipsis-h"></i>
                                        </button>
                                        <div class="dropdown-menu dropdown-menu-end">
                                            <a class="dropdown-item" href="#">Profile</a>
                                            <a class="dropdown-item" href="#">Archive</a>
                                            <a class="dropdown-item" href="#">Muted</a>
                                            <a class="dropdown-item" href="#">Delete</a>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div>
                    <div class="chat-conversation py-3">
                        <ul class="list-unstyled mb-0 chat-conversation-message px-3" data-simplebar
                            style="height: calc(135vh - 417px)">
                            {html_message}
                        </ul>
                    </div>
                </div>

                <div class="p-3 chat-input-section" style="position: absolute; bottom: 0; width: 100%">
                    <div class="row">
                        <div class="col">
                            <div class="position-relative">
                                <input id="chat-input" type="text" class="form-control chat-input rounded"
                                    placeholder="Enter Message..." />
                            </div>
                        </div>
                        <div class="col-auto">
                            <button type="submit" class="btn btn-primary chat-send w-md waves-effect waves-light"
                                id="edit-event-btn" onclick="editEvent('{get_participants['chat_id']}')">
                                <span class="d-none d-sm-inline-block me-2">Send</span>
                                <i class="mdi mdi-send float-end"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            """
            # Return the user_id from the found participants document
            return JSONResponse(
                status_code=200, content={"html_contacts": html_contacts}
            )
        except Exception as e:
            logging.exception(e)
            return JSONResponse(
                status_code=500, content={"message": "Internal server error"}
            )

    @staticmethod
    async def add_message(
        chat_id: Union[str, ObjectId], request: RequestAddMessage, user: UserToken
    ):
        get_chat = await chat_collection.find_one({"_id": str(ObjectId(chat_id))})
        if get_chat is None:
            return JSONResponse(status_code=404, content={"message": "Chat not found"})
        message = MessageModel(
            chat_id=str(ObjectId(chat_id)),
            user_id=str(ObjectId(user.get("id"))),
            content=request.content,
        )
        message.id = str(ObjectId())
        await message_collection.insert_one(message.dict(by_alias=True))
        return JSONResponse(
            status_code=200, content={"message": "Message added successfully"}
        )
